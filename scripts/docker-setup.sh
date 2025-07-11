#!/bin/bash

# Docker Setup Script for iGoUltra Backend
echo "🐳 Setting up iGoUltra Backend with Docker..."

# Build the images
echo "📦 Building Docker images..."
docker-compose build

# Start the services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser (optional)
echo "👤 Creating superuser..."
docker-compose exec web python manage.py createsuperuser --noinput || echo "Superuser creation skipped (already exists or interactive mode needed)"

# Load initial data (layers)
echo "📊 Loading initial data..."
docker-compose exec web python manage.py loaddata layers/fixtures/layers.json

# Initialize user layer progress
echo "🎯 Initializing user layer progress..."
docker-compose exec web python manage.py init_user_layer_progress

echo "✅ Setup complete!"
echo "🌐 Django admin: http://localhost:8000/admin"
echo "📚 API docs: http://localhost:8000/api/schema/swagger-ui/"
echo ""
echo "To stop the services: docker-compose down"
echo "To view logs: docker-compose logs -f" 