# Portal Authentication High-Level Design

## Overview
This document outlines the high-level design for connecting the RTOComply AI Portal (Frontend) to the Backend using Supabase Authentication.

## Architecture
The authentication flow follows a **Client-Side Auth** model where the Portal interacts directly with Supabase for login, and then uses the returned JWT to authenticate with the Backend.

```mermaid
sequenceDiagram
    participant User
    participant Portal as Portal (Frontend)
    participant Supabase as Supabase Auth
    participant Backend as Control Plane API

    User->>Portal: Enter Credentials (Email/Pass)
    Portal->>Supabase: supabase.auth.signInWithPassword()
    Supabase-->>Portal: Return Session (Access Token / JWT)
    Portal->>Portal: Store Session (Context/LocalStorage)
    
    Note over Portal, Backend: Authenticated API Call
    Portal->>Backend: API Request (Header: Authorization: Bearer <JWT>)
    Backend->>Backend: Verify JWT with Supabase Secret
    Backend-->>Portal: API Response
```

## Components

### 1. Supabase Client
- **Library**: `@supabase/supabase-js`
- **Configuration**:
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- **Singleton**: Create a single instance of the Supabase client to be used throughout the app.

### 2. AuthProvider (Context)
- **Purpose**: Manage global authentication state (user, session, loading).
- **Responsibilities**:
  - Initialize Supabase auth listener (`onAuthStateChange`).
  - Expose `user`, `session`, `login`, `logout` to the rest of the app.
  - Handle session persistence and restoration on page load.

### 3. Login Page
- **UI**: Form with Email and Password fields.
- **Logic**:
  - Call `supabase.auth.signInWithPassword({ email, password })`.
  - Handle errors (invalid credentials, email not confirmed).
  - Redirect to Dashboard on success.

### 4. API Client / Interceptor
- **Purpose**: Attach the authentication token to every request sent to the Backend.
- **Logic**:
  - Before sending a request, retrieve the current session's `access_token`.
  - Add header: `Authorization: Bearer <access_token>`.
  - Handle `401 Unauthorized` responses (e.g., trigger logout or token refresh).

## Data Flow

1.  **Login**:
    - User submits form.
    - Supabase validates credentials.
    - Returns `access_token` (JWT) and `user` object.

2.  **Backend Request**:
    - Portal sends `GET /api/tenants/`.
    - Header: `Authorization: Bearer eyJhbGciOiJIUzI1Ni...`
    - Backend `SupabaseAuthentication` class decodes and verifies the token.
    - Backend creates/retrieves the Django User matching the token's email.
    - Request proceeds as authenticated user.

3.  **Logout**:
    - Portal calls `supabase.auth.signOut()`.
    - Clears local session.
    - Redirects to Login page.

## Security Considerations
- **HTTPS**: All communication must be over HTTPS.
- **Token Storage**: Supabase client handles token storage securely (localStorage/cookies).
- **Token Expiry**: Supabase tokens expire (usually 1 hour). The client library handles auto-refreshing. Ensure the API client always gets the *current* token from the session.
