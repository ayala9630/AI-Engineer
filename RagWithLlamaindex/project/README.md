# RAG with LlamaIndex

A sophisticated Retrieval-Augmented Generation (RAG) system built with LlamaIndex, featuring agentic workflows, multi-model support, and vector-based semantic search capabilities.

## 🌟 Features

- **Agentic Workflows**: Event-driven workflow system for intelligent query routing and synthesis
- **Multi-Source Retrieval**: Support for documents, structured data (JSON), and vectors
- **Vector Search**: Powered by ChromaDB with optional Pinecone integration
- **Multi-Model Support**: 
  - LLM: Cohere's Command-R model
  - Embeddings: Cohere's multilingual embeddings
  - Fallback to OpenAI models
- **Gradio UI**: Interactive web interface for querying and exploring knowledge
- **Graph Visualization**: Network visualization of document relationships using PyVis
- **Query Routing**: Intelligent router that directs queries to appropriate retrieval engines
- **Multilingual Support**: Handles Hebrew and English text

## 📋 Requirements

- Python >= 3.13
- Virtual environment (venv)

### Key Dependencies

```
chromadb>=1.5.5
llama-index>=0.14.16
llama-index-embeddings-cohere>=0.7.0
llama-index-llms-cohere>=0.7.1
fastapi>=0.135.1
gradio>=6.9.0
pyvis>=0.3.2
networkx>=3.6.1
pydantic>=2.12.5
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Navigate to project directory
cd project

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate  # macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -e .
# or
uv sync
```

### 3. Configure API Keys

Create a `.env` file in the project root:

```env
COHERE_API_KEY=your_cohere_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_key_here
```

### 4. Build Knowledge Base

```bash
# Extract data from sources
python extract_data.py

# Build RAG indexes
python build_rag.py
```

### 5. Run the Application

```bash
python main.py
```

This launches the Gradio interface for interactive querying.

## 📁 Project Structure

```
project/
├── main.py                          # Main entry point with Gradio UI and Agentic Workflow
├── build_rag.py                     # RAG index building and initialization
├── extract_data.py                  # Data extraction and preprocessing
├── indexer.py                       # Index management utilities
├── structured_knowledge.json        # Structured knowledge base
├── workflow_graph.html              # Interactive workflow visualization
├── pyproject.toml                   # Project configuration and dependencies
├── chroma_db/                       # Vector database storage
│   └── chroma.sqlite3
├── data/                            # Indexed reference materials from external sources
│   ├── *.md files                   # Documentation indexed for RAG (from external projects)
├── prompts/                         # RAG prompt templates
│   ├── rag.md                       # RAG system prompt
│   └── refine.md                    # Refinement prompt
├── storage/                         # LlamaIndex storage (vectors, graphs, indexes)
│   ├── default__vector_store.json
│   ├── docstore.json
│   └── index_store.json
└── lib/                             # Frontend libraries
    ├── vis-9.1.2/                   # Vis.js for graph visualization
    └── tom-select/                  # UI component library
```

## 🔧 Configuration

### LLM Settings

Modify `main.py` to adjust model parameters:

```python
Settings.context_window = 128000  # Context window size
Settings.num_output = 4096        # Maximum output tokens
Settings.embed_model = CohereEmbedding(...)
Settings.llm = Cohere(...)
```

### Vector Store

- **Default**: ChromaDB (local SQLite)
- **Alternative**: Pinecone (cloud-based)

Configure in `build_rag.py`:

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.vector_stores.pinecone import PineconeVectorStore
```

## 🤖 Agentic Workflow

The system uses an event-driven agentic workflow:

1. **Query Input** → `StartEvent`
2. **Query Validation** → `ValidationEvent`
3. **Router Decision** → Routes to appropriate retrieval engine
4. **Context Retrieval** → Fetches relevant documents/data
5. **Response Synthesis** → `SynthesisEvent`
6. **Output** → `StopEvent`

This architecture enables:
- Intelligent query routing
- Multi-source information synthesis
- Fallback mechanisms
- Streaming response support

## 📚 Usage Examples

### Interactive Query (Gradio UI)

```bash
python main.py
```

Then open the browser to the provided URL and query your knowledge base.

### Programmatic Query

```python
from main import AgenticRouterWorkflow, router_engine

workflow = AgenticRouterWorkflow(router_engine)
response = workflow.run(query="Your question here")
```

### Data Extraction and Indexing

```bash
python extract_data.py          # Extract from sources
python build_rag.py             # Build indexes
python indexer.py               # Manage indexes
```

## 📊 Outputs

- **Gradio Interface**: Interactive web UI at `http://localhost:7860`
- **Workflow Visualization**: `workflow_graph.html` - Interactive graph of document relationships
- **Vector Database**: ChromaDB storage in `chroma_db/`
- **Structured Knowledge**: `structured_knowledge.json` - Extracted and structured data

## 🔍 Query Types Supported

- **Semantic Search**: Find similar documents/passages
- **Structured Query**: JSON data querying
- **Routing Query**: Automatic routing to best retrieval engine
- **Synthesis Query**: Multi-source answer generation

## 🛠️ Troubleshooting

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -e .
```

### API Key Issues

- Verify `.env` file exists and contains valid keys
- Check `COHERE_API_KEY` and `OPENAI_API_KEY` are set

### Vector Database Issues

Rebuild the indexes:
```bash
python build_rag.py --rebuild
```

### Performance

- Adjust `context_window` and `num_output` in settings
- Monitor ChromaDB for optimal performance
- Consider using Pinecone for large-scale deployments

## 💬 Example Queries

The RAG system can answer a wide variety of questions about your indexed knowledge base. Here are some example queries demonstrating the system's capabilities:

### Example 1: System Overview and Setup

**שאלה:**
מה המטרה הכללית של המערכת ואיך מבצעים התקנה?

**תשובה:**
 המטרה הכללית של המערכת היא לספק סביבת עבודה יעילה ומאורגנת עבור פרויקטים של פיתוח תוכנה. המערכת כוללת מגוון כלים, הנחיות ודרכי עבודה המסייעים בתהליך הפיתוח, החל משלב התכנון ועד לשלב הבדיקות והפריסה.
לגבי התקנת המערכת, על פי המסמכים, יש לבצע את השלבים הבאים:
1. קריאה מעמיקה של AGENT_GUIDE.md המספק סקירה כללית על הפרויקט
2. הבנת המבנה והארכיטקטורה של הפרויקט באמצעות ARCHITECTURE.md
3. עיון בקובץ הנחיות הקידוד ודפוסי העיצוב

### Example 2: Task Management Logic

**שאלה:** 
האם יש הסבר על הלוגיקה מאחורי ניהול המשימות בפרויקט?

**תשובה:** 
ניהול המשימות בפרויקט מתואר כמערכת בעלת 7 שלבי פיתוח:
1. **עיצוב התכונה** - תכנון ועיצוב של התכונה החדשה
2. **עדכוני מודל** - עדכון המודלים הרלוונטיים למערכת
3. **תכנון מאגר הנתונים** - הגדרת מבנה מאגר הנתונים
4. **יישום הליבה** - יישום הליבה של התכונה החדשה
5. **בדיקות** - בדיקות מקיפות של התכונה
6. **תיעוד** - תיעוד מקיף של התכונה
7. **ביקורת קוד** - ביקורת על הקוד כדי לוודא שעומד בסטנדרטים

### Example 3: Database Technical Decisions

**שאלה:** 
"תן רשימה של כל ההחלטות הטכניות שהתקבלו בפרויקט בנוגע למסדי נתונים."

**תשובה:** 
החלטות טכניות בנוגע למסדי נתונים:
שימוש ב-SQLite כמסד נתונים
שימוש ב-SQLite לניהול הנתונים
שימוש בדאטאקלאס (dataclass) למידול הנתונים
