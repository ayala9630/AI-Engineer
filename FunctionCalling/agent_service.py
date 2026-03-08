import os
import json
import httpx
import ast  
from datetime import date
from dotenv import load_dotenv
from groq import Groq
from todo_service import get_tasks, add_task, update_task, delete_task

load_dotenv()

http_client = httpx.Client(verify=False)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    http_client=http_client
)

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "Get a list of tasks, optionally filtered by status",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["Pending", "Completed", "In Progress"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task. Calculate dates based on current date if relative time is given.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "task_type": {"type": "string"},
                    "start_date": {"type": "string", "description": "YYYY-MM-DD format"},
                    "end_date": {"type": "string", "description": "YYYY-MM-DD format"}
                },
                "required": ["title", "description", "task_type", "start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update task status or end date",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "status": {"type": "string"},
                    "end_date": {"type": "string"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"}
                },
                "required": ["task_id"]
            }
        }
    }
]

available_functions = {
    "get_tasks": get_tasks,
    "add_task": add_task,
    "update_task": update_task,
    "delete_task": delete_task,
}

def process_agent_query(user_query: str, chat_history: list = None) -> str:
    """
    מנהל את השיח עם המודל, מזהה קריאות לפונקציה ומחזיר תשובה מעובדת.
    """
    
    system_prompt = f"""
    You are a helpful task management assistant.
    Current date: {date.today()}.
    You speak Hebrew (Male gender).
    When a user asks to perform an action, call the appropriate tool.
    If the user asks for tasks, call get_tasks.
    
    IMPORTANT INSTRUCTION:
    After receiving data from a tool, summarize it in a friendly, natural Hebrew sentence.
    Do NOT return JSON objects, lists, or code structures. 
    Just output plain text.
    """

    messages = [{"role": "system", "content": system_prompt}]
    
    if chat_history:
        for turn in chat_history:
            if isinstance(turn, (list, tuple)):
                if len(turn) > 0 and turn[0]: 
                    messages.append({"role": "user", "content": str(turn[0])})
                if len(turn) > 1 and turn[1]: 
                    messages.append({"role": "assistant", "content": str(turn[1])})
            elif isinstance(turn, dict):
                role = turn.get("role")
                content = turn.get("content")
                if role and content:
                    messages.append({"role": role, "content": str(content)})

    messages.append({"role": "user", "content": user_query})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools_schema,
        tool_choice="auto",
        temperature=0.1
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    final_content = response_message.content

    if tool_calls:
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            try:
                function_response = function_to_call(**function_args)
                content_str = json.dumps(function_response, ensure_ascii=False)
            except Exception as e:
                content_str = json.dumps({"error": str(e)})

            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": content_str,
                }
            )

        second_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        final_content = second_response.choices[0].message.content

    if final_content:
        cleaned_content = final_content.strip()
        if cleaned_content.startswith("[") and "text" in cleaned_content:
            try:
                parsed_data = ast.literal_eval(cleaned_content)
                if isinstance(parsed_data, list) and len(parsed_data) > 0:
                    if isinstance(parsed_data[0], dict) and 'text' in parsed_data[0]:
                        return parsed_data[0]['text']
            except:
                pass 
                
    return final_content