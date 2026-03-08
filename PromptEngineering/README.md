# 💻 CLI Command Generator - Grok AI

A FastAPI application that converts natural language text into executable terminal commands using xAI's Grok AI.

📋 **Overview**
---
This project leverages the power of Grok AI to translate natural language requests into safe, executable CLI commands. It provides a RESTful API built with FastAPI, making it easy to integrate AI-driven command generation into developer workflows.

✨ **Features**
---
* **Natural Language to CLI:** Convert plain English instructions into terminal commands.
* **Smart Parsing:** Uses a specialized prompt (`prompts/cli-commands.md`) to ensure commands are executable and safe.
* **Syntax Support:** Defaults to PowerShell syntax, with the ability to override to bash, zsh, etc.
* **Safety First:** Clear refusals for dangerous operations and asks for clarification on ambiguous requests.
* **FastAPI Backend:** Fast, modern, and documented REST API.

🚀 **Getting Started**
---
**Prerequisites**
* Python installed on your machine
* `uv` package manager installed
* Grok API Key (Get it from the [xAI Console](https://console.x.ai/))

**Installation & Setup**

1. **Configure Environment:**
   Copy the example environment file and add your API key.
   ```bash
   cp .env.example .env
   # Edit .env and paste your GROK_API_KEY