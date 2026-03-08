# Task Manager - AI-Powered Task Management System

A smart task management system powered by AI agents, featuring a natural language chat interface for managing tasks efficiently.

## 📋 Overview

This project combines a Groq AI agent with a Gradio chat interface to provide an intelligent task management system. Users can interact with the system using natural language to create, view, update, and delete tasks.

## ✨ Features

- **Natural Language Interface**: Chat-based interface for task management using conversational Hebrew/English
- **AI-Powered Agent**: Groq-based agent with function calling capabilities for intelligent task handling
- **Task Operations**:
  - Create new tasks with titles, descriptions, types, start dates, and end dates
  - View all tasks or filter by status (Pending, In Progress, Completed)
  - Update task status and end dates
  - Delete tasks by ID
- **Status Management**: Track tasks with Pending, In Progress, and Completed statuses
- **Web-Based UI**: User-friendly Gradio chat interface

## 🏗️ Project Structure

```
Tasks/
├── main.py                 # Gradio chat interface entry point
├── agent_service.py        # Groq agent service with tool calling
├── todo_service.py         # Task management core logic
├── pyproject.toml          # Project configuration and dependencies
└── README.md              # This file
```

## 📦 Dependencies

- **gradio** (≥6.6.0): Web-based UI framework for the chat interface
- **groq** (≥1.0.0): AI API client for agentic capabilities
- **httpx** (≥0.28.1): HTTP client library
- **python-dotenv** (≥1.2.1): Environment variable management

## 🚀 Getting Started

### Prerequisites
- Python 3.13 or higher
- Groq API key

### Installation

1. Clone or navigate to the project directory:
   ```bash
   cd Tasks
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # On Windows PowerShell
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the Application

Start the chat interface:
```bash
python main.py
```

The application will launch a web interface (typically at `http://localhost:7860`) where you can interact with the task manager.

## 💬 Usage Examples

In the chat interface, you can try commands like:

- **View tasks**: "What are my tasks for today?"
- **Add task**: "Add a new task: Buy milk tomorrow"
- **Delete task**: "Delete the report task"
- **Update status**: "Mark the project task as completed"

## 🔧 Architecture

### Components

**main.py** - Gradio Chat Interface
- Wraps the agent service for Gradio compatibility
- Provides user-friendly chat interface
- Handles message history

**agent_service.py** - AI Agent Service
- Integrates with Groq API
- Implements function calling with tool definitions
- Supports operations: `get_tasks`, `add_task`, `update_task`, `delete_task`
- Processes natural language queries and routes them to appropriate functions

**todo_service.py** - Task Management Core
- `Task` class: Represents individual tasks with UUID-based IDs
- CRUD operations for task management
- In-memory task storage
- Status filtering support

## 🔌 Task Operations API

### get_tasks
Retrieve tasks, optionally filtered by status.
- **Parameters**: `status` (optional): "Pending", "In Progress", or "Completed"
- **Returns**: List of task dictionaries

### add_task
Create a new task.
- **Parameters**: 
  - `title` (required): Task title
  - `description` (required): Task description
  - `task_type` (required): Type of task
  - `start_date` (required): YYYY-MM-DD format
  - `end_date` (required): YYYY-MM-DD format
- **Returns**: Confirmation message with task details

### update_task
Update an existing task's status or end date.
- **Parameters**:
  - `task_id` (required): Task ID
  - `status` (optional): New status
  - `end_date` (optional): New end date
- **Returns**: Updated task details or error message

### delete_task
Remove a task by ID.
- **Parameters**: `task_id` (required)
- **Returns**: Confirmation or error message

## 🛠️ Development

### Project Configuration
The project uses `pyproject.toml` for dependency management with PDM/pip compatibility.

### Environment Setup
- Ensure `.env` file is properly configured before running
- SSL verification is disabled for HTTP client (for development purposes)

## 📝 Notes

- Tasks are stored in-memory (no persistent storage)
- Task IDs are generated as 8-character UUIDs
- Date format must be YYYY-MM-DD
- The system supports Hebrew language prompts in the Gradio interface

## 🎨 UI Themes

The Gradio interface uses the "Soft" theme for a comfortable user experience.
