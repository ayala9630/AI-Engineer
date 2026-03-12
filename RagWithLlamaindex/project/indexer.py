import pip_system_certs.wrapt_requests

import os
from dotenv import load_dotenv

# ספריות הליבה
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.core.node_parser import MarkdownNodeParser

# חיבורים ל-Cohere ו-Pinecone
from llama_index.embeddings.cohere import CohereEmbedding
# from llama_index.vector_stores.pinecone import PineconeVectorStore
# from pinecone import Pinecone

# טעינת מפתחות
load_dotenv()

cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("Cohere API key not found in environment variables.")

# --- שלב 1: הגדרת מודל ה-Embedding כברירת המחדל של המערכת ---
# חובה להגדיר זאת ב-Settings כדי שהמערכת לא תחפש מפתח של OpenAI
Settings.embed_model = CohereEmbedding(
    cohere_api_key=cohere_api_key,
    model_name=os.getenv("COHERE_MODEL", "embed-multilingual-v3.0"),
    input_type="search_document", # קריטי: מגדיר שזה מסמך שנשמר במסד
)

print("Loading documents from ./data ...")
# --- שלב 2: קריאת הקבצים וחיתוכם ---
reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
documents = reader.load_data()

parser = MarkdownNodeParser()
nodes = parser.get_nodes_from_documents(documents)
print(f"Created {len(nodes)} chunks from markdown files.")

# --- שלב 3 ו-4: יצירת אינדקס ושמירה לדיסק המקומי ---
print("Creating vector index locally...")
# יצירת האינדקס ישירות מהזיכרון (ללא Pinecone)
index = VectorStoreIndex(
    nodes,
    show_progress=True 
)

print("Saving to local folder './storage'...")
# שמירת כל הנתונים לתוך תיקייה בשם storage בפרויקט שלך
index.storage_context.persist(persist_dir="./storage")

print("✅ Indexing Complete! You can now run main.py")

# # --- שלב 3: התחברות ל-Pinecone ---
# from pinecone import ServerlessSpec # הוסף את זה למעלה יחד עם שאר האימפורטים

# # --- שלב 3: התחברות ל-Pinecone ויצירת האינדקס ---
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# index_name = "my-pinecone-index"

# # בדיקה אם האינדקס כבר קיים בחשבון, ואם לא - יצירה שלו
# existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

# if index_name not in existing_indexes:
#     print(f"Index '{index_name}' does not exist. Creating it now...")
#     pc.create_index(
#         name=index_name,
#         dimension=1024, # חשוב מאוד! זה הגודל של המודל של קוהיר
#         metric="cosine", # שיטת החישוב המומלצת לחיפוש טקסט
#         spec=ServerlessSpec(
#             cloud="aws",
#             region="us-east-1" # אזור ברירת המחדל החינמי
#         )
#     )
#     print("Index created successfully!")

# # כעת בטוח להתחבר לאינדקס
# vector_store = PineconeVectorStore(pinecone_index=pc.Index(index_name))
# storage_context = StorageContext.from_defaults(vector_store=vector_store)