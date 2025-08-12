# ===========================
# Stage 1: Builder
# ===========================
FROM python:3.9-slim AS builder

WORKDIR /app

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# ===========================
# Stage 2: Runtime
# ===========================
FROM python:3.9-slim

WORKDIR /app

# Install only the runtime dependencies needed for TensorFlow to work with HDF5
RUN apt-get update && apt-get install -y --no-install-recommends \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source code
COPY . .
RUN python train_dummy_model.py

EXPOSE 8000

CMD ["python", "app.py"]
