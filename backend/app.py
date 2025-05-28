import os
from flask import Flask, request, jsonify, stream_with_context, Response
from flask_cors import CORS
import openai
import pinecone
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
pinecone_index_name = os.getenv("PINECONE_INDEX")

# Initialize Pinecone
pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
index = pinecone.Index(pinecone_index_name)

app = Flask(__name__)
CORS(app)

def get_context_from_pinecone(query, top_k=5):
    embed_response = openai.Embedding.create(input=query, model="text-embedding-ada-002")
    query_embedding = embed_response["data"][0]["embedding"]
    search_result = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    
    sources = []
    context_text = ""
    for match in search_result["matches"]:
        text = match["metadata"].get("text", "")
        source = match["metadata"].get("source", "unknown")
        context_text += f"\nSource: {source}\n{text}\n"
        sources.append(source)
    
    return context_text, sources

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    context, sources = get_context_from_pinecone(question)
    prompt = f"Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"

    def generate():
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in response:
            content = chunk["choices"][0].get("delta", {}).get("content", "")
            yield content

    return Response(stream_with_context(generate()), content_type='text/plain')

@app.route("/sources", methods=["POST"])
def get_sources():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    _, sources = get_context_from_pinecone(question)
    return jsonify({"sources": list(set(sources))})

@app.route("/")
def home():
    return "Pinecone RAG Chatbot Backend is Running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
