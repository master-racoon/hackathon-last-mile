# Platform Support

This FastAPI service is configured to automatically build for the correct platform (ARM64 for Apple Silicon Macs, AMD64 for Intel/Windows).

## How it Works

The Dockerfiles now use the official multi-architecture Python images:

- `python:3.11-slim` - Automatically pulls the correct architecture for your system

Docker automatically detects your platform and pulls the appropriate image:

- **Apple Silicon Macs (M1/M2/M3)**: Uses ARM64 (linux/arm64)
- **Intel Macs / Windows**: Uses AMD64 (linux/amd64)

## Building

No special flags are needed - Docker automatically detects your platform:

```bash
# Development
docker-compose up --build backend

# Production
docker build -f Dockerfile.prod -t lastmile-api:latest .
```

## Manual Platform Override (if needed)

If you need to build for a specific platform:

```bash
# Force ARM64 (Apple Silicon)
docker build --platform linux/arm64 -f Dockerfile.dev -t lastmile-api:dev .

# Force AMD64 (Intel/Windows)
docker build --platform linux/amd64 -f Dockerfile.dev -t lastmile-api:dev .
```

## Troubleshooting

If you encounter platform-related issues:

1. **Check your Docker version**: Ensure you're using Docker Desktop 20.10+ which has better multi-platform support
2. **Clear build cache**: `docker builder prune -a`
3. **Rebuild from scratch**: `docker-compose build --no-cache backend`

## Notes

- The production Dockerfile (`Dockerfile.prod`) also supports multi-platform builds
- PostgreSQL and Node.js images used in docker-compose are already multi-platform compatible
- The ML training service Python image is also multi-platform compatible
