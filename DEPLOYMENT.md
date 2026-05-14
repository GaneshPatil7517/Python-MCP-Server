# Deployment Guide

## Local Development

### Setup
```bash
./scripts/setup.sh
source venv/bin/activate
./scripts/start-dev.sh
```

## Docker Deployment

### Single Container
```bash
docker build -t python-mcp-server:latest .
docker run -p 8000:8000 --env-file .env python-mcp-server:latest
```

### Full Stack (with DB & Redis)
```bash
docker-compose up -d
```

## Cloud Deployment

### Railway
1. Push to GitHub
2. Connect repository to Railway
3. Set environment variables
4. Auto-deploy on push

[Railway Docs](https://docs.railway.app)

### Render
1. Create Web Service
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port \$PORT`

[Render Docs](https://render.com/docs)

### AWS EC2

```bash
# SSH into instance
ssh -i key.pem ubuntu@instance-ip

# Clone repository
git clone your-repo
cd python-mcp-server

# Setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Install systemd service
sudo cp deployment/mcp-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

### Heroku
```bash
# Install Heroku CLI
heroku login
heroku create your-app-name
git push heroku main
```

### DigitalOcean

```bash
# Create droplet (Ubuntu 22.04 LTS)
# SSH into droplet
ssh root@droplet-ip

# Setup
apt update && apt upgrade -y
apt install python3.12 python3.12-venv git docker.io docker-compose -y

# Clone and deploy
git clone your-repo
cd python-mcp-server
docker-compose up -d
```

### AWS Lambda (Serverless)

```bash
# Install serverless framework
npm install -g serverless

# Deploy
serverless deploy
```

See `serverless.yml` for configuration.

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (1.24+)
- kubectl configured
- Helm (optional)

### Deploy
```bash
# Create namespace and deploy
kubectl apply -f kubernetes/deployment.yaml

# Check status
kubectl get pods -n mcp-server
kubectl logs -f deployment/mcp-server -n mcp-server

# Access service
kubectl port-forward svc/mcp-server 8000:80 -n mcp-server
```

### With Helm
```bash
# Add Helm repository
helm repo add mcp-server https://your-repo.com
helm repo update

# Install
helm install mcp-server mcp-server/mcp-server \
  --namespace mcp-server \
  --create-namespace \
  --values values.yaml
```

## Monitoring & Logging

### View Logs
```bash
# Docker
docker-compose logs -f mcp-server

# Kubernetes
kubectl logs -f deployment/mcp-server -n mcp-server

# Local
tail -f logs/mcp.log | jq .
```

### Health Checks
```bash
# Manual
curl http://localhost:8000/health

# With script
./scripts/health-check.sh
```

### Metrics
- CPU usage
- Memory usage
- Request count
- Response times
- Error rates

## Security Best Practices

1. **Environment Variables**
   - Never commit `.env`
   - Use `.env.example` for templates
   - Rotate keys regularly

2. **SSL/TLS**
   - Use Let's Encrypt (free)
   - Enable HSTS header
   - Enforce HTTPS

3. **Authentication**
   - Use strong API keys
   - Rotate bearer tokens
   - Enable CORS restrictions

4. **Database**
   - Use strong passwords
   - Enable backups
   - Restrict network access
   - Use encrypted connections

5. **Docker**
   - Use minimal base images
   - Don't run as root
   - Scan for vulnerabilities
   - Keep dependencies updated

## Scaling

### Horizontal Scaling
- Add more server instances
- Use load balancer
- Kubernetes HPA recommended

### Vertical Scaling
- Increase server resources
- Use faster database
- Enable caching (Redis)

### Database Scaling
- Use connection pooling
- Enable read replicas
- Optimize queries
- Archive old data

## Backup & Recovery

### Database Backups
```bash
# PostgreSQL
docker-compose exec postgres pg_dump -U mcp_user mcp_db > backup.sql

# Restore
docker-compose exec -T postgres psql -U mcp_user mcp_db < backup.sql
```

### Automated Backups
```bash
# Backup script
./scripts/backup-database.sh

# Restore
./scripts/restore-database.sh backup.sql
```

## Troubleshooting

### Server won't start
```bash
# Check logs
docker-compose logs mcp-server

# Check port
lsof -i :8000

# Check configuration
python -c "from app.config.settings import get_settings; print(get_settings())"
```

### Database connection error
```bash
# Test connection
docker-compose exec postgres psql -U mcp_user -d mcp_db -c "SELECT 1"
```

### Redis connection error
```bash
# Test connection
docker-compose exec redis redis-cli ping
```

### API not responding
```bash
# Check server status
curl http://localhost:8000/health

# Check recent logs
docker-compose logs --tail 100 mcp-server
```

## Performance Tuning

### Database
- Add indexes
- Use connection pooling
- Enable query caching
- Archive old data

### Application
- Enable Redis caching
- Use async operations
- Implement request batching
- Profile hot paths

### Infrastructure
- Use CDN for static assets
- Enable gzip compression
- Optimize Docker image
- Use faster hardware

## Cost Optimization

- Use spot instances
- Auto-scale based on demand
- Cache frequently accessed data
- Optimize database queries
- Use managed services (RDS, ElastiCache)

## Disaster Recovery

- Regular backups
- Multi-region deployment
- Failover procedures
- Documented recovery steps
- Test recovery regularly

---

For additional support, check README.md or open an issue.
