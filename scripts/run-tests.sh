#!/bin/bash
# Run tests with coverage

echo "🧪 Running tests..."

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

echo ""
echo "✅ Tests complete!"
echo "📊 Coverage report: htmlcov/index.html"
