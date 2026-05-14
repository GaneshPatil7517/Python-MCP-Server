#!/bin/bash
# Deploy script for Railway

echo "🚀 Deploying to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Install from: https://docs.railway.app/cli/installation"
    exit 1
fi

# Login to Railway
railway login

# Create new project
railway init

# Set environment variables
echo "📝 Setting environment variables..."
railway variables set DEBUG=False ENVIRONMENT=production

# Deploy
echo "🚀 Deploying..."
railway up

echo "✅ Deployment complete!"
echo "View your app: railway open"
