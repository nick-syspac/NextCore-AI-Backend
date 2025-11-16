"""
AI Gateway - Routes AI model requests to appropriate providers.

This service handles:
- Model routing and load balancing
- Usage metering and token counting
- Rate limiting
- Request/response logging
- Multi-provider support (OpenAI, Anthropic, etc.)
"""

import hashlib
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import httpx
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import redis.asyncio as redis

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings."""

    redis_url: str = "redis://localhost:6379/2"
    control_plane_url: str = "http://localhost:8000"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    rate_limit_per_minute: int = 60

    class Config:
        env_file = ".env"


settings = Settings()

# Global Redis connection pool
redis_client: redis.Redis | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Lifespan context manager for startup/shutdown events."""
    global redis_client

    # Startup
    logger.info("Starting AI Gateway...")
    redis_client = await redis.from_url(settings.redis_url, decode_responses=True)
    logger.info("Connected to Redis")

    yield

    # Shutdown
    logger.info("Shutting down AI Gateway...")
    if redis_client:
        await redis_client.close()
    logger.info("Redis connection closed")


app = FastAPI(
    title="RTOComply AI Gateway",
    description="AI model routing and metering gateway",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models
class ChatMessage(BaseModel):
    """Chat message structure."""

    role: str = Field(..., description="Role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class ChatCompletionRequest(BaseModel):
    """Request for chat completion."""

    model: str = Field(..., description="Model identifier (e.g., gpt-4, claude-3)")
    messages: list[ChatMessage] = Field(..., description="Conversation messages")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, gt=0, le=4096)
    stream: bool = Field(default=False, description="Enable streaming responses")
    tenant_id: str = Field(..., description="Tenant identifier")


class UsageInfo(BaseModel):
    """Token usage information."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """Response from chat completion."""

    id: str
    model: str
    choices: list[dict[str, Any]]
    usage: UsageInfo
    created: int = Field(default_factory=lambda: int(time.time()))


class ErrorResponse(BaseModel):
    """Error response structure."""

    error: dict[str, Any]


# Dependency: Get Redis client
async def get_redis() -> redis.Redis:
    """Dependency to get Redis client."""
    if not redis_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis connection not available",
        )
    return redis_client


# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    response = await call_next(request)

    # Log response
    duration = time.time() - start_time
    logger.info(
        f"Response: {response.status_code} for {request.method} {request.url.path} ({duration:.2f}s)"
    )

    return response


# Rate limiting
async def check_rate_limit(tenant_id: str, redis_client: redis.Redis) -> bool:
    """
    Check if tenant is within rate limits.

    Args:
        tenant_id: Tenant identifier
        redis_client: Redis client instance

    Returns:
        True if within limits, False otherwise
    """
    key = f"ratelimit:{tenant_id}:{int(time.time() // 60)}"

    try:
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, 60)

        if current > settings.rate_limit_per_minute:
            logger.warning(f"Rate limit exceeded for tenant: {tenant_id}")
            return False

        return True
    except Exception as e:
        logger.error(f"Rate limit check failed: {e}")
        return True  # Fail open


# Token counting (simplified - use tiktoken for production)
def count_tokens(text: str) -> int:
    """
    Estimate token count for text.

    This is a simplified estimation. Use tiktoken for accurate counting.
    """
    # Rough estimation: ~4 characters per token
    return len(text) // 4


def estimate_request_tokens(request: ChatCompletionRequest) -> int:
    """Estimate tokens for a request."""
    total = 0
    for message in request.messages:
        total += count_tokens(message.content)
    return total + 10  # Add overhead for formatting


# Route model requests to appropriate provider
async def route_to_provider(request: ChatCompletionRequest) -> dict[str, Any]:
    """
    Route request to appropriate AI provider based on model.

    Args:
        request: Chat completion request

    Returns:
        Response from the provider

    Raises:
        HTTPException: If provider call fails
    """
    model = request.model.lower()

    # Determine provider
    if model.startswith("gpt") or model.startswith("o1"):
        provider = "openai"
        api_key = settings.openai_api_key
        endpoint = "https://api.openai.com/v1/chat/completions"
    elif model.startswith("claude"):
        provider = "anthropic"
        api_key = settings.anthropic_api_key
        endpoint = "https://api.anthropic.com/v1/messages"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported model: {request.model}",
        )

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Provider {provider} not configured",
        )

    # Prepare request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    if provider == "anthropic":
        headers["anthropic-version"] = "2023-06-01"

    payload = {
        "model": request.model,
        "messages": [msg.model_dump() for msg in request.messages],
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
    }

    # Make request to provider
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Provider request failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Provider request failed: {str(e)}",
            )


# Record usage metrics
async def record_usage(
    tenant_id: str, model: str, tokens: int, redis_client: redis.Redis
) -> None:
    """
    Record usage metrics to Redis.

    Args:
        tenant_id: Tenant identifier
        model: Model used
        tokens: Number of tokens used
        redis_client: Redis client instance
    """
    try:
        # Daily usage
        date_key = time.strftime("%Y-%m-%d")
        await redis_client.hincrby(f"usage:{tenant_id}:{date_key}", model, tokens)

        # Monthly usage
        month_key = time.strftime("%Y-%m")
        await redis_client.hincrby(f"usage:{tenant_id}:{month_key}", "total", tokens)

        logger.info(
            f"Usage recorded: tenant={tenant_id}, model={model}, tokens={tokens}"
        )
    except Exception as e:
        logger.error(f"Failed to record usage: {e}")


# Endpoints
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "ai-gateway",
        "redis": "connected" if redis_client else "disconnected",
    }


@app.get("/metrics/{tenant_id}")
async def get_metrics(tenant_id: str, r: redis.Redis = Depends(get_redis)):
    """
    Get usage metrics for a tenant.

    Args:
        tenant_id: Tenant identifier
        r: Redis client dependency

    Returns:
        Usage metrics
    """
    try:
        date_key = time.strftime("%Y-%m-%d")
        month_key = time.strftime("%Y-%m")

        daily_usage = await r.hgetall(f"usage:{tenant_id}:{date_key}")
        monthly_usage = await r.hgetall(f"usage:{tenant_id}:{month_key}")

        return {
            "tenant_id": tenant_id,
            "daily": daily_usage,
            "monthly": monthly_usage,
        }
    except Exception as e:
        logger.error(f"Failed to fetch metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch metrics",
        )


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(
    request: ChatCompletionRequest, r: redis.Redis = Depends(get_redis)
):
    """
    Process chat completion request.

    Args:
        request: Chat completion request
        r: Redis client dependency

    Returns:
        Chat completion response
    """
    # Check rate limit
    if not await check_rate_limit(request.tenant_id, r):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded"
        )

    # Estimate tokens
    estimated_tokens = estimate_request_tokens(request)

    logger.info(
        f"Processing request: tenant={request.tenant_id}, "
        f"model={request.model}, estimated_tokens={estimated_tokens}"
    )

    # Route to provider
    try:
        response = await route_to_provider(request)

        # Extract usage information
        usage = response.get("usage", {})
        total_tokens = usage.get("total_tokens", estimated_tokens)

        # Record usage
        await record_usage(request.tenant_id, request.model, total_tokens, r)

        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "RTOComply AI Gateway",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/v1/chat/completions",
            "metrics": "/metrics/{tenant_id}",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
