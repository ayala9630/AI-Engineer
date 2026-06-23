# Agent UI

מטרה:
- פרויקט זה בונה ממשק Streamlit סביב `agent.py`, שמפעיל סוכן מחקר המשתמש ב-Tavily עבור חיפוש אינטרנט.
- ה-Agent מתוכנן לבצע חיפוש חיצוני ולעצור ב-HITL (Human-In-The-Loop) כדי להציג למשתמש מקורות ולהמשיך רק אחרי בחירה.

דרישות:
- Python 3.13+ בהתאם ל-`pyproject.toml`
- ספריות מותקנות דרך הסביבה של הפרויקט (`.venv`)
- משתני סביבה:
  - `TAVILY_API_KEY` - מפתח API ל-Tavily
  - `GEMINI_API_KEY` או `GOOGLE_API_KEY` - מפתח API לשימוש ב-Gemini דרך `langchain-google-genai`

התקנה והרצה:
1. היכנס לתיקיית הפרויקט:
   ```powershell
   cd "c:\Users\This_user\Documents\הנדסאים יג\הנדסאים אילה\AI\LangChain"
   ```
2. הפעל את הסביבה הווירטואלית אם לא כבר:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
3. התקן את התלויות אם צריך:
   ```powershell
   pip install -r requirements.txt
   ```
   או אם אין `requirements.txt`:
   ```powershell
   pip install streamlit
   ```
4. הרץ את ה-UI עם `uv`:
   ```powershell
   uv run streamlit run agent.py
   ```

כיצד להשתמש:
- הזן שאלה בשדה הטקסט ולחץ `שלח`.
- אם ה-Agent מזהה צורך בחיפוש באינטרנט, הוא יעצור ויציג רשימת מקורות / requests.
- בחר את המקורות הרלוונטיים ולחץ `המשך עם הבחירות`.
- לאחר מכן ה-Agent ימשיך לייצר תשובה מבוססת המקורות שנבחרו.

דוגמאות לשאלות:
- "מצא מידע עדכני על [נושא מסוים]"
- "כתוב סיכום מחקר על [נושא]"
- "מהם היתרונות והחסרונות של [טכנולוגיה]"
- "הכן דו""ח קצר על [מוצר / שירות / תחום]."
- "איזה מידע קיים לגבי [אירוע / חדשות]"

הערות:
- אם ה-Agent לא מצליח להתחבר ל-API, בדוק שהמשתנים `TAVILY_API_KEY` ו-`GEMINI_API_KEY` מוגדרים כהלכה.
- אם יש בעיית תלות, וודא שה-venv פעיל ו-`streamlit` מותקן בסביבה הנכונה.
