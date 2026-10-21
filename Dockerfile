# ==============================================================================
# Multi-Stage Production Dockerfile for Cars Dealership Full-Stack Capstone
# Stage 1: Build React Frontend Application
# ==============================================================================
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# ==============================================================================
# Stage 2: Python / Django Production Runtime
# ==============================================================================
FROM python:3.13-slim AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Source Code
COPY manage.py .
COPY server/ server/
COPY data/ data/
COPY scripts/ scripts/

# Copy Built Frontend Distribution from Stage 1
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Run Database Migrations and Seed Data during build/startup
RUN python manage.py migrate --noinput && \
    python manage.py seed_dealerships

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/api/dealers/ || exit 1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
