# Pinecone RAG Chatbot – Full Deployment Guide

This document outlines how to deploy the Pinecone RAG chatbot using:

- GitHub (for source code repo)
- OpenAI (for embeddings + completions)
- Pinecone (for vector storage and retrieval)
- Google Cloud Platform (Cloud Run for backend + Firebase for frontend)
- Environment configuration (.env)

---

## ✅ Step 1: Set Up Your Accounts

### 1.1 GitHub
- Create a GitHub repository (e.g., `pinecone-rag-chatbot`)
- Upload all backend and frontend code to it

### 1.2 OpenAI
- Create an OpenAI account: https://platform.openai.com/
- Generate an API key from your account dashboard

### 1.3 Pinecone
- Create a Pinecone account: https://www.pinecone.io/start/
- Set up:
  - Index name (e.g., `rag-index`)
  - Environment (e.g., `us-west1-gcp`)
  - API Key from dashboard

### 1.4 Google Cloud Platform (GCP)
- Create a GCP project
- Enable:
  - Cloud Run
  - Artifact Registry
  - Cloud Build
  - Firebase Hosting (through https://console.firebase.google.com/)

---

## ✅ Step 2: Environment Configuration

Create a `.env` file inside your backend folder using this template:

```env
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=your-pinecone-region
PINECONE_INDEX=your-index-name
LOG_LEVEL=INFO
```

You may also define:
- `PROJECT_ID=your-gcp-project-id` (for Jenkins or Cloud Build)
- `PORT=8080` (optional for local debugging)

---

## ✅ Step 3: Deploy the Backend to Cloud Run

### 3.1 Local Docker Build (optional)
```bash
docker build -t gcr.io/YOUR_PROJECT_ID/pinecone-rag-backend .
docker push gcr.io/YOUR_PROJECT_ID/pinecone-rag-backend
```

### 3.2 Cloud Build Deploy (recommended)
```bash
gcloud builds submit --config cloudbuild.yaml .
```

This will:
- Build a Docker image
- Push it to Artifact Registry
- Deploy to Cloud Run

---

## ✅ Step 4: Deploy Frontend to Firebase Hosting

### 4.1 Build the Frontend
```bash
npm install
npm run build
```

### 4.2 Initialize Firebase Hosting
```bash
firebase login
firebase init hosting
```

- Set public directory to `dist`
- Choose single-page app = yes

### 4.3 Deploy
```bash
firebase deploy
```

---

## ✅ Step 5: CI/CD via Jenkins (Optional)

Use the provided `Jenkinsfile`. You must:
- Store your GCP service account as a secret
- Use a Jenkins agent with Docker + gcloud CLI installed

---

## ✅ Step 6: Verify

- Test file uploads at: `http://<CLOUD_RUN_URL>/upload`
- Test chat at: `https://<FIREBASE_URL>`
- View logs with:
  ```bash
  gcloud logging read "resource.type=cloud_run_revision" --limit=20
  ```

---

## ✅ Summary

| Component     | Provider       | Where Configured         |
|---------------|----------------|---------------------------|
| Embeddings    | OpenAI         | `.env` → `OPENAI_API_KEY` |
| Vector DB     | Pinecone       | `.env` → PINECONE_*       |
| Backend API   | Cloud Run (GCP)| `cloudbuild.yaml`         |
| Frontend UI   | Firebase       | `firebase.json`, `dist/`  |
| Secrets       | `.env` file    | Root of backend folder    |
| CI/CD         | Jenkins (opt)  | `Jenkinsfile`             |

--- 

For any frontend-to-backend request in dev mode, ensure:
```js
// vite.config.js
server: {
  proxy: {
    '/ask': 'http://localhost:5000',
    '/upload': 'http://localhost:5000',
    '/stream': 'http://localhost:5000'
  }
}
```

And that’s it — your full stack Pinecone RAG chatbot is live.

