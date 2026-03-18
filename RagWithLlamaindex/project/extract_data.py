import os
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from llama_index.llms.cohere import Cohere
from llama_index.core import SimpleDirectoryReader, Settings, PromptTemplate


class DecisionExtract(BaseModel):
    title: str = Field(description="כותרת קצרה של ההחלטה")
    summary: str = Field(description="תקציר ההחלטה הטכנית")
    tags: list[str] = Field(description="תגיות רלוונטיות, למשל db, architecture")

class RuleExtract(BaseModel):
    rule: str = Field(description="החוק או ההנחיה לפיתוח")
    scope: str = Field(description="תחום ההשפעה, למשל ui, backend, testing")
    notes: str = Field(description="הערות נוספות או יוצאי דופן לחוק")

class WarningExtract(BaseModel):
    area: str = Field(description="האזור או הרכיב הרגיש בקוד")
    message: str = Field(description="תוכן האזהרה או מה אסור לעשות")
    severity: str = Field(description="רמת חומרה: low, medium, high, critical")

class ExtractedDocument(BaseModel):
    decisions: list[DecisionExtract] = Field(default_factory=list)
    rules: list[RuleExtract] = Field(default_factory=list)
    warnings: list[WarningExtract] = Field(default_factory=list)


def run_extraction():
    load_dotenv()
    
    llm = Cohere(
        api_key=os.getenv("COHERE_API_KEY"),
        model="command-r-08-2024"
    )
    Settings.llm = llm

    print("סורק קבצי תיעוד מתיקיית הפרויקט...")
    
    reader = SimpleDirectoryReader(
        input_dir="./", 
        required_exts=[".md"], 
        recursive=True,
        exclude_hidden=False 
    )
    documents = reader.load_data()

    ignored_filenames = {
        "README.md", "LICENSE.md", "CHANGELOG.md", "AUTHORS.md",
        "dependencies.md", "other-tools.md", "datasetcard_template.md",
        "modelcard_template.md", "system_header_template.md", "INDEX.md",
        "DOCS_INDEX.md", "PROJECT_STRUCTURE.md"
    }

    filtered_documents = [
        doc for doc in documents 
        if doc.metadata.get("file_name") not in ignored_filenames
    ]

    prompt_string = """
    You are a strict data extraction system. You MUST use the provided schema to map the technical content into structured JSON.
    
    CATEGORIES:
    - Decisions: Architecture choices, frameworks, databases, tool selections.
    - Rules: Coding standards, conventions, specific test requirements.
    - Warnings: Known bugs, security risks, 'DO NOT' statements.
    
    EXPECTED JSON STRUCTURE EXAMPLE:
    {{
      "decisions": [
        {{"title": "Use React", "summary": "Frontend uses React for UI components", "tags": ["frontend", "ui"]}}
      ],
      "rules": [
        {{"rule": "Write tests", "scope": "testing", "notes": "Aim for 80% coverage"}}
      ],
      "warnings": []
    }}
    
    CRITICAL RULES:
    1. Output MUST be valid JSON matching the schema.
    2. If a category is empty, return an empty list [].
    
    Document Content:
    {text}
    """
    prompt_template = PromptTemplate(prompt_string)

    all_decisions = []
    all_rules = []
    all_warnings = []

    total_docs = len(filtered_documents)
    print(f"נמצאו {total_docs} קבצים רלוונטיים לאחר סינון. מתחיל חילוץ...")

    for index, doc in enumerate(filtered_documents):
        file_name = doc.metadata.get("file_name", "unknown.md")
        
        if len(doc.text.strip()) < 50:
            continue
            
        print(f"[{index + 1}/{total_docs}] מעבד קובץ: {file_name}")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = llm.structured_predict(
                    ExtractedDocument,
                    prompt_template,
                    text=doc.text
                )
                
                if isinstance(result, str):
                    preview = result[:100].replace("\n", " ")
                    print(f"  - שגיאת Pydantic/פורמט. תוכן השגיאה: '{preview}...' מדלג על הקובץ.")
                    break
                    
                print(f"  [V] חולצו: {len(result.decisions)} החלטות, {len(result.rules)} חוקים, {len(result.warnings)} אזהרות.")
                
                for d in result.decisions:
                    item_dict = d.model_dump()
                    item_dict["id"] = f"dec-{(len(all_decisions) + 1):03d}"
                    item_dict["source_file"] = file_name
                    all_decisions.append(item_dict)
                    
                for r in result.rules:
                    item_dict = r.model_dump()
                    item_dict["id"] = f"rule-{(len(all_rules) + 1):03d}"
                    item_dict["source_file"] = file_name
                    all_rules.append(item_dict)
                    
                for w in result.warnings:
                    item_dict = w.model_dump()
                    item_dict["id"] = f"warn-{(len(all_warnings) + 1):03d}"
                    item_dict["source_file"] = file_name
                    all_warnings.append(item_dict)
                    
                break 
                
            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "Too Many Requests" in err_msg:
                    sleep_time = 15 * (attempt + 1)
                    print(f"  [!] שגיאת 429. ממתין {sleep_time} שניות...")
                    time.sleep(sleep_time)
                else:
                    print(f"  [X] שגיאה בלתי צפויה: {type(e).__name__}, מדלג.")
                    break

        time.sleep(4)

    
    current_time = datetime.now(timezone.utc).isoformat()
    
    final_output = {
        "schema_version": "1.0",
        "generated_at": current_time,
        "items": {
            "decisions": all_decisions,
            "rules": all_rules,
            "warnings": all_warnings
        }
    }

    output_path = "structured_knowledge.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)

    print(f"\nהתהליך הושלם בהצלחה. הנתונים נשמרו לקובץ: {output_path}")
    print(f"סך הכל חולצו: {len(all_decisions)} החלטות, {len(all_rules)} חוקים, {len(all_warnings)} אזהרות.")

if __name__ == "__main__":
    run_extraction()
