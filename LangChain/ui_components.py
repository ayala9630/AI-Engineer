"""
רכיבי UI משופרים להצגת תוצאות האגנט בצורה ידידותית למשתמש
"""

import streamlit as st
import re
from typing import List, Dict


def extract_sources(text: str) -> List[Dict]:
    """
    חלץ את המקורות מהטקסט
    תומך בפורמטים: [כותרת - URL] או [כותרת](URL)
    """
    sources = []
    
    # חיפוש בפורמט [כותרת - URL]
    pattern1 = r'\*?\s*\[(.*?)\s*-\s*([^\]]+)\]'
    matches1 = re.findall(pattern1, text)
    
    for title, url in matches1:
        sources.append({
            "title": title.strip(),
            "url": url.strip()
        })
    
    # חיפוש בפורמט [כותרת](URL)
    pattern2 = r'\[(.*?)\]\((https?:\/\/[^\)]+)\)'
    matches2 = re.findall(pattern2, text)
    
    for title, url in matches2:
        if {"title": title.strip(), "url": url.strip()} not in sources:
            sources.append({
                "title": title.strip(),
                "url": url.strip()
            })
    
    return sources


def remove_sources_section(text: str) -> str:
    """
    הסרת סעיף המקורות מהטקסט
    """
    # הסרת סעיף מקורות בכמה פורמטים אפשריים
    text = re.sub(r'\n*-{3,}\n*\*?\*?מקורות.*?(?=\n|$)', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\n+###\s*מקורות.*?(?=\n\n|$)', '', text, flags=re.DOTALL | re.IGNORECASE)
    return text.strip()


def display_summary_with_sources(content: str):
    """
    הצגה משופרת של סיכום עם מקורות - עם markdown rendering
    """
    sources = extract_sources(content)
    content = remove_sources_section(content)
    
    # הצגת התוכן הראשי בMarkdown
    st.markdown(content)
    
    # הצגת המקורות בצורה יפה
    if sources:
        st.divider()
        
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.subheader("📚 מקורות")
        with col2:
            st.caption(f"כלל {len(sources)} מקורות")
        
        for idx, source in enumerate(sources, 1):
            col_num, col_content = st.columns([0.05, 0.95])
            
            with col_num:
                st.markdown(f"**{idx}.**")
            
            with col_content:
                title = source['title']
                url = source['url']
                
                # הצגת בצורת link
                st.markdown(f"[{title}]({url})")


def render_section_with_icon(title: str, icon: str, content: str):
    """
    רנדור סעיף עם אייקון
    """
    st.subheader(f"{icon} {title}")
    st.markdown(content)


def create_metric_cards(metrics: Dict[str, any]):
    """
    יצירת כרטיסי מטריקה
    """
    cols = st.columns(len(metrics))
    
    for col, (label, value) in zip(cols, metrics.items()):
        with col:
            st.metric(label=label, value=value)


def display_sources_for_review(sources: List[Dict]):
    """
    הצגה יפה של מקורות לביקורת המשתמש
    """
    st.subheader("🔍 בדוק ובחר מקורות")
    
    selected_sources = []
    
    for idx, source in enumerate(sources, 1):
        cols = st.columns([0.05, 0.95])
        
        with cols[0]:
            checked = st.checkbox(" ", key=f"source_{idx}", value=True)
        
        with cols[1]:
            col_title, col_url = st.columns([0.6, 0.4])
            with col_title:
                st.write(f"**{source.get('title', 'מקור ללא כותרת')}**")
            with col_url:
                url = source.get('url', '#')
                st.caption(f"🔗 [צפה]({url})")
        
        if checked:
            selected_sources.append(source)
    
    return selected_sources


def display_error_message(error: str):
    """
    הצגת הודעת שגיאה בצורה יפה
    """
    st.error(f"❌ שגיאה: {error}")


def format_content_for_display(content: str) -> str:
    """
    עיצוב כללי של תוכן לתצוגה
    - המרה של ** ל-bold
    - המרה של * ל-italics
    - שמירה על כל המארקאפ
    """
    return content
