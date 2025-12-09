# 🚀 FoodSaver Docker Deployment Guide

## Quick Start with Docker

### Option 1: Docker Build & Run (Simple)
```bash
# Build the Docker image
docker build -t foodsaver .

# Run the container
docker run -d -p 5000:5000 --name foodsaver-app foodsaver
```

### Option 2: Docker Compose (Recommended)
```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production:
```env
FLASK_ENV=production
SECRET_KEY=your-super-secure-secret-key-here
DATABASE_URL=sqlite:///data/foodsaver.db
HUGGINGFACE_API_KEY=your-huggingface-api-key
```

### Production Deployment
```bash
# Build for production
docker build -t foodsaver:latest .

# Run with environment file
docker run -d \
  -p 5000:5000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  --name foodsaver-prod \
  foodsaver:latest
```

## 📊 Monitoring

### Check Application Status
```bash
# Check container status
docker ps

# View application logs
docker logs foodsaver-app

# Check health
curl http://localhost:5000/
```

### Container Management
```bash
# Restart container
docker restart foodsaver-app

# Stop container
docker stop foodsaver-app

# Remove container
docker rm foodsaver-app
```

## 🔒 Security Notes

1. **Change SECRET_KEY** - Use a secure random key in production
2. **Database Persistence** - Use volumes for data persistence
3. **Non-root User** - Container runs as non-root user for security
4. **Health Checks** - Built-in health monitoring

## 🌐 Access Your App

Once running, access your FoodSaver app at:
- **Local**: http://localhost:5000
- **Production**: Update port mapping as needed

## 📝 Docker Image Details

- **Base**: Python 3.10.12-slim (lightweight)
- **Web Server**: Gunicorn with 2 workers
- **Security**: Non-root user execution
- **Health**: Built-in health checks
- **Size**: Optimized for minimal image size
