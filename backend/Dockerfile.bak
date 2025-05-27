FROM python:3.10-slim

WORKDIR /app

# Copy the contents of the backend directory into the container
COPY backend /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run expects the app to listen on this port
ENV PORT=8080

CMD ["python", "app.py"]
