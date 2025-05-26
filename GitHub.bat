# PowerShell script to initialize Git and upload project to GitHub
# Assumes you have git installed and GitHub CLI configured

cd "C:\Users\ptm\OneDrive\chatGPT RAG"

git init

git add .

git commit -m "Initial commit of Pinecone RAG chatbot project"

# Replace USERNAME and REPO with your GitHub username and desired repository name
gh repo create USERNAME/chatgpt-rag --public --source=. --remote=origin --push
