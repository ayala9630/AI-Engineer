import pip_system_certs.wrapt_requests
import os
from dotenv import load_dotenv
import gradio as gr

from llama_index.core import StorageContext, VectorStoreIndex, Settings, load_index_from_storage, PromptTemplate

from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere

load_dotenv()


Settings.context_window = 128000 
Settings.num_output = 4096       

Settings.embed_model = CohereEmbedding(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    model_name="embed-multilingual-v3.0", 
    input_type="search_query" 
)

Settings.llm = Cohere(
    api_key=os.getenv("COHERE_API_KEY"),
    model="command-r-08-2024" 
)

print("Loading index from local storage...")

storage_context = StorageContext.from_defaults(persist_dir="./storage")

index = load_index_from_storage(storage_context)



qa_prompt_path = os.path.join("prompts", "rag.md")
with open(qa_prompt_path, "r", encoding="utf-8") as file:
    qa_prompt_tmpl = PromptTemplate(file.read())

refine_prompt_path = os.path.join("prompts", "refine.md")
with open(refine_prompt_path, "r", encoding="utf-8") as file:
    refine_prompt_tmpl = PromptTemplate(file.read())



qa_prompt_path = os.path.join("prompts", "rag.md")
with open(qa_prompt_path, "r", encoding="utf-8") as file:
    qa_prompt_tmpl = PromptTemplate(file.read())

query_engine = index.as_query_engine(
    similarity_top_k=7, 
    response_mode="compact",
    text_qa_template=qa_prompt_tmpl
)

def chat_function(message, history):
    """
    הפונקציה שמקבלת שאלה ומחזירה תשובה מה-RAG
    """
    try:
        response = query_engine.query(message)

        print("\n=== CONTEXT RETRIEVED ===")
        for i, node in enumerate(response.source_nodes):
            print(f"Chunk {i+1}: {node.text[:100]}...") 
        print("=========================\n")
        
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

demo = gr.ChatInterface(
    fn=chat_function,
    title="Cohere RAG System 🎯",
    description="מערכת RAG חכמה לתשאול קבצי התיעוד של צוות הפיתוח.",
    examples=["מה הצבע העיקרי של המערכת?", "האם היו שינויים ב-DB?", "מה ההנחיות ל-RTL?"]
)

if __name__ == "__main__":
    demo.launch()
