from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

VAULT = "/docker/obsidian-vault"
PERSIST = "./index"

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.llm = None

print(f"Loading markdown files from: {VAULT}")
docs = SimpleDirectoryReader(
    VAULT,
    recursive=True,
    required_exts=[".md"],
).load_data()

print(f"Loaded documents: {len(docs)}")
print("Building index...")
index = VectorStoreIndex.from_documents(docs)

print(f"Persisting index to: {PERSIST}")
index.storage_context.persist(persist_dir=PERSIST)

print("Index build complete")
