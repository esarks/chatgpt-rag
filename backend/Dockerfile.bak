# Dockerfile for deploying your Flask + Pinecone RAG backend on Cloud Run
FROM python:3.10-slim

# Create app directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Cloud Run expects
ENV PORT=8080

# Run the application
CMD ["python", "app.py"]
