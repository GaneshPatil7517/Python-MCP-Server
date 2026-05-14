# Troubleshooting Guide

## Common Issues & Solutions

### 1. Port Already in Use

**Error:** `Address already in use`

**Solutions:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
PORT=8001 python -m uvicorn app.main:app --reload
```

---

### 2. API Key Not Working

**Error:** `Authentication failed` or `Invalid API key`

**Solutions:**
```bash
# Verify .env is loaded
python -c "from app.config.settings import get_settings; s = get_settings(); print(f'API Key: {s.api_key}')"

# Check if ENABLE_AUTH=False in .env
grep ENABLE_AUTH .env

# Try without authentication (development only)
curl -H "X-API-Key: any-key" http://localhost:8000/api/tools
```

---

### 3. Database Connection Error

**Error:** `Could not connect to database` or `Connection refused`

**For Docker:**
```bash
# Check if postgres is running
docker-compose ps postgres

# View postgres logs
docker-compose logs postgres

# Restart postgres
docker-compose restart postgres

# Check connection
docker-compose exec postgres psql -U mcp_user -d mcp_db -c "SELECT 1"
```

**For Local PostgreSQL:**
```bash
# Check if PostgreSQL service is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql

# Test connection
psql -U postgres -h localhost -d mcp_db -c "SELECT 1"
```

---

### 4. Redis Connection Error

**Error:** `ConnectionRefusedError` or `Redis connection failed`

**Solutions:**
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server

# Or with Docker
docker-compose restart redis

# Test connection
docker-compose exec redis redis-cli ping
```

---

### 5. Weather API Not Working

**Error:** `API request failed` or `Invalid API key`

**Solutions:**
```bash
# Check if API key is set
grep WEATHER_API_KEY .env

# Get free API key from OpenWeatherMap
# https://openweathermap.org/api

# Update .env
WEATHER_API_KEY=your-api-key-here

# Test manually
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY"
```

---

### 6. GitHub API Rate Limit

**Error:** `API error` or `422 response`

**Solutions:**
```bash
# Use GitHub token for higher limits
grep GITHUB_TOKEN .env

# Get token from https://github.com/settings/tokens

# Update .env
GITHUB_TOKEN=ghp_xxxxx

# Check current rate limit
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/rate_limit
```

---

### 7. OpenAI API Not Working

**Error:** `OpenAI API error` or `Invalid API key`

**Solutions:**
```bash
# Check if API key is set
grep OPENAI_API_KEY .env

# Get API key from https://platform.openai.com/api-keys

# Update .env
OPENAI_API_KEY=sk-xxxxxx

# Verify API key format (should start with sk-)
python -c "from app.config.settings import get_settings; print(get_settings().openai_api_key[:10])"
```

---

### 8. Import Errors

**Error:** `ModuleNotFoundError` or `ImportError`

**Solutions:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

---

### 9. Hot Reload Not Working

**Error:** Server doesn't restart on file changes

**Solutions:**
```bash
# Make sure using --reload flag
python -m uvicorn app.main:app --reload

# Check DEBUG mode
grep DEBUG .env

# Verify file is being saved
ls -la app/main.py
```

---

### 10. Docker Build Fails

**Error:** `docker build` fails with various errors

**Solutions:**
```bash
# Check Docker installation
docker --version

# Clean up
docker system prune -a

# Build with no cache
docker build --no-cache -t python-mcp-server:latest .

# Check Dockerfile
docker build --progress=plain -t python-mcp-server:latest .

# View full build logs
docker build -vv -t python-mcp-server:latest .
```

---

### 11. Docker Compose Fails

**Error:** `docker-compose up` fails

**Solutions:**
```bash
# Check docker-compose installation
docker-compose --version

# Validate compose file
docker-compose config

# Check .env file exists
ls -la .env

# Pull latest images
docker-compose pull

# Rebuild containers
docker-compose up --build

# Check service status
docker-compose ps

# View logs for specific service
docker-compose logs mcp-server
```

---

### 12. CORS Errors

**Error:** `CORS policy: Cross-Origin Request Blocked`

**Solutions:**
```bash
# Check CORS settings in .env
grep CORS_ORIGINS .env

# For development, allow all origins
CORS_ORIGINS=["*"]

# For production, specify domains
CORS_ORIGINS=["https://example.com", "https://app.example.com"]

# Check headers in response
curl -i -H "Origin: http://localhost:3000" http://localhost:8000/api/tools
```

---

### 13. Rate Limiting Issues

**Error:** `Rate limit exceeded` or `429 Too Many Requests`

**Solutions:**
```bash
# Disable rate limiting temporarily
RATE_LIMIT_ENABLED=False

# Increase rate limit
RATE_LIMIT_REQUESTS_PER_MINUTE=120

# Check which IP is rate limited
grep "Rate limit" logs/mcp.log | tail -20

# Reset rate limiter
# (rate limiter is in-memory and resets on restart)
```

---

### 14. Memory Usage High

**Error:** High memory consumption or OOM kills

**Solutions:**
```bash
# Check memory usage
ps aux | grep uvicorn

# Monitor in real-time
top -p $(pgrep -f uvicorn)

# Set memory limits (Docker)
docker-compose up --memory 512m mcp-server

# Enable caching to reduce database queries
CACHE_ENABLED=True
CACHE_TTL=3600

# Check for memory leaks in logs
grep -i "memory" logs/mcp.log
```

---

### 15. Slow Requests

**Error:** Request taking too long or timing out

**Solutions:**
```bash
# Increase timeout
HTTP_TIMEOUT=60
API_CALL_TIMEOUT=120

# Enable caching
CACHE_ENABLED=True

# Check external API response times
curl -w "@curl-format.txt" https://api.github.com/users/torvalds

# Profile application
pip install py-spy
py-spy record -o profile.svg -- python -m uvicorn app.main:app
```

---

## Debug Mode

### Enable Debug Logging

```bash
# Set debug environment
DEBUG=True
LOG_LEVEL=DEBUG

# View detailed logs
tail -f logs/mcp.log | jq .
```

### Test Specific Endpoint

```bash
# Test with verbose output
curl -v http://localhost:8000/api/tools

# With authentication
curl -v -H "X-API-Key: test-key" http://localhost:8000/api/tools

# POST request
curl -v -X POST http://localhost:8000/api/tools/execute \
  -H "Content-Type: application/json" \
  -d '{"tool":"get_weather","input":{"city":"London"}}'
```

### Check Configuration

```bash
# Print all configuration
python -c "from app.config.settings import get_settings; import json; s = get_settings(); print(json.dumps(s.dict(), indent=2))"

# Check specific setting
python -c "from app.config.settings import get_settings; print(get_settings().database_url)"
```

---

## Performance Debugging

### Check Request Times

```bash
# View processing times in logs
grep "execute in" logs/mcp.log | tail -20

# Find slow requests
grep '"process_time_ms"' logs/mcp.log | jq .process_time_ms | sort -rn | head -10
```

### Database Query Performance

```bash
# Enable PostgreSQL logging
docker-compose exec postgres psql -U mcp_user -c "SET log_statement = 'all';"

# View slow queries
docker-compose logs postgres | grep "duration:"
```

### Network Performance

```bash
# Test API response time
time curl http://localhost:8000/api/tools

# Measure with curl
curl -w "Total time: %{time_total}s\n" http://localhost:8000/api/tools

# Load test with Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health
```

---

## Health Check

```bash
# Run comprehensive health check
./scripts/health-check.sh

# Manual health check
curl http://localhost:8000/health

# Check all services
curl http://localhost:8000/api/status
```

---

## Getting Help

1. Check logs: `docker-compose logs -f`
2. Check this guide
3. Run health check: `./scripts/health-check.sh`
4. Enable debug logging: `LOG_LEVEL=DEBUG`
5. Open GitHub issue with:
   - Error message
   - Logs (sanitized)
   - Configuration (sanitized)
   - Steps to reproduce

---

## Contact & Support

- GitHub Issues: Report bugs and request features
- Documentation: Check README.md and EXTENDING.md
- Community: Discuss with other users
