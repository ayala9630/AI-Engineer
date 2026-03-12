import pip_system_certs.wrapt_requests
import os
from dotenv import load_dotenv
import gradio as gr

# ספריות הליבה של LlamaIndex
from llama_index.core import StorageContext, VectorStoreIndex, Settings, load_index_from_storage, PromptTemplate

# חיבור ל-Cohere (עבור Embeddings ועבור ה-LLM)
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere

# טעינת המפתחות מקובץ ה-.env
load_dotenv()

# --- שלב 1: הגדרת ה"עובדים" (המודלים) בתוך LlamaIndex ---

# מגדיר ש-command-r תומך בעד 128 אלף טוקנים (מונע שגיאות חישוב)
Settings.context_window = 128000 
Settings.num_output = 4096       

# המודל שהופך טקסט למספרים (Embedding) - Cohere
Settings.embed_model = CohereEmbedding(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    model_name="embed-multilingual-v3.0", 
    input_type="search_query" 
)

# המודל שחושב ועונה (LLM) - Cohere
Settings.llm = Cohere(
    api_key=os.getenv("COHERE_API_KEY"),
    model="command-r-08-2024" 
)

# --- שלב 2: טעינת מחסן הנתונים (מהדיסק המקומי) ---
print("Loading index from local storage...")

# מגדיר ל-LlamaIndex מאיפה לקרוא את הקבצים
storage_context = StorageContext.from_defaults(persist_dir="./storage")

# טוען את האינדקס המוכן
index = load_index_from_storage(storage_context)
# --- שלב 3: קריאת הפרומפט ויצירת מנוע השאילתות ---

# הגדרת הנתיב לקובץ הפרומפט 
prompt_file_path = os.path.join("prompts", "rag.md")

# קריאת הפרומפט מהקובץ החיצוני (חובה utf-8 בגלל העברית)
with open(prompt_file_path, "r", encoding="utf-8") as file:
    qa_prompt_tmpl_str = file.read()

# הפיכת הטקסט לאובייקט ש-LlamaIndex מבין
qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

# יצירת המנוע והזרקת הפרומפט ישירות
query_engine = index.as_query_engine(
    similarity_top_k=6,
    response_mode="compact", # מכריח את המערכת להכניס את כל המידע לפרומפט אחד
    text_qa_template=qa_prompt_tmpl,
)

# --- שלב 4: הממשק הגרפי (Gradio) ---

def chat_function(message, history):
    """
    הפונקציה שמקבלת שאלה ומחזירה תשובה מה-RAG
    """
    try:
        response = query_engine.query(message)

        # דיבאג - מדפיס בטרמינל את המידע שנשלף מהמסמכים
        print("\n=== CONTEXT RETRIEVED ===")
        for i, node in enumerate(response.source_nodes):
            print(f"Chunk {i+1}: {node.text[:100]}...") 
        print("=========================\n")
        
        # חילוץ המקורות שעליהם התבססה התשובה
        sources = []
        for node in response.source_nodes:
            file_name = node.metadata.get('file_name', 'מסמך לא ידוע')
            if file_name not in sources:
                sources.append(file_name)
                
        reply = str(response)
        if sources:
            reply += f"\n\n**מקורות:** {', '.join(sources)}"
            
        return reply
    
    except Exception as e:
        return f"אופס, קרתה שגיאה: {str(e)}"

# יצירת הצ'אט
demo = gr.ChatInterface(
    fn=chat_function,
    title="Cohere RAG System 🎯",
    description="מערכת RAG חכמה לתשאול קבצי התיעוד של צוות הפיתוח.",
    examples=["מה הצבע העיקרי של המערכת?", "האם היו שינויים ב-DB?", "מה ההנחיות ל-RTL?"]
)

if __name__ == "__main__":
    demo.launch()