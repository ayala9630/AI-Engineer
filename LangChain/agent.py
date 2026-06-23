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

    research_instructions = (
        "You are an expert researcher. Your job is to conduct thorough research and then write a polished report. "
        "You have access to an internet search tool as your primary means of gathering information."
    )

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
            st.chat_message("user").write(message["content"])
        elif message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
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
    st.set_page_config(page_title="Agent 2 UI", layout="wide")
    st.title("Agent 2 — ממשק מחקר עם HITL")
    st.markdown("הקלד שאלה, ואז בחר מקורות בשלב הביניים כדי להמשיך.")

    get_agent()

    with st.form("query_form", clear_on_submit=True):
        query = st.text_input("שאלה", key="query_input")
        submitted = st.form_submit_button("שלח")

    if submitted and query:
        handle_user_query(query)

    if st.session_state.history:
        render_chat_history()

    if st.session_state.interrupt:
        st.markdown("### בחירת מקורות עבור HITL")
        options = [label for label, _ in st.session_state.interrupt_items]
        selected = st.multiselect("בחר מקורות מהרשימה", options)

        with st.expander("צפה בפרטי ההפרעה", expanded=False):
            st.json(getattr(st.session_state.interrupt, "value", str(st.session_state.interrupt)))

        if st.button("המשך עם הבחירות", key="resume_button"):
            handle_resume(selected)


if __name__ == "__main__":
    main()
