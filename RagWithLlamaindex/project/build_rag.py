import os
import json
import chromadb
from dotenv import load_dotenv

from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere

def initialize_settings() -> None:
    """מגדיר את מודל השפה ומודל ההטמעות של המערכת."""
    load_dotenv()
    
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY is missing from environment variables.")

    Settings.llm = Cohere(api_key=api_key, model="command-r-08-2024")
    
    Settings.embed_model = CohereEmbedding(
        cohere_api_key=api_key,
        model_name="embed-multilingual-v3.0",
        input_type="search_document"
    )

def load_documents_from_json(json_path: str) -> list[Document]:
    """קורא קובץ JSON וממיר את החוקים וההחלטות לאובייקטים מסוג Document."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"The file {json_path} does not exist.")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents: list[Document] = []

    for dec in data.get("items", {}).get("decisions", []):
        text = f"Architecture Decision: {dec['title']}\nSummary: {dec['summary']}\nTags: {', '.join(dec['tags'])}"
        doc = Document(
            text=text, 
            metadata={"type": "decision", "id": dec["id"], "source": dec["source_file"]}
        )
        documents.append(doc)

    for rule in data.get("items", {}).get("rules", []):
        text = f"Coding Rule: {rule['rule']}\nScope: {rule['scope']}\nNotes: {rule['notes']}"
        doc = Document(
            text=text, 
            metadata={"type": "rule", "id": rule["id"], "source": rule["source_file"]}
        )
        documents.append(doc)

    for warn in data.get("items", {}).get("warnings", []):
        text = f"Warning/Risk: {warn['message']}\nArea: {warn['area']}\nSeverity: {warn['severity']}"
        doc = Document(
            text=text, 
            metadata={"type": "warning", "id": warn["id"], "source": warn["source_file"]}
        )
        documents.append(doc)
    return documents

def build_or_load_index(json_path: str, persist_dir: str = "./chroma_db") -> VectorStoreIndex:
    """יוצר אינדקס וקטורי חדש או טוען אינדקס קיים ממסד נתונים מקומי."""
    db = chromadb.PersistentClient(path=persist_dir)
    chroma_collection = db.get_or_create_collection("project_knowledge")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    if chroma_collection.count() > 0:
        print("טוען אינדקס קיים ממסד הנתונים המקומי...")
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context
        )
    else:
        print("יוצר אינדקס וקטורי חדש מהמסמכים...")
        documents = load_documents_from_json(json_path)
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context
        )
        
    return index

def main() -> None:
    initialize_settings()
    
    json_file = "structured_knowledge.json"
    index = build_or_load_index(json_file)
    
    query_engine = index.as_query_engine(similarity_top_k=5)    
    query = "What database is used in this project and how should database queries be formatted to prevent security issues?"
    print(f"\nשאילתה: {query}")
    
    response = query_engine.query(query)
    print(f"\nתשובה:\n{response}")
    
    print("\nמקורות (Metadata):")
    for node in response.source_nodes:
        print(f"- {node.metadata.get('source')} (ID: {node.metadata.get('id')})")

if __name__ == "__main__":
    main()
