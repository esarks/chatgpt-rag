import os
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import pinecone

# Load .env if available (local dev)
load_dotenv()

# Initialize environment variables
try:
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    PINECONE_ENVIRONMENT = os.environ["PINECONE_ENVIRONMENT"]
    PINECONE_INDEX = os.environ["PINECONE_INDEX"]
except KeyError as e:
    raise RuntimeError(f"Missing required environment variable: {e}")

openai.api_key = OPENAI_API_KEY

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
index = pinecone.Index(PINECONE_INDEX)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "running", "source": "Pinecone RAG backend"})

def get_context_from_pinecone(query, top_k=5):
    embedding = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )["data"][0]["embedding"]

    results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    
    context = ""
    sources = set()
    for match in results.get("matches", []):
        metadata = match.get("metadata", {})
        text = metadata.get("text", "")
        source = metadata.get("source", "unknown")
        context += f"\nSource: {source}\n{text}\n"
        sources.add(source)
    
    return context.strip(), list(sources)

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "Missing 'question' in request"}), 400

        context, sources = get_context_from_pinecone(question)

        prompt = f"""Answer the question using the context below.
If the context is not helpful, say so.

Context:
{context}

Question: {question}
Answer:"""

        def generate():
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            for chunk in response:
                content = chunk["choices"][0].get("delta", {}).get("content", "")
                if content:
                    yield content

        return Response(stream_with_context(generate()), content_type="text/plain")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sources", methods=["POST"])
def get_sources():
    try:
        data = request.get_json()
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "Missing 'question' in request"}), 400

        _, sources = get_context_from_pinecone(question)
        return jsonify({"sources": sources})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
