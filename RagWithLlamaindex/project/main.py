import os
import json
from dotenv import load_dotenv
import gradio as gr

from llama_index.core import (
    Settings, 
    VectorStoreIndex, 
    StorageContext, 
    load_index_from_storage, 
    PromptTemplate
)
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.indices.struct_store import JSONQueryEngine
from llama_index.core.workflow import Event, StartEvent, StopEvent, Workflow, step, Context
from llama_index.utils.workflow import draw_all_possible_flows

from llama_index.llms.cohere import Cohere
from llama_index.embeddings.cohere import CohereEmbedding

load_dotenv()

Settings.context_window = 128000 
Settings.num_output = 4096       

Settings.embed_model = CohereEmbedding(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    model_name="embed-multilingual-v3.0", 
    input_type="search_query" 
)

hebrew_system_prompt = (
    "You are a strict technical assistant. Your ultimate directive is to answer EVERY question entirely in Hebrew. "
    "Even if the source documentation, context nodes, or JSON data are written in English, "
    "you MUST translate the information and generate your final response STRICTLY in Hebrew. "
    "Do not output any explanations, bullet points, or lists in English."
)

Settings.llm = Cohere(
    api_key=os.getenv("COHERE_API_KEY"),
    model="command-r-08-2024",
    system_prompt=hebrew_system_prompt 
)

class ValidationEvent(Event):
    query: str

class SynthesisEvent(Event):
    response: str
    source_nodes: list
    metadata: dict

class AgenticRouterWorkflow(Workflow):
    def __init__(self, router_engine: RouterQueryEngine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.router = router_engine

    @step
    async def validate_input(self, ctx: Context, ev: StartEvent) -> ValidationEvent | StopEvent:
        """מוודא שהקלט תקין, מונע הרצת חיפוש על קלט ריק."""
        query = ev.get("query", "").strip()
        if not query or len(query) < 3:
            return StopEvent(result="השאילתה קצרה מדי או שאינה תקינה. יש לנסח שאלה ברורה.")
        return ValidationEvent(query=query)

    @step
    async def route_and_query(self, ctx: Context, ev: ValidationEvent) -> SynthesisEvent:
        """
        הנתב (Router) מחליט בזמן אמת לאיזה מנוע לפנות: 
        לחיפוש הווקטורי המקומי או למנוע ה-JSON המובנה.
        """
        try:
            response = await self.router.aquery(ev.query)
            return SynthesisEvent(
                response=str(response), 
                source_nodes=getattr(response, "source_nodes", []),
                metadata=getattr(response, "metadata", {})
            )
        except Exception as e:
            return SynthesisEvent(response=f"שגיאה במהלך ניתוב או שליפת הנתונים: {str(e)}", source_nodes=[], metadata={})

    @step
    async def format_output(self, ctx: Context, ev: SynthesisEvent) -> StopEvent:
        """מעצב את התוצאה הסופית ומוסיף מטא-דאטה בהתאם למנוע שנבחר."""
        final_response = f"🎯 תוצאה:\n{ev.response}\n\n"
        
        sources = []
        if ev.source_nodes:
            for node in ev.source_nodes:
                file_name = node.metadata.get('file_name', 'מסמך כללי')
                if file_name not in sources:
                    sources.append(file_name)
            final_response += f"**מקורות מידע (חיפוש סמנטי):** {', '.join(sources)}"
            
        elif ev.metadata and "json_path" in ev.metadata:
            json_path = ev.metadata.get("json_path", "")
            final_response += f"**נשלף מהנתונים המובנים באמצעות השאילתה:** `{json_path}`"

        return StopEvent(result=final_response)


print("טוען אינדקס מקומי מתיקיית ./storage ותבניות פרומפט...")
try:
    with open(os.path.join("prompts", "rag.md"), "r", encoding="utf-8") as f:
        qa_template = PromptTemplate(f.read())
    with open(os.path.join("prompts", "refine.md"), "r", encoding="utf-8") as f:
        refine_template = PromptTemplate(f.read())

    semantic_storage_context = StorageContext.from_defaults(persist_dir="./storage")
    semantic_index = load_index_from_storage(semantic_storage_context)
    
    semantic_query_engine = semantic_index.as_query_engine(
        similarity_top_k=4,
        text_qa_template=qa_template,
        refine_template=refine_template
    )
except Exception as e:
    print(f"שגיאה בטעינת האינדקס המקומי או תבניות הפרומפט. השגיאה: {e}")
    semantic_query_engine = None

print("טוען את המידע המובנה מקובץ ה-JSON ואת הפרומפט הייעודי...")

json_path_file = "structured_knowledge.json"
if os.path.exists(json_path_file):
    with open(json_path_file, "r", encoding="utf-8") as f:
        json_data = json.load(f)
else:
    json_data = {"items": {"decisions": [], "rules": [], "warnings": []}}

json_schema = {
    "items": {
        "decisions": [{"title": "string", "summary": "string", "tags": "list"}],
        "rules": [{"rule": "string", "scope": "string", "notes": "string"}],
        "warnings": [{"area": "string", "message": "string", "severity": "string"}]
    }
}

try:
    with open(os.path.join("prompts", "json_qa.md"), "r", encoding="utf-8") as f:
        json_qa_template = PromptTemplate(f.read())
except Exception as e:
    print(f"שגיאה בטעינת פרומפט ה-JSON מתיקיית prompts. שגיאה: {e}")
    json_qa_template = None

structured_query_engine = JSONQueryEngine(
    json_value=json_data,
    json_schema=json_schema,
    llm=Settings.llm,
    synthesize_prompt=json_qa_template 
)

print("בונה את הנתב (Router)...")
tools = [
    QueryEngineTool(
        query_engine=structured_query_engine,
        metadata=ToolMetadata(
            name="structured_data",
            description=(
                "Use this tool STRICTLY for specific structured lists: "
                "architectural decisions, coding rules, RTL guidelines, "
                "and known warnings/security risks. Useful for questions like 'what are the rules...' or 'list the decisions...'."
            )
        )
    )
]

if semantic_query_engine:
    tools.append(
        QueryEngineTool(
            query_engine=semantic_query_engine,
            metadata=ToolMetadata(
                name="semantic_search",
                description=(
                    "Use this tool for general questions about how the system works, "
                    "code logic, general documentation, or installation steps."
                )
            )
        )
    )

router_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=tools
)

rag_workflow = AgenticRouterWorkflow(router_engine=router_engine)

async def chat_function(message: str, history: list) -> str:
    try:
        result = await rag_workflow.run(query=message, timeout=120.0)
        return str(result)
    except Exception as e:
        return f"אירעה שגיאה: {str(e)}"

demo = gr.ChatInterface(
    fn=chat_function,
    title="Agentic Router RAG 🎯",
    description="מערכת RAG מבוססת אירועים - מנתבת אוטומטית בין חיפוש וקטורי מקומי לבין תשאול נתונים מובנים.",
    examples=[
        "איך מתקינים את המערכת?", 
        "תן לי רשימה של ההחלטות הטכניות שהתקבלו.", 
        "אילו אזורים הוגדרו כרגישים למגע (Warnings)?"
    ]
)

if __name__ == "__main__":
    draw_all_possible_flows(rag_workflow, filename="workflow_graph.html")
    demo.launch()
