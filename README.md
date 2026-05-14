# Python MCP Server

A production-ready, scalable **Model Context Protocol (MCP) server** built with **FastAPI** and **Python 3.12+**. Deploy on Claude Desktop, Cursor, VS Code, and other MCP-compatible clients.



## Features

### MCP Components
- **MCP Tools** - Weather lookup, GitHub user search, text summarization, system status
- **MCP Resources** - API documentation, server status, project info, usage guides
- **MCP Prompts** - Debugging assistant, code review, architecture explanation, API docs

### Core Features
- **Async Execution** - Non-blocking async/await throughout
- **Structured Logging** - JSON logging with request tracking
- **Error Handling** - Centralized exception handling with custom error codes
- **Authentication** - API Key and Bearer token authentication
- **Rate Limiting** - Configurable rate limiting per minute/hour
- **Caching** - In-memory and Redis-based caching
- **Validation** - Pydantic schemas for all inputs/outputs
- **Security** - CORS, security headers, input sanitization

### DevOps & Deployment
- **Docker** - Multi-stage Dockerfile with optimization
- **Docker Compose** - PostgreSQL, Redis, and MCP server
- **CI/CD** - GitHub Actions workflow
- **Testing** - Unit and integration tests with pytest
- **Health Checks** - Built-in health monitoring



## Project Structure


python-mcp-server/
├── app/
│   ├── core/                 # Core utilities
│   │   ├── exceptions.py     # Custom exceptions
│   │   └── logging_config.py # Logging setup
│   ├── config/
│   │   └── settings.py       # Configuration management
│   ├── schemas/              # Pydantic schemas
│   │   ├── tools.py
│   │   ├── resources.py
│   │   └── prompts.py
│   ├── models/
│   │   └── database.py       # SQLAlchemy models
│   ├── services/             # Business logic
│   │   ├── external_apis.py
│   │   └── cache.py
│   ├── middleware/
│   │   └── auth.py           # Auth & security middleware
│   ├── tools/
│   │   └── implementations.py # All MCP tools
│   ├── resources/
│   │   └── implementations.py # All MCP resources
│   ├── prompts/
│   │   └── implementations.py # All MCP prompts
│   ├── utils/
│   │   └── helpers.py        # Utility functions
│   └── main.py               # FastAPI app entry point
├── tests/
│   ├── unit/                 # Unit tests
│   │   ├── test_tools.py
│   │   ├── test_cache.py
│   │   └── test_schemas.py
│   ├── integration/          # Integration tests
│   │   └── test_api.py
│   └── conftest.py
├── docker/                   # Docker configs
├── scripts/                  # Helper scripts
│   ├── setup.sh
│   ├── start-dev.sh
│   └── run-tests.sh
├── .github/workflows/        # CI/CD
│   └── ci-cd.yml
├── Dockerfile                # Production container
├── docker-compose.yml        # Full stack with DB & Redis
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```


## Quick Start

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (optional, for containerized deployment)
- API keys for integrations (OpenWeather, GitHub, OpenAI - optional)

### Local Development

1. **Clone and setup:**
   ```bash
   cd python-mcp-server
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Start development server:**
   ```bash
   ./scripts/start-dev.sh
   ```
   Server runs at `http://localhost:8000`

5. **Access documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - OpenAPI: http://localhost:8000/openapi.json



## Docker Deployment

### With Docker Compose (Recommended)

```bash
# Start all services (MCP server, PostgreSQL, Redis)
docker-compose up -d

# View logs
docker-compose logs -f mcp-server

# Stop services
docker-compose down
```

Services:
- MCP Server: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### With Docker Only

```bash
# Build image
docker build -t python-mcp-server:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name mcp-server \
  python-mcp-server:latest

# View logs
docker logs -f mcp-server
```

---

## Configuration

### Environment Variables

```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False
ENVIRONMENT=production

# API Keys
OPENAI_API_KEY=sk-xxx
WEATHER_API_KEY=xxx
GITHUB_TOKEN=ghp_xxx

# Security
SECRET_KEY=your-secret-key
API_KEY=your-api-key
BEARER_TOKEN=your-bearer-token
ENABLE_AUTH=True

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS_PER_MINUTE=60

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/mcp_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_JSON=True
```

---

## MCP Tools

### 1. Get Weather

Fetch weather information for any city.

**Input:**
```json
{
  "city": "London",
  "unit": "metric"
}
```

**Output:**
```json
{
  "success": true,
  "data": {
    "city": "London",
    "temperature": 15.0,
    "humidity": 65,
    "description": "Partly cloudy",
    ...
  }
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/tools/execute \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_weather",
    "input": {"city": "London"}
  }'
```

### 2. GitHub User Lookup

Search GitHub users and repositories.

**Input:**
```json
{
  "username": "torvalds",
  "include_repos": true
}
```

**Output:**
```json
{
  "success": true,
  "data": {
    "username": "torvalds",
    "followers": 200000,
    "repositories": [...]
  }
}
```

### 3. Summarize Text

Summarize text using OpenAI or fallback summarization.

**Input:**
```json
{
  "text": "Long text here...",
  "max_length": 100
}
```

**Output:**
```json
{
  "success": true,
  "summary": "Summary text...",
  "original_length": 5000,
  "summary_length": 80
}
```

### 4. System Status

Get real-time system metrics.

**Output:**
```json
{
  "success": true,
  "data": {
    "cpu_percent": 45.2,
    "memory_percent": 60.5,
    "memory_available_gb": 3.2,
    "uptime_seconds": 86400
  }
}
```


## MCP Resources

Access read-only resources:

```bash
# List all resources
curl http://localhost:8000/api/resources

# Get specific resource
curl http://localhost:8000/api/resources/api_documentation
curl http://localhost:8000/api/resources/server_status
curl http://localhost:8000/api/resources/project_information
curl http://localhost:8000/api/resources/usage_guide
curl http://localhost:8000/api/resources/tools_list
```



## MCP Prompts

Use predefined system prompts for AI assistants:

```bash
# List all prompts
curl http://localhost:8000/api/prompts

# Get specific prompt
curl http://localhost:8000/api/prompts/debugging-assistant
curl http://localhost:8000/api/prompts/code-review-assistant
curl http://localhost:8000/api/prompts/architecture-explanation
curl http://localhost:8000/api/prompts/api-documentation
```


## Authentication

### API Key (Recommended)

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/tools
```

### Bearer Token

```bash
curl -H "Authorization: Bearer your-token" http://localhost:8000/api/tools
```

### Disable Authentication

Set `ENABLE_AUTH=False` in `.env` (development only).



## Testing

Run all tests:
```bash
./scripts/run-tests.sh
```

Run specific tests:
```bash
pytest tests/unit/test_tools.py -v
pytest tests/integration/test_api.py -v
```

Coverage report:
```bash
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

## Error Handling

All errors follow consistent format:

```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid input provided",
  "details": {
    "field": "city",
    "reason": "required"
  }
}
```

**Error Codes:**
- `VALIDATION_ERROR` (400) - Invalid input
- `AUTHENTICATION_ERROR` (401) - Auth failed
- `AUTHORIZATION_ERROR` (403) - Insufficient permissions
- `NOT_FOUND` (404) - Resource not found
- `RATE_LIMIT_EXCEEDED` (429) - Rate limited
- `API_ERROR` (502) - External API failed
- `TIMEOUT` (504) - Operation timed out
- `INTERNAL_ERROR` (500) - Server error


## Performance & Caching

### Enable Caching

```env
CACHE_ENABLED=True
CACHE_TTL=3600
REDIS_URL=redis://localhost:6379/0
```

### Monitoring

Check server status:
```bash
curl http://localhost:8000/api/status
```

Health check:
```bash
curl http://localhost:8000/health
```


## Claude Desktop Integration

### macOS Setup

1. Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "python-mcp-server": {
      "command": "python",
      "args": ["/path/to/mcp/app/main.py"],
      "env": {
        "OPENAI_API_KEY": "sk-xxx",
        "WEATHER_API_KEY": "xxx",
        "GITHUB_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

2. Restart Claude Desktop

### Linux Setup

Edit `~/.config/Claude/claude_desktop_config.json` (same config as macOS).

### Windows Setup

Edit `%APPDATA%\Claude\claude_desktop_config.json` (same config as macOS).

---

## Cursor Integration

1. Open Cursor settings
2. Go to Features → MCP
3. Add new MCP server:

```json
{
  "name": "Python MCP Server",
  "command": "python",
  "args": ["/path/to/app/main.py"],
  "env": {}
}
```

## Deployment

### Railway

1. Push to GitHub
2. Connect repository to Railway
3. Set environment variables
4. Deploy

### Render

1. Push to GitHub
2. Create new Web Service
3. Connect GitHub repo
4. Set environment variables
5. Deploy

### AWS EC2

```bash
# SSH into instance
ssh -i key.pem ec2-user@instance-ip

# Clone repo
git clone your-repo
cd python-mcp-server

# Setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Start with systemd
sudo nano /etc/systemd/system/mcp-server.service
```

```ini
[Unit]
Description=Python MCP Server
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/python-mcp-server
ExecStart=/home/ec2-user/python-mcp-server/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

### Docker Swarm / Kubernetes

**docker-compose.yml** is compatible with Docker Swarm.

For Kubernetes, create deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: python-mcp-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: database-url
```

---

## 🔍 Logging

### Structured Logging

All logs are structured JSON for easy parsing:

```json
{
  "timestamp": "2024-01-01T00:00:00.000000",
  "level": "INFO",
  "message": "Tool executed successfully",
  "module": "tools",
  "function": "execute",
  "extra": {
    "tool_name": "get_weather",
    "execution_time_ms": 125.5
  }
}
```

### Log Levels

```bash
# Set in .env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### View Logs

```bash
# In Docker
docker-compose logs -f mcp-server

# In terminal
tail -f logs/mcp.log | jq .
```

---

## 🛣️ Development Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Streaming responses for large data
- [ ] PostgreSQL migrations with Alembic
- [ ] JWT authentication
- [ ] OAuth2 integration
- [ ] Celery background tasks
- [ ] Kafka event streaming
- [ ] Monitoring dashboard (Prometheus/Grafana)
- [ ] Advanced caching strategies
- [ ] Multi-region deployment
- [ ] GraphQL endpoint


## Security Considerations

1. **Never commit .env** - Use `.env.example` only
2. **Rotate API Keys** - Regularly update secrets
3. **Use HTTPS** - Enable SSL in production
4. **Rate Limiting** - Adjust limits per your needs
5. **CORS** - Restrict origins in production
6. **Authentication** - Always enable in production
7. **Input Validation** - All inputs validated with Pydantic
8. **Logging** - No sensitive data in logs
9. **Dependencies** - Regularly update packages
10. **Docker** - Run as non-root user

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes and tests
4. Run tests: `./scripts/run-tests.sh`
5. Submit pull request


## API Documentation

Complete API documentation available at `/docs` (Swagger UI) or `/redoc` (ReDoc).


## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Database Connection Error
```bash
# Check PostgreSQL
docker-compose ps
docker-compose logs postgres
```

### Redis Connection Failed
```bash
# Check Redis
docker-compose exec redis redis-cli ping
```

### API Keys Not Working
```bash
# Verify .env is loaded
python -c "from app.config.settings import get_settings; print(get_settings().openai_api_key)"
```

---

## License

MIT License - See LICENSE file


## Author

Created as a production-ready MCP server template for AI integration.

Heartly welcome for Contributers....
