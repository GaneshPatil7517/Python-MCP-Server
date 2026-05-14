#!/bin/bash
# Lint code with flake8, mypy, and pylint

echo "🔍 Linting code..."

# Install linters
pip install flake8 mypy pylint black

echo ""
echo "Running flake8..."
flake8 app tests --max-line-length=100 --ignore=E203,W503

echo ""
echo "Running black check..."
black --check app tests

echo ""
echo "Running mypy..."
mypy app --ignore-missing-imports || true

echo ""
echo "Running pylint..."
pylint app --disable=all --enable=F,E --exit-zero

echo ""
echo "✅ Linting complete!"
