
#!/bin/bash

cd ~/chatgpt-rag/backend || exit 1

# ✅ Authenticate if not already
if ! gcloud auth list --format=json | grep -q 'ACTIVE'; then
  echo "🔐 You need to log in to your Google account..."
  gcloud auth login
fi

# ✅ Set project ID
PROJECT_ID=pinecone-rag-chatbot
IMAGE_NAME=pinecone-rag-backend
REGION=us-central1

# Replace these with your real environment values
OPENAI_API_KEY="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"
PINECONE_API_KEY="pcsk_4n3j9n_DrU9bZFidVvc2GDdzVxBdUJ1ugnZfycqqQAHeafWxKE1ZMcYaZ2Kz31ZKhqZGPo"
PINECONE_INDEX="rag-index"
PINECONE_ENVIRONMENT="us-east-1"

# ✅ Submit Docker image
gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME

# ✅ Deploy to Cloud Run
gcloud run deploy $IMAGE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY,PINECONE_API_KEY=$PINECONE_API_KEY,PINECONE_INDEX=$PINECONE_INDEX,PINECONE_ENVIRONMENT=$PINECONE_ENVIRONMENT
