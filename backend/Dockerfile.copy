# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (optional but useful for local testing)
EXPOSE 8080

# Set environment variable
ENV PORT=8080

# Command to run the app
CMD ["python", "app.py"]
