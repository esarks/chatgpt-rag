import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import pinecone

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
index = pinecone.Index(PINECONE_INDEX)

# Healthcheck endpoint
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    try:
        # Check OpenAI key
        openai.Model.list()

        # Check Pinecone index
        stats = index.describe_index_stats()
        if not stats:
            raise Exception("No index stats returned.")

        return jsonify({"status": "ok", "message": "All systems operational"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Main ask endpoint
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "Missing question"}), 400

        # Get embedding
        embedding = openai.Embedding.create(
            input=[question],
            model="text-embedding-ada-002"
        )["data"][0]["embedding"]

        # Query Pinecone
        search_result = index.query(vector=embedding, top_k=5, include_metadata=True)
        contexts = [match["metadata"].get("text", "") for match in search_result.get("matches", [])]
        context_block = "\n---\n".join(contexts)

        prompt = f"Answer the question based on the context below:\n\nContext:\n{context_block}\n\nQuestion:\n{question}\nAnswer:"

        # Get response
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        answer = completion["choices"][0]["message"]["content"]

        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Entry point for Cloud Run
if __name__ == "__main__":
    print("✅ Environment loaded")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
