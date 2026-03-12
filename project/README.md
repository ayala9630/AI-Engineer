# Task Manager Project

A Python-based task management system with intelligent agent support for enhanced development workflows.

## Project Structure

- `task_manager/` - Core application code
- `.github/instructions/` - File-specific coding instructions
- `.github/prompts/` - Parameterized task prompts
- `.github/agents/` - Custom agents for specialized workflows
- `.github/skills/` - Reusable skill workflows

## Quick Start

### Command-Line Interface
```bash
python task_manager/main.py
```

### Web Interface (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the web application
python task_manager/app.py
```

Then open your browser to **http://localhost:5000**

## Features

- ✅ Create, read, update, and delete tasks
- ✅ Task prioritization (Critical, High, Medium, Low)
- ✅ Task status tracking (Pending, Completed)
- ✅ Task filtering (by priority, status, date)
- ✅ Statistics dashboard
- ✅ SQLite database persistence
- ✅ Modern web UI with responsive design
- ✅ REST API endpoints
- ✅ Agentic coding workflow support

## Agentic Tools Setup

This project is configured with:
- **Workspace Instructions** - General coding guidelines for the project
- **File Instructions** - Database and API-specific patterns
- **Custom Prompts** - Quick task templates
- **Custom Agents** - Specialized workflows for refactoring and testing
- **Skills** - Multi-step development processes

See `.github/` directory for detailed configuration.
