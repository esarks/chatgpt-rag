# Uploading Pinecone RAG Chatbot to GitHub

This guide will walk you through uploading your project to GitHub from your local machine.

---

## ✅ Prerequisites

- Git installed (`git --version`)
- GitHub account ([https://github.com](https://github.com))

---

## 🧭 Step-by-Step Instructions

### 1. Create a New Repository

- Visit [https://github.com/new](https://github.com/new)
- Name the repo (e.g., `pinecone-rag-chatbot`)
- Choose Public or Private
- **Do NOT** initialize with README

---

### 2. Organize Your Project Folder Locally

Example structure:

```
pinecone-rag-chatbot/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   ├── cloudbuild.yaml
│   ├── logging_setup.py
│   ├── Jenkinsfile
│   ├── README_JENKINS_CICD.md
│   └── README_ERROR_LOGGING.md
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── ChatWindow.jsx
│   │       ├── FileUpload.jsx
│   ├── firebase.json
│   ├── .firebaserc
│   ├── tailwind.config.js
│   ├── vite.config.js
│   ├── package.json
│   └── README_FIREBASE_DEPLOY.md
├── Pinecone_RAG_Chatbot_Requirements.docx
├── Pinecone_RAG_Deployment_Instructions.md
```

---

### 3. Initialize Git

```bash
cd pinecone-rag-chatbot
git init
git add .
git commit -m "Initial commit - full Pinecone RAG deployment"
```

---

### 4. Link to GitHub Remote

```bash
git remote add origin https://github.com/YOUR_USERNAME/pinecone-rag-chatbot.git
git branch -M main
git push -u origin main
```

---

## ✅ Done

Your full Pinecone RAG chatbot is now uploaded to GitHub.

---

## Optional: Want a .gitignore?

Create a file named `.gitignore` and include:

```
.env
backend.log
node_modules/
dist/
__pycache__/
```

