
# Firebase Hosting for Pinecone RAG Chatbot (Frontend)

## Setup Instructions

1. Install Firebase CLI (if not already installed):
   npm install -g firebase-tools

2. Login to Firebase:
   firebase login

3. Initialize Firebase in the frontend directory:
   firebase init hosting
   (Use "dist" as the public directory and configure as a single-page app)

4. Build the project:
   npm run build

5. Deploy to Firebase:
   firebase deploy

Your chatbot frontend will be live at the Firebase Hosting URL.
