FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if any are needed
# RUN apt-get update && apt-get install -y --no-install-recommends ...

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

# Expose the port for SSE mode
EXPOSE 8000

# Run in SSE mode by default
ENTRYPOINT ["python", "server.py", "--transport", "sse", "--port", "8000"]
