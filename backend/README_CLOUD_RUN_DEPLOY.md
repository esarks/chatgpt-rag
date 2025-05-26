
# Deploying Flask Backend to GCP Cloud Run

## Prerequisites

- Google Cloud CLI (`gcloud`) installed
- A GCP project with billing enabled
- Cloud Run and Artifact Registry enabled
- Docker installed locally (optional if not using Cloud Build)

## One-Time Setup

1. Authenticate:
   gcloud auth login

2. Set your GCP project:
   gcloud config set project YOUR_PROJECT_ID

3. Enable required services:
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com

## Build and Deploy with Cloud Build

1. From the backend directory, run:
   gcloud builds submit --config cloudbuild.yaml .

2. Visit your deployed endpoint at:
   https://YOUR_PROJECT_REGION.run.app

**Note:** Cloud Run defaults to port 8080, and the Dockerfile is configured to use gunicorn to serve your Flask app.

