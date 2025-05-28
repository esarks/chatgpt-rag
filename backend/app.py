import os
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv

print("💡 Starting app.py...")

# Load local .env file if available
load_dotenv()
print("✅ dotenv loaded")

# Try to load env variables
try:
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
    PINECONE_ENVIRONMENT = os.environ["PINECONE_ENVIRONMENT"]
    PINECONE_INDEX = os.environ["PINECONE_INDEX"]
    print("✅ Environment variables loaded")
except KeyError as e:
    print(f"❌ Missing environment variable: {e}")
    raise

import openai
import pinecone

openai.api_key = OPENAI_API_KEY

# Initialize Pinecone
try:
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
    index = pinecone.Index(PINECONE_INDEX)
    print(f"✅ Pinecone initialized with index: {PINECONE_INDEX}")
except Exception as e:
    print(f"❌ Pinecone init failed: {e}")
    raise

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    print("👋 / endpoint hit")
    return jsonify({"status": "running"})

def get_context_from_pinecone(query, top_k=5):
    try:
        print(f"🔍 Getting embedding for: {query}")
        embedding = openai.Embedding.create(
            input=query,
            model="text-embedding-ada-002"
        )["data"][0]["embedding"]
        print("✅ OpenAI embedding received")

        results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
        print(f"✅ Pinecone results: {len(results['matches'])} matches")

        context = ""
        sources = set()
        for match in results.get("matches", []):
            metadata = match.get("metadata", {})
            text = metadata.get("text", "")
            source = metadata.get("source", "unknown")
            context += f"\nSource: {source}\n{text}\n"
            sources.add(source)

        return context.strip(), list(sources)
    except Exception as e:
        print(f"❌ get_context_from_pinecone failed: {e}")
        raise

@app.route("/ask", methods=["POST"])
def ask():
    try:
        print("📥 /ask request received")
        data = request.get_json()
        question = data.get("question", "")
        print(f"🧠 Question: {question}")

        if not question:
            print("❌ No question provided")
            return jsonify({"error": "Missing 'question' in request"}), 400

        context, sources = get_context_from_pinecone(question)

        prompt = f"""Answer the question using the context below.
If the context is not helpful, say so.

Context:
{context}

Question: {question}
Answer:"""

        def generate():
            print("⚙️ Streaming OpenAI response...")
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
        print(f"❌ /ask handler failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/sources", methods=["POST"])
def get_sources():
    try:
        print("📥 /sources request received")
        data = request.get_json()
        question = data.get("question", "")
        print(f"🧠 Question: {question}")

        if not question:
            print("❌ No question provided")
            return jsonify({"error": "Missing 'question' in request"}), 400

        _, sources = get_context_from_pinecone(question)
        return jsonify({"sources": sources})
    except Exception as e:
        print(f"❌ /sources handler failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Running app on port {port}")
    app.run(host="0.0.0.0", port=port)
