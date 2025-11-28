FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8503

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8503/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8503", "--server.address=0.0.0.0"]
