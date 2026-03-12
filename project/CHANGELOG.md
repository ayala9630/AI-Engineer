Changelog — Recent automated edits

Summary
- Fixed several API and database issues to make the Flask web UI functional.

Files modified
- task_manager/app.py
  - Converted endpoints to use `get_db()` per-request instead of a global `db`.
  - Added robust try/except blocks and ensured `db.close()` is always called.
  - Restored original non-debug startup block (removed temporary debug changes).
  - Added additional logging for delete operations during debugging (then refined/removed as needed).

- task_manager/database.py
  - Fixed typos and correctness issues in DB code (e.g. replaced incorrect cursor calls).
  - `delete_task()` now checks `cursor.rowcount > 0` and returns `True` only when a row was deleted.
  - Ensured `sqlite3.connect()` is used correctly (previous fixes included `check_same_thread=False` when needed).

- task_manager/static/app.js
  - Improved client-side error handling for `deleteTask()` and `toggleTask()` to show server-provided error messages.

Files added (temporary diagnostics)
- task_manager/debug_delete.py (removed)
- task_manager/run_and_test_delete.py (removed)
- task_manager/show_scaffold.py (removed)
- sitecustomize.py (removed)

Files removed
- sitecustomize.py (compat shim) — removed to avoid environment-wide side effects
- debug and helper scripts used during debugging (listed above)

Notes & next steps
- Current blocker: launching the server in your virtualenv fails with `AttributeError: module 'pkgutil' has no attribute 'get_loader'`.
  - This indicates your Python environment's `pkgutil` implementation (in the venv or system) lacks `get_loader`, which Flask expects.
  - I reverted the temporary compatibility shim because it caused side effects; recommended fixes:
    - Ensure you run the app with a standard CPython installation (3.10-3.11 recommended) or
    - Recreate the venv with a compatible Python, or
    - Install/restore a proper `pkgutil` module if it was accidentally shadowed.

How to run the app locally (recommended)
1. Activate your venv (PowerShell):

   . .venv\Scripts\Activate.ps1

2. Start the server:

   python task_manager\app.py

3. Open: http://localhost:5000

If you want, I can attempt a safer compatibility shim or walk through recreating the venv. If you'd like me to try starting the server again here, say so and I will continue troubleshooting the `pkgutil.get_loader` issue.
