#!/bin/bash
# Health check and monitoring script

echo "🏥 MCP Server Health Check"
echo "========================="
echo ""

# Check if server is running
echo "🔍 Checking server status..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$RESPONSE" = "200" ]; then
    echo "✅ Server is running (HTTP $RESPONSE)"
else
    echo "❌ Server is not responding (HTTP $RESPONSE)"
    exit 1
fi

# Check database
echo ""
echo "🔍 Checking database..."
curl -s http://localhost:8000/api/resources/server_status | jq .

# Check API endpoints
echo ""
echo "🔍 Checking API endpoints..."

endpoints=(
    "/api/tools"
    "/api/resources"
    "/api/prompts"
    "/api/status"
)

for endpoint in "${endpoints[@]}"; do
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000$endpoint)
    if [ "$response" = "200" ]; then
        echo "✅ $endpoint ($response)"
    else
        echo "❌ $endpoint ($response)"
    fi
done

echo ""
echo "✅ Health check complete!"
