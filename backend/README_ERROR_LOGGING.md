
# Backend Error Logging – Pinecone RAG Chatbot

This logging setup logs all output to:

- `backend.log` file
- Standard console output (Cloud Run or local dev)

## Setup

1. Import the logger in your `app.py`:
   ```python
   from logging_setup import setup_logging
   setup_logging()
   ```

2. Use logging throughout:
   ```python
   import logging
   logging.info("This is an info message.")
   logging.error("This is an error message.")
   ```

3. Customize the log level by setting the `LOG_LEVEL` environment variable:
   ```
   LOG_LEVEL=DEBUG
   ```

## Output

By default, logs are saved to:

- `backend.log` in the app directory
- Streamed to console if deployed to Cloud Run

