#!/bin/bash
# Format code with black and isort

echo "🎨 Formatting code..."

# Install formatters
pip install black isort

# Run isort
echo "Sorting imports..."
isort app tests

# Run black
echo "Formatting with black..."
black app tests

echo "✅ Formatting complete!"
