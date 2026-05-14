#!/bin/bash
# Build and push Docker image

echo "🐳 Building Docker image..."

# Variables
IMAGE_NAME="python-mcp-server"
IMAGE_TAG="latest"
REGISTRY="${REGISTRY:-}"  # Set to your registry (e.g., docker.io/username)

# Build image
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

if [ $? -eq 0 ]; then
    echo "✅ Image built successfully!"
    echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
    
    # Push if registry provided
    if [ -n "$REGISTRY" ]; then
        echo "📤 Pushing to registry: $REGISTRY"
        docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
        docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
        echo "✅ Image pushed!"
    else
        echo "💡 To push to registry, set REGISTRY env variable:"
        echo "   export REGISTRY=docker.io/username"
        echo "   ./scripts/docker-build.sh"
    fi
else
    echo "❌ Build failed!"
    exit 1
fi
