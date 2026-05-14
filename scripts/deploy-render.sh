#!/bin/bash
# Deploy script for Render

echo "🚀 Deploying to Render..."

echo "1. Create new Web Service on Render.com"
echo "2. Connect GitHub repository"
echo "3. Set environment variables:"
echo "   - DEBUG=False"
echo "   - ENVIRONMENT=production"
echo "   - DATABASE_URL=postgresql://..."
echo "   - REDIS_URL=redis://..."
echo ""
echo "4. Set build command:"
echo "   pip install -r requirements.txt"
echo ""
echo "5. Set start command:"
echo "   python -m uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "✅ Render will auto-deploy on git push to main"
