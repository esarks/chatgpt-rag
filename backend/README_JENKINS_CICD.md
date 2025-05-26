
# Jenkins CI/CD for Pinecone RAG Chatbot

## Pipeline Overview

This Jenkinsfile defines a pipeline that:

1. Installs dependencies
2. Runs linting (optional)
3. Runs tests (placeholder)
4. Builds Docker image
5. Pushes image to GCP Artifact Registry
6. Deploys to Cloud Run

## Setup Instructions

1. Ensure Jenkins agent has Docker and gcloud CLI.
2. Add Google service account JSON as a Jenkins secret:
   - ID: gcp-service-account-key

3. Configure `PROJECT_ID` as a Jenkins environment variable or use `gcloud config`.

4. Connect Jenkins to your GitHub repository and trigger on changes.

## Notes

- Adjust lint/test stages as your project grows.
- Replace `pytest` and `flake8` commands with real test/lint runners.

