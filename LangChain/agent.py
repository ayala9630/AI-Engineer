from netfree_unstrict_ssl import unstrict_ssl
unstrict_ssl()

from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
from typing import Literal

import streamlit as st
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from tavily import TavilyClient

from load_prompt import load_prompt_from_file
from ui_components import (
    display_summary_with_sources,
)

checkpointer = InMemorySaver()


def create_internet_search_tool(client):
    def internet_search(
        query: str,
        max_results: int = 5,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = False,
    ):
        """Run a web search"""
        print(f"TOOL CALLED: {query}")
        return client.search(
            query=query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )

    return internet_search


def init_agent():
    client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY", ""))
    internet_search = create_internet_search_tool(client)

    human_middleware = HumanInTheLoopMiddleware(interrupt_on={"internet_search": True})

    # טעינת System Prompt מהקובץ
    research_instructions = load_prompt_from_file("collect_information_prompt.md")

    model = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
    return create_agent(
        model=model,
        tools=[internet_search],
        system_prompt=research_instructions,
        checkpointer=checkpointer,
        middleware=[human_middleware],
    )


def get_message_text(message):
    if isinstance(message, dict):
        return message.get("content", str(message))
    if hasattr(message, "content"):
        return message.content
    return str(message)


def get_interrupt_items(interrupt):
    if not hasattr(interrupt, "value"):
        return [("interrupt", str(interrupt))]

    value = interrupt.value
    if isinstance(value, dict):
        items = []
        for field in ("action_requests", "review_configs", "sources", "tool_outputs"):
            entries = value.get(field, [])
            if entries:
                for idx, entry in enumerate(entries, start=1):
                    label = f"{field}[{idx}]"
                    items.append((label, entry))

        if items:
            return items

        return [("interrupt", value)]

    return [("interrupt", str(value))]


def build_resume_command(selected_items):
    decision = {"type": "approve"}
    if selected_items:
        decision["metadata"] = {"selected_sources": selected_items}
    return Command(resume={"decisions": [decision]})


def add_chat_message(role, content):
    st.session_state.history.append({"role": role, "content": content})


def render_chat_history():
    for message in st.session_state.history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"**{message['content']}**")
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                content = message["content"]
                
                # אם זה סיכום עם כותרות ומקורות, הציג בצורה משופרת
                if "###" in content or "**מקורות" in content or "מקורות" in content:
                    from ui_components import display_summary_with_sources
                    display_summary_with_sources(content)
                else:
                    # הצגה רגילה של markdown
                    st.markdown(content)
        else:
            st.info(message["content"])


def get_agent():
    if "agent" not in st.session_state:
        st.session_state.agent = init_agent()
        st.session_state.config = {"configurable": {"thread_id": "user-1"}}
        st.session_state.history = []
        st.session_state.interrupt = None
        st.session_state.interrupt_items = []
    return st.session_state.agent


def handle_user_query(query):
    agent = get_agent()
    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=st.session_state.config,
    )

    add_chat_message("user", query)

    if "__interrupt__" in result:
        interrupt = result["__interrupt__"][0]
        st.session_state.interrupt = interrupt
        st.session_state.interrupt_items = get_interrupt_items(interrupt)
        add_chat_message(
            "system",
            "ה-Agent עצר לביקורת HITL. בחר מקורות מהרשימה ולחץ על המשך.",
        )
        return result

    for msg in result.get("messages", []):
        text = get_message_text(msg)
        if text:
            add_chat_message("assistant", text)

    return result


def handle_resume(selected_labels):
    selected_items = [
        item for label, item in st.session_state.interrupt_items if label in selected_labels
    ]
    agent = get_agent()
    result = agent.invoke(build_resume_command(selected_items), config=st.session_state.config)

    if "__interrupt__" in result:
        st.warning("ה-Agent חזר עם הפרעה נוספת. סקור מחדש את המקורות.")
        interrupt = result["__interrupt__"][0]
        st.session_state.interrupt = interrupt
        st.session_state.interrupt_items = get_interrupt_items(interrupt)
        return result

    for msg in result.get("messages", []):
        text = get_message_text(msg)
        if text:
            add_chat_message("assistant", text)

    st.session_state.interrupt = None
    st.session_state.interrupt_items = []
    return result


def main():
    st.set_page_config(page_title="Research Agent | AI MiniNotebookLM", layout="wide")
    
    # תיאור כללי
    st.title("🤖 Research Agent — מחקר בעזרת AI")
    st.markdown("""
    **ממשק חכם לאיסוף מידע על כל נושא** 
    
    עזור לנו להבין את הנושא שלך על ידי הקלדת שאלה. ה-Agent יבצע חיפוש באינטרנט,
    יאסוף מקורות רלוונטיים, ואז — עם הסכמתך — יכין סיכום מקיף.
    """)
    
    st.divider()

    get_agent()

    # ממשק הזנת השאלה
    st.subheader("❓ מה את/ה רוצה לחקור?")
    
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        query = st.text_input(
            "הקלד את השאלה",
            key="query_input",
            placeholder="לדוגמה: 'מצא מידע עדכני על בינה מלאכותית בחודשים האחרונים'",
            label_visibility="collapsed"
        )
    with col2:
        submitted = st.button("🔍 חפש", use_container_width=True)

    if submitted and query:
        with st.spinner("⏳ ה-Agent חוקר..."):
            handle_user_query(query)
    
    st.divider()

    if st.session_state.history:
        st.subheader("💬 שיחה וממצאים")
        render_chat_history()
    else:
        st.info("💡 הקלד שאלה כדי להתחיל את המחקר")

    if st.session_state.interrupt:
        st.divider()
        st.subheader("🔍 שלב בחירת המקורות")
        st.markdown("""
        ה-Agent מצא מקורות רלוונטיים. בחר אילו מהם תרצה להשתמש להמשך המחקר:
        """)
        
        # הצגת אפשרויות בחירה יפה
        options = [label for label, _ in st.session_state.interrupt_items]
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            selected = st.multiselect(
                "📚 בחר מקורות לביקורת",
                options,
                help="בחר את המקורות שתרצה שה-Agent יעבוד איתם"
            )
        
        with col2:
            st.metric(
                label="מקורות שנבחרו",
                value=len(selected)
            )

        with st.expander("🔬 צפה בפרטי הטכניים", expanded=False):
            st.json(getattr(st.session_state.interrupt, "value", str(st.session_state.interrupt)))

        col1, col2, col3 = st.columns([0.3, 0.3, 0.4])
        with col1:
            if st.button("✅ המשך עם הבחירות", key="resume_button", use_container_width=True):
                handle_resume(selected)
        with col2:
            if st.button("⚡ בחר הכל", key="select_all_button", use_container_width=True):
                st.session_state.selected_all = True
                handle_resume(options)
        with col3:
            st.caption("או עדכן את הבחירה ולחץ המשך")


if __name__ == "__main__":
    main()
