import logging
from pathlib import Path
from typing import Any

# הגדרת לוגר להדפסת שגיאות בצורה מסודרת
logger = logging.getLogger(__name__)

def load_prompt_from_file(file_path: str | Path, **kwargs: Any) -> str:
    """
    Loads a prompt from a text/markdown file and optionally formats it with dynamic variables.

    Args:
        file_path (str | Path): The path to the prompt file (e.g., 'prompts/agent_prompt.md').
        **kwargs: Arbitrary keyword arguments to be injected into the prompt using string formatting.

    Returns:
        str: The fully formatted prompt string.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        KeyError: If a format variable in the text is missing from kwargs.
        IOError: If there is an issue reading the file.
    """
    path_obj = Path(file_path)
    
    try:
        # פתיחת הקובץ עם קידוד מפורש למניעת בעיות במערכות הפעלה שונות
        with path_obj.open('r', encoding='utf-8') as file:
            content = file.read()
            
        # אם הועברו ארגומנטים נוספים, נזריק אותם לפרומפט
        if kwargs:
            content = content.format(**kwargs)
            
        return content

    except FileNotFoundError:
        logger.error(f"Error: Prompt file not found at '{path_obj.absolute()}'.")
        raise
    except KeyError as e:
        logger.error(f"Error: Missing variable for prompt formatting: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while reading prompt file '{file_path}': {e}")
        raise

# --- דוגמת שימוש (Usage Example) ---
if __name__ == "__main__":
    from datetime import datetime
    
    # יצירת קובץ דמה לצורך הדוגמה (במציאות זה יהיה הקובץ agent_prompt.md שיצרת קודם)
    test_file = "test_prompt.md"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("You are an AI assistant. Today's date is {current_date}. Your user is {username}.")
    
    try:
        # טעינת הפרומפט והזרקת המשתנים בזמן ריצה
        prompt = load_prompt_from_file(
            test_file, 
            current_date=datetime.now().strftime("%Y-%m-%d"),
            username="Alice"
        )
        print("Loaded Prompt:\n", prompt)
    except Exception as e:
        print("Failed to load prompt.")