#!/bin/bash
# Setup script for Text-to-Speech CLI on Mac M3

echo "Setting up Text-to-Speech CLI..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install it first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "Creating virtual environment with uv..."
uv venv

echo "Installing dependencies..."
uv pip install -e .

# For Mac M3, we need to ensure PyTorch uses MPS backend
echo ""
echo "Verifying PyTorch MPS support for Mac M3..."
uv run python -c "import torch; print(f'MPS available: {torch.backends.mps.is_available()}')"

echo ""
echo "✓ Setup complete!"
echo ""
echo "To use the CLI:"
echo "  1. Activate the environment: source .venv/bin/activate"
echo "  2. Run: text2speech \"Your text here\""
echo ""
echo "Or use directly with uv:"
echo "  uv run text2speech \"Your text here\""
