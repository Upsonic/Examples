#!/bin/bash
# Docker services setup for fraud detection example

echo "🐳 Setting up Docker services for fraud detection example..."

# Create network for services
docker network create fraud-detection-network 2>/dev/null || echo "Network already exists"

# Start Redis
echo "Starting Redis..."
docker run -d \
  --name fraud-redis \
  --network fraud-detection-network \
  -p 6379:6379 \
  redis:7-alpine

# Start MongoDB
echo "Starting MongoDB..."
docker run -d \
  --name fraud-mongodb \
  --network fraud-detection-network \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  mongo:7

# Start PostgreSQL
echo "Starting PostgreSQL..."
docker run -d \
  --name fraud-postgres \
  --network fraud-detection-network \
  -p 5432:5432 \
  -e POSTGRES_DB=fraud_detection \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  postgres:15

echo "✅ All services started!"
echo ""
echo "Services available at:"
echo "  Redis: localhost:6379"
echo "  MongoDB: localhost:27017"
echo "  PostgreSQL: localhost:5432"
echo ""
echo "To stop services:"
echo "  docker stop fraud-redis fraud-mongodb fraud-postgres"
echo "  docker rm fraud-redis fraud-mongodb fraud-postgres"
echo "  docker network rm fraud-detection-network"
