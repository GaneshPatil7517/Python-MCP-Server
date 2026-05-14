# Architecture Overview

## System Design

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer                              │
│  (Claude Desktop | Cursor | VS Code | Other MCP Clients)   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ MCP Protocol
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  Reverse Proxy (Nginx)                       │
│                    - SSL/TLS                                 │
│                    - Rate Limiting                           │
│                    - Load Balancing                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              FastAPI Application Server                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Middleware Stack                         │  │
│  │  - Request Logging                                   │  │
│  │  - Authentication (API Key / Bearer Token)           │  │
│  │  - Rate Limiting                                     │  │
│  │  - Security Headers                                  │  │
│  │  - CORS                                              │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Endpoint Routers                         │  │
│  │  - Tools API        (/api/tools)                     │  │
│  │  - Resources API    (/api/resources)                 │  │
│  │  - Prompts API      (/api/prompts)                   │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────┬─────────────────────────┬──────────────┬─────────┘
           │                         │              │
           │ Execute                 │ Fetch        │ Generate
           │                         │              │
┌──────────▼────────┐  ┌─────────────▼──┐  ┌──────▼────────┐
│   Tools Layer     │  │ Resources Layer│  │ Prompts Layer │
│                   │  │                │  │               │
│ - get_weather     │  │ - API Docs     │  │ - Debugging   │
│ - github_lookup   │  │ - Server Stats │  │ - Code Review │
│ - summarize_text  │  │ - Project Info │  │ - Architecture│
│ - system_status   │  │ - Usage Guide  │  │ - API Docs    │
│                   │  │                │  │               │
└──────────┬────────┘  └────────────────┘  └───────────────┘
           │
    ┌──────┴──────────────────┬─────────────────┐
    │                         │                 │
┌───▼───────────────┐  ┌──────▼──────┐  ┌──────▼──────┐
│ External APIs     │  │   Database  │  │    Cache    │
│                   │  │             │  │             │
│ - OpenWeather     │  │ PostgreSQL  │  │   Redis     │
│ - GitHub          │  │             │  │             │
│ - OpenAI          │  │ SQLAlchemy  │  │ In-Memory   │
│                   │  │ Models      │  │             │
└───────────────────┘  └─────────────┘  └─────────────┘
```

## Component Architecture

### Core Components

#### 1. **API Layer** (`app/main.py`)
- FastAPI application
- Route definitions
- Exception handlers
- Response formatting

#### 2. **Middleware Stack** (`app/middleware/`)
- Authentication & Authorization
- Rate Limiting
- Security Headers
- Request Logging

#### 3. **Service Layer** (`app/services/`)
- Business logic
- External API integrations
- Caching logic
- Data transformation

#### 4. **Tool Handlers** (`app/tools/`)
- MCP tool implementations
- Input validation
- Execution logic
- Error handling

#### 5. **Resource Providers** (`app/resources/`)
- Static resource data
- Computed resources
- Resource formatting

#### 6. **Prompt Providers** (`app/prompts/`)
- System prompts
- Prompt customization
- Template rendering

#### 7. **Data Layer** (`app/models/`, `app/schemas/`)
- Database models (SQLAlchemy)
- Request/Response schemas (Pydantic)
- Data validation

#### 8. **Configuration** (`app/config/`)
- Environment variable management
- Settings validation
- Configuration loading

#### 9. **Utilities** (`app/utils/`, `app/core/`)
- Helper functions
- Logging utilities
- Exception handling

## Data Flow

### Tool Execution Flow

```
Client Request
    │
    ▼
Middleware (Auth, Rate Limit, Logging)
    │
    ▼
Route Handler (/api/tools/execute)
    │
    ▼
Input Validation (Pydantic Schema)
    │
    ▼
Tool Handler Selection
    │
    ├─ get_weather ──────► WeatherService ──► OpenWeather API
    │
    ├─ github_lookup ────► GitHubService ──► GitHub API
    │
    ├─ summarize_text ──► OpenAIService ──► OpenAI API
    │
    └─ system_status ───► System Utils ──► OS Metrics
    │
    ▼
Cache Check (Redis/In-Memory)
    │
    ▼ (if cached)
Return Cached Result
    │
    └─ (if not cached)
        ▼
        Execute Tool
        │
        ▼
        Transform Result
        │
        ▼
        Cache Result
        │
        ▼
        Return Response
    │
    ▼
Response Formatting
    │
    ▼
Client Response
```

## Request Lifecycle

```
1. Request Received
   └─ Client sends HTTP request to /api/tools/execute

2. Middleware Processing
   ├─ RequestLoggingMiddleware: Log request details
   ├─ SecurityHeadersMiddleware: Add security headers
   ├─ RateLimitMiddleware: Check rate limits
   └─ AuthenticationMiddleware: Validate credentials

3. Route Handler
   ├─ Parse request body
   ├─ Validate input with Pydantic
   └─ Get tool from registry

4. Tool Execution
   ├─ Start timer
   ├─ Check cache
   ├─ If cached, return cached result
   ├─ If not cached:
   │  ├─ Execute tool handler
   │  ├─ Handle errors gracefully
   │  ├─ Cache successful result
   │  └─ Return result
   └─ Stop timer

5. Response Formatting
   ├─ Wrap result in ToolResponse schema
   ├─ Add execution metadata
   └─ Return JSON response

6. Middleware Post-Processing
   └─ Log response details

7. Response Sent to Client
```

## Scalability Considerations

### Horizontal Scaling
- Multiple server instances
- Load balancer (Nginx, HAProxy)
- Stateless design
- Shared cache (Redis)
- Shared database (PostgreSQL)

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize application code
- Database query optimization
- Connection pooling

### Caching Strategy
- Cache API responses (Redis)
- Cache database queries
- Cache tool results with TTL
- Cache invalidation on updates

### Database Optimization
- Connection pooling
- Query optimization
- Index creation
- Sharding (if needed)
- Read replicas

## Security Architecture

### Authentication & Authorization

```
Client Request
    │
    ▼
Extract Auth Header
    │
    ├─ X-API-Key Header
    │  └─ Compare with configured API key
    │
    └─ Authorization: Bearer Header
       └─ Validate bearer token
    │
    ▼
If Valid
├─ Set request.state.authenticated = True
└─ Continue to route handler
    │
    └─ If Invalid
        ├─ Return 401 Unauthorized
        └─ Log authentication failure
```

### Security Layers

1. **Transport Security**
   - HTTPS/SSL encryption
   - Certificate management
   - TLS 1.2+

2. **Application Security**
   - Input validation
   - Output encoding
   - SQL injection prevention
   - XSS protection

3. **API Security**
   - API key authentication
   - Bearer token validation
   - Rate limiting
   - CORS restrictions

4. **Infrastructure Security**
   - Firewall rules
   - Network segmentation
   - VPC isolation
   - Security headers

## Error Handling Architecture

```
Operation Execution
    │
    ├─ Success
    │  └─ Return 200 OK with data
    │
    └─ Error
        │
        ├─ Validation Error
        │  └─ Return 400 Bad Request
        │
        ├─ Authentication Error
        │  └─ Return 401 Unauthorized
        │
        ├─ Authorization Error
        │  └─ Return 403 Forbidden
        │
        ├─ Not Found Error
        │  └─ Return 404 Not Found
        │
        ├─ Rate Limit Error
        │  └─ Return 429 Too Many Requests
        │
        ├─ External API Error
        │  └─ Return 502 Bad Gateway
        │
        ├─ Timeout Error
        │  └─ Return 504 Gateway Timeout
        │
        └─ Unhandled Error
           └─ Return 500 Internal Server Error
               ├─ Log error with context
               └─ Return generic message
```

## Logging Architecture

```
Log Entry Generated
    │
    ▼
JSONFormatter
    │
    ├─ Add timestamp
    ├─ Add log level
    ├─ Add module info
    ├─ Add request ID (if available)
    ├─ Add user ID (if available)
    ├─ Add extra data
    └─ Convert to JSON
    │
    ▼
Handler Distribution
    │
    ├─ Console Handler
    │  └─ Print to stdout
    │
    └─ File Handler
       ├─ Write to file
       └─ Rotate logs (10MB, keep 5 files)
```

## Deployment Architecture

### Local Development
```
Developer Machine
├─ FastAPI (development mode with reload)
├─ SQLite Database
└─ In-Memory Cache
```

### Docker Development
```
Docker Container
├─ FastAPI
├─ PostgreSQL Container
└─ Redis Container
```

### Production Deployment
```
Load Balancer (AWS/GCP)
    │
    ├─ Server Instance 1 (Kubernetes Pod/EC2)
    ├─ Server Instance 2 (Kubernetes Pod/EC2)
    └─ Server Instance N (Kubernetes Pod/EC2)
         │
         └─ All connect to:
            ├─ PostgreSQL (RDS/Managed)
            └─ Redis (ElastiCache/Managed)
```

## Database Schema

```
┌─────────────────────┐
│   api_requests      │
├─────────────────────┤
│ id (UUID)           │
│ timestamp (DateTime)│
│ method (String)     │
│ path (String)       │
│ status_code (Int)   │
│ response_time_ms    │
│ user_id (UUID)      │
│ ip_address (String) │
│ error (Text)        │
└─────────────────────┘

┌─────────────────────┐
│   tool_executions   │
├─────────────────────┤
│ id (UUID)           │
│ tool_name (String)  │
│ status (String)     │
│ input_data (JSON)   │
│ output_data (JSON)  │
│ error (Text)        │
│ execution_time_ms   │
│ created_at (DateTime)
│ user_id (UUID)      │
└─────────────────────┘

┌─────────────────────┐
│   audit_logs        │
├─────────────────────┤
│ id (UUID)           │
│ action (String)     │
│ resource_type (Str) │
│ resource_id (UUID)  │
│ user_id (UUID)      │
│ details (JSON)      │
│ created_at (DateTime)
│ status (String)     │
└─────────────────────┘
```

## API Contract

### Request Format
```json
{
  "tool": "tool_name",
  "input": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

### Response Format
```json
{
  "success": true,
  "result": {
    "data": "response_data"
  },
  "execution_time_ms": 125.5
}
```

### Error Response Format
```json
{
  "error": "ERROR_CODE",
  "message": "Human readable error message",
  "details": {
    "additional": "information"
  }
}
```

## Performance Metrics

### Target Metrics
- API Response Time: < 500ms (p95)
- Database Query Time: < 100ms (p95)
- Cache Hit Rate: > 80%
- Error Rate: < 0.1%
- Availability: 99.9%

### Monitoring
- CPU Usage: < 70%
- Memory Usage: < 80%
- Disk Usage: < 85%
- Network Bandwidth: < 80% capacity
- Request Queue: < 100

---

For implementation details, see the code in the respective modules.
