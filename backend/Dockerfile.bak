# Use slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy source code and install dependencies
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Set the port for Cloud Run
EXPOSE 8080

# Start the app
CMD ["python", "app.py"]
