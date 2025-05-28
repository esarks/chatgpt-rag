import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
print("✅ dotenv loaded")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")

print("🔑 Keys loaded")

# Initialize clients
openai.api_key = OPENAI_API_KEY

print("⚙️ Initializing Pinecone client...")
pc = Pinecone(api_key=PINECONE_API_KEY)

# Verify Pinecone index exists
index = pc.Index(PINECONE_INDEX)
print(f"📦 Connected to Pinecone index: {PINECONE_INDEX}")

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        _ = index.describe_index_stats()
        return jsonify(status="healthy", index_info=_), 200
    except Exception as e:
        return jsonify(status="unhealthy", error=str(e)), 500

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')

    if not question:
        return jsonify(error="Missing 'question' in request"), 400

    try:
        # Example response (replace with actual vector search + OpenAI completion)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response['choices'][0]['message']['content'].strip()
        return jsonify(answer=answer)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    print("🚀 Starting app.py...")
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
