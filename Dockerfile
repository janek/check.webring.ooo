FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ---------------------------------------------------------------------------
# Install runtime dependencies
# ---------------------------------------------------------------------------
# `names-dataset` is rather large; installing it in a single RUN layer makes
# the final image smaller than using a requirements file with multiple layers.
RUN pip install --no-cache-dir \
    fastapi>=0.115.0 \
    uvicorn[standard]>=0.34.0 \
    names-dataset>=3.3.0

# ---------------------------------------------------------------------------
# Copy application source
# ---------------------------------------------------------------------------
COPY backend/ /app/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 