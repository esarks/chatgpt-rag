import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import openai

# Load environment variables
load_dotenv()
print("✅ dotenv loaded")

# Initialize Flask app
app = Flask(__name__)
CORS(app)
print("💡 Starting app.py...")

# Load API keys and config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

# Debug environment variable loading
print(f"🔑 OPENAI_API_KEY set: {'Yes' if OPENAI_API_KEY else 'No'}")
print(f"🔑 PINECONE_API_KEY set: {'Yes' if PINECONE_API_KEY else 'No'}")
print(f"🌍 PINECONE_ENVIRONMENT: {PINECONE_ENVIRONMENT}")
print(f"📚 PINECONE_INDEX: {PINECONE_INDEX}")

# Set up OpenAI
openai.api_key = OPENAI_API_KEY

# Set up Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
index = pc.Index(PINECONE_INDEX)
print(f"📦 Pinecone index '{PINECONE_INDEX}' ready.")

# Healthcheck endpoint
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    try:
        openai.Model.list()
        pc.list_indexes()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500

# Main chat endpoint
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "No question provided."}), 400

        # Embed question using OpenAI
        embedding_response = openai.Embedding.create(
            input=[question],
            model="text-embedding-ada-002"
        )
        embedding = embedding_response["data"][0]["embedding"]

        # Query Pinecone index
        results = index.query(vector=embedding, top_k=5, include_metadata=True)

        # Build context
        context = "\n".join([match["metadata"].get("text", "") for match in results["matches"]])

        # Use GPT to answer
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Answer the question based on the context below."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
            ]
        )
        answer = completion["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Needed for gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
