import gradio as gr
from agent_service import process_agent_query

def chat_wrapper(message, history):
    """
    עוטף את הפונקציה של ה-Agent כדי להתאים לממשק של Gradio.
    Gradio מעביר את ההיסטוריה כרשימה של רשימות: [[user_msg, bot_msg], ...]
    """
    response = process_agent_query(message, chat_history=history)
    return response

chat_interface = gr.ChatInterface(
    fn=chat_wrapper,
    title=" מערכת לניהול משימות",
    description="מערכת חכמה לניהול משימות יומיומיות",
    examples=["מה המשימות שלי להיום?", "הוסף משימה חדשה: לקנות חלב מחר", "תמחק את המשימה של הדוח"]
)

if __name__ == "__main__":
    chat_interface.launch(theme=gr.themes.Soft())