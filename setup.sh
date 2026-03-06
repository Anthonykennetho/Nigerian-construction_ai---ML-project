#!/bin/bash

echo "🏗️  Nigerian Construction AI - Setup Script"
echo "==========================================="

echo ""
echo "Step 1: Training ML models..."
docker-compose up train

echo ""
echo "Step 2: Starting services..."
docker-compose up -d api streamlit

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 Services running:"
echo "   - API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Streamlit UI: http://localhost:8501"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs: docker-compose logs -f"
