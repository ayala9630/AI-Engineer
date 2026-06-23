import subprocess
import sys

if __name__ == "__main__":
    # הרץ את ה-Streamlit UI
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "agent.py"],
        cwd="."
    )
