# Study Coach Chatbot

## Overview
24/7 AI tutor powered by LLM and vector database for contextual student support. Provides instant help with homework, exam prep, concept review, and personalized learning guidance.

## Features

### 🤖 Conversational AI
- **Real-time Chat**: Live messaging with AI study coach
- **Context-Aware Responses**: Retrieves relevant course materials using vector search
- **Multi-Session Support**: Persistent conversation history across sessions
- **Sentiment Analysis**: Detects student confusion, frustration, and engagement
- **Intent Detection**: Understands question types and learning needs

### 📚 Vector Database Integration
- **Contextual Retrieval**: Searches knowledge base using semantic similarity
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Top-K Search**: Retrieves 5 most relevant documents per query
- **Similarity Threshold**: 0.7 minimum for relevance
- **Document Types**: Syllabi, lecture notes, textbooks, FAQs, study guides

### 📊 Analytics & Insights
- **Session Analytics**: Track engagement, message count, duration
- **Subject Analysis**: Identify most discussed topics
- **Sentiment Tracking**: Monitor emotional state trends
- **Knowledge Gaps**: Detect areas needing additional support
- **Satisfaction Ratings**: 5-star feedback system

### ⚙️ Configuration
- **LLM Selection**: Support for GPT-4, GPT-3.5, Claude-3
- **Temperature Control**: Adjust response creativity
- **Coaching Style**: Encouraging, Socratic, Direct, or Adaptive
- **Safety Features**: Content filtering, profanity detection, crisis escalation
- **24/7 Availability**: Always-on student support

## Architecture

### Backend Models
1. **ChatSession**: Manages conversation sessions
   - Session metadata (subject, topic, type)
   - Status tracking (active, completed, archived)
   - Analytics (message count, duration, ratings)
   - Context tracking (materials referenced, concepts discussed)

2. **ChatMessage**: Individual messages
   - Role-based (student, coach, system)
   - LLM metadata (tokens, model, response time)
   - Vector search results and relevance scores
   - Sentiment and intent detection

3. **KnowledgeDocument**: Vector DB documents
   - Document types (syllabus, notes, textbook, etc.)
   - Embedding storage and chunking
   - Retrieval tracking and usage analytics
   - Access control and visibility

4. **CoachingInsight**: Aggregated analytics
   - Time-period metrics
   - Subject and topic analysis
   - Sentiment trends
   - Recommended actions

5. **CoachConfiguration**: System settings
   - LLM parameters
   - Coaching personality
   - Vector DB settings
   - Safety and moderation

### API Endpoints
- `POST /sessions/send_message/` - Send message and get AI response
- `POST /sessions/{id}/rate_session/` - Rate completed session
- `GET /sessions/dashboard/` - Get dashboard statistics
- `GET /messages/` - Retrieve message history
- `GET /documents/` - List knowledge base documents
- `POST /insights/generate_insights/` - Generate student insights
- `GET /config/` - Retrieve coach configuration

### Frontend Interface
- **Live Chat Tab**: Real-time conversation interface
- **Session History Tab**: Browse past conversations
- **Knowledge Base Tab**: View vector DB documents
- **Insights Tab**: Analytics and recommendations
- **Configuration Tab**: Customize AI behavior

## Technical Stack
- **LLM**: GPT-4, GPT-3.5-turbo, Claude-3 (configurable)
- **Embeddings**: all-MiniLM-L6-v2 (384-dim)
- **Vector DB**: Simulated (production: Pinecone, Weaviate, Qdrant)
- **NLP**: Sentiment analysis, intent detection
- **Backend**: Django REST Framework
- **Frontend**: Next.js 14 with TypeScript

## Use Cases

### Homework Help
Student asks about specific assignment problems, gets step-by-step guidance without direct answers.

### Concept Review
Coach retrieves lecture notes and textbook chapters to explain concepts with examples.

### Exam Preparation
Provides study strategies, practice questions, and reviews key topics.

### Project Guidance
Offers structure, milestones, and resources for long-term projects.

### Career Advice
Discusses career paths, industry trends, and skill development.

### Study Tips
Shares learning techniques, time management, and productivity strategies.

## Scalability
- **Concurrent Sessions**: Handles multiple students simultaneously
- **Vector Search**: Fast retrieval with indexed embeddings
- **LLM Load Balancing**: Fallback models for high demand
- **Session Persistence**: Database-backed conversation history
- **Caching**: Similarity scores and frequent queries

## Safety & Moderation
- **Content Filtering**: Blocks inappropriate content
- **Profanity Detection**: Maintains professional environment
- **Crisis Keywords**: Escalates mental health concerns
- **Response Guidelines**: Ensures educational integrity
- **Prohibited Topics**: Configurable restricted subjects

## Future Enhancements
- Multi-language support
- Voice chat integration
- Image analysis (diagrams, handwriting)
- Collaborative study groups
- Scheduled tutoring sessions
- Mobile app support
- Integration with LMS platforms
