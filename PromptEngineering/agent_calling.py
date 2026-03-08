from dotenv import load_dotenv
import os
import httpx
import json

def read_file_content(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"הקובץ {filename} לא נמצא."
    except Exception as e:
        return f"אירעה שגיאה: {e}"


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_MODEL = os.getenv("GROQ_MODEL")


print(f"DEBUG: Using GROQ_API_URL={GROQ_API_URL}")


async def groq_chat_completion(message: str) -> dict:
    """Call Groq AI using REST API with httpx.

    The implementation uses a configurable endpoint and API key. Adjust
    `GROQ_API_URL`, `GROQ_API_KEY`, and `GROQ_MODEL` in your environment as needed.
    """
    prompt = read_file_content('prompts/cli-commands.md')

    if not GROQ_API_KEY:
        return {"error": "GROQ_API_KEY (or XAI_API_KEY) not set in .env file"}
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ],
            "temperature": 0,
        }
        
        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            response = await client.post(
                GROQ_API_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()

            return {
                "choices": [
                    {
                        "message": {
                            "content": result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
                        }
                    }
                ]
            }
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
        print(f"Groq API Error: {error_msg}")
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"Groq API Error: {error_msg}")
        import traceback
        traceback.print_exc()
        return {"error": error_msg}