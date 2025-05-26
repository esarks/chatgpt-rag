from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_4n3j9n_DrU9bZFidVvc2GDdzVxBdUJ1ugnZfycqqQAHeafWxKE1ZMcYaZ2Kz31ZKhqZGPo")
index = pc.Index("rag-index")  # Replace with your actual index name

dummy = [0.0] * 1536

results = index.query(
    vector=dummy,
    top_k=100,
    include_metadata=True
)

files = set()
for match in results["matches"]:
    source = match.get("metadata", {}).get("source")
    if source:
        files.add(source)

print("Uploaded files:")
for f in sorted(files):
    print(f)
