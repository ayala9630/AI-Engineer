import pip_system_certs.wrapt_requests
import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter

from llama_index.embeddings.cohere import CohereEmbedding

load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("Cohere API key not found.")

Settings.embed_model = CohereEmbedding(
    cohere_api_key=cohere_api_key,
    model_name=os.getenv("COHERE_MODEL", "embed-multilingual-v3.0"),
    input_type="search_document", 
)

print("Loading documents from ./data ...")
reader = SimpleDirectoryReader(
    input_dir="./data", 
    recursive=True,
    exclude_hidden=False
documents = reader.load_data()

parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = parser.get_nodes_from_documents(documents)
print(f"Created {len(nodes)} perfectly sized chunks from files.")

print("Creating vector index locally...")
index = VectorStoreIndex(
    nodes,
    show_progress=True 
)

print("Saving to local folder './storage'...")
index.storage_context.persist(persist_dir="./storage")

print("✅ Indexing Complete! You can now run main.py")
