# Documentation Index & Navigation Guide

**Complete guide to all documentation for the Task Manager project.** Use this to find the right guide for what you're trying to do.

---

## 📚 Documentation Files

### Start Here (Most Important)
- **[AGENT_GUIDE.md](AGENT_GUIDE.md)** ⭐ 
  - Main guide for AI agents
  - Project overview, setup, key concepts
  - Guidelines for working with the project
  - Common patterns and conventions
  - **READ THIS FIRST**

### Understanding the Code
- **[ARCHITECTURE.md](ARCHITECTURE.md)**
  - Complete project structure explanation
  - File dependencies and relationships
  - Data flow examples
  - Database schema
  - Component responsibilities
  - **Read when you need to understand how files relate**

- **[copilot-instructions.md](copilot-instructions.md)**
  - Project-wide coding guidelines
  - Design patterns to follow
  - Performance considerations
  - Testing requirements
  - Naming conventions
  - **Read when starting any coding work**

### Doing Specific Tasks
- **[FEATURE_GUIDE.md](FEATURE_GUIDE.md)**
  - Step-by-step feature implementation
  - Complete workflow from design to testing
  - Checklists for each phase
  - Code examples for common patterns
  - **Read when adding a new feature**

- **[WORKFLOWS.md](WORKFLOWS.md)**
  - Common development workflows
  - Setup and configuration
  - Quick reference for commands
  - Integration examples
  - **Read when doing routine development**

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)**
  - Testing framework and setup
  - Test patterns and templates
  - Coverage goals and tools
  - Debugging test failures
  - **Read before writing any tests**

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**
  - Common errors and solutions
  - Performance issues and fixes
  - Debugging strategies
  - Prevention checklist
  - **Read when something breaks**

### File-Specific Instructions (in `.github/instructions/`)
- **[database.instructions.md](.github/instructions/database.instructions.md)**
  - Database design and operations
  - Connection management
  - SQL query patterns
  - Schema modification
  - **Read before editing database.py**

- **[task.instructions.md](.github/instructions/task.instructions.md)**
  - Task model structure
  - Adding new task fields
  - Field validation
  - Serialization patterns
  - **Read before editing task.py**

- **[app.instructions.md](.github/instructions/app.instructions.md)**
  - Flask web application patterns
  - Route structure
  - Request/response format
  - Error handling
  - **Read before editing app.py**

- **[main.instructions.md](.github/instructions/main.instructions.md)**
  - TaskManager class design
  - CLI patterns
  - Input validation
  - Adding new operations
  - **Read before editing main.py**

---

## 🎯 Find Documentation by Task

### "I'm new to this project"
1. Read [AGENT_GUIDE.md](AGENT_GUIDE.md) (15 min)
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) (10 min)
3. Run the project locally (see [WORKFLOWS.md](WORKFLOWS.md#one-time-setup))
4. Read [copilot-instructions.md](copilot-instructions.md) (5 min)

### "I need to add a new feature"
1. Start: [FEATURE_GUIDE.md](FEATURE_GUIDE.md)
2. Follow: Phase 1 (Planning & Design)
3. Code: Phase 2 (Implementation)
4. Test: Phase 3 (Testing)
5. Document: Phase 4 (Documentation)
6. Use file-specific instructions from `.github/instructions/` as needed

### "I need to fix a bug"
1. Start: [WORKFLOWS.md: Fixing a Bug](WORKFLOWS.md#workflow-fixing-a-bug)
2. Reference: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
3. Write: Tests that reproduce the bug
4. Fix: In the appropriate layer (see [ARCHITECTURE.md](ARCHITECTURE.md))
5. Verify: All tests pass

### "I need to write tests"
1. Start: [TESTING_GUIDE.md](TESTING_GUIDE.md)
2. Use: Test patterns for your component type
3. Run: `pytest --cov=task_manager` to check coverage
4. Reference: [TROUBLESHOOTING.md](TROUBLESHOOTING.md#test-errors) if tests fail

### "I'm editing database.py"
1. Read: [.github/instructions/database.instructions.md](.github/instructions/database.instructions.md)
2. Follow: Database Design Principles
3. Use: Query templates from instructions
4. Remember: Always use parameterized queries
5. Test: With [TESTING_GUIDE.md](TESTING_GUIDE.md) patterns

### "I'm editing task.py"
1. Read: [.github/instructions/task.instructions.md](.github/instructions/task.instructions.md)
2. Follow: Task Class Structure pattern
3. Update: database.py if schema changed
4. Add: Validation in `__post_init__`
5. Test: Field validation and serialization

### "I'm editing app.py"
1. Read: [.github/instructions/app.instructions.md](.github/instructions/app.instructions.md)
2. Follow: Route template from instructions
3. Add: Input validation
4. Error: Handle all exceptions
5. Return: Consistent JSON format

### "I'm editing main.py"
1. Read: [.github/instructions/main.instructions.md](.github/instructions/main.instructions.md)
2. Follow: Method patterns provided
3. Validate: All inputs
4. Test: With mocked database first
5. Add: CLI menu option if user-facing

### "Something is broken"
1. Check: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Debug: Using strategies in [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. Isolate: Write a test that reproduces it
4. Fix: In the identified layer
5. Verify: Test passes, other tests still pass

### "Performance is slow"
1. Profile: Using suggestions in [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Add: Database indexes
3. Optimize: Queries or algorithms
4. Check: No N+1 queries
5. Benchmark: Verify improvement

### "I need to understand how X works"
- Task model: See [ARCHITECTURE.md: task.py](ARCHITECTURE.md#taskpy-data-model-layer)
- Database: See [ARCHITECTURE.md: database.py](ARCHITECTURE.md#databasepy-data-persistence-layer)
- Web app: See [ARCHITECTURE.md: app.py](ARCHITECTURE.md#apppy-presentationweb-layer)
- CLI: See [ARCHITECTURE.md: main.py](ARCHITECTURE.md#mainpy-business-logic-layer)
- Full workflow: See [ARCHITECTURE.md: Data Flow Examples](ARCHITECTURE.md#data-flow-examples)

### "I'm stuck and need help"
1. Check [TROUBLESHOOTING.md: When Code is Completely Broken](TROUBLESHOOTING.md#when-code-is-completely-broken)
2. Look for similar issues in [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. Check test output and error messages
4. Review relevant file-specific instructions
5. Write a minimal test case to isolate the issue

---

## 📖 Reading Order (Comprehensive)

### For Agents Working on This Project (Recommended Order)

1. **[README.md](README.md)** (5 min)
   - Project overview
   - Quick start

2. **[AGENT_GUIDE.md](AGENT_GUIDE.md)** (20 min) ⭐ Essential
   - Agent guidelines
   - Project setup
   - Core concepts
   - Common patterns

3. **[ARCHITECTURE.md](ARCHITECTURE.md)** (15 min)
   - Component structure
   - File relationships
   - Data flow

4. **[copilot-instructions.md](copilot-instructions.md)** (10 min)
   - Coding guidelines
   - Naming conventions
   - Design patterns

5. **Task-Specific Guides** (as needed)
   - [FEATURE_GUIDE.md](FEATURE_GUIDE.md) for new features
   - [TESTING_GUIDE.md](TESTING_GUIDE.md) for tests
   - [WORKFLOWS.md](WORKFLOWS.md) for routines
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for issues

6. **File-Specific Instructions** (before editing)
   - See `.github/instructions/` folder

---

## 🔍 Search Guide

### By Topic

**Architecture & Design**
- Components: [ARCHITECTURE.md](ARCHITECTURE.md)
- Patterns: [AGENT_GUIDE.md: Important Patterns](AGENT_GUIDE.md#important-patterns--conventions)
- Design principles: [copilot-instructions.md](copilot-instructions.md)

**Coding**
- Guidelines: [copilot-instructions.md](copilot-instructions.md)
- Patterns: [FEATURE_GUIDE.md](FEATURE_GUIDE.md)
- Examples: [WORKFLOWS.md](WORKFLOWS.md)

**Database**
- Design: [.github/instructions/database.instructions.md](.github/instructions/database.instructions.md)
- Schema: [ARCHITECTURE.md: Database Schema](ARCHITECTURE.md#database-schema)
- Queries: [.github/instructions/database.instructions.md](.github/instructions/database.instructions.md)
- Issues: [TROUBLESHOOTING.md: Database Errors](TROUBLESHOOTING.md#database-errors)

**Testing**
- Setup: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- Patterns: [TESTING_GUIDE.md: Test Patterns](TESTING_GUIDE.md#test-patterns)
- Running: [TESTING_GUIDE.md: Running Tests](TESTING_GUIDE.md#running-tests)
- Issues: [TROUBLESHOOTING.md: Test Errors](TROUBLESHOOTING.md#test-errors)

**Troubleshooting**
- Errors: [TROUBLESHOOTING.md: Common Errors](TROUBLESHOOTING.md#common-errors--solutions)
- Performance: [TROUBLESHOOTING.md: Performance Issues](TROUBLESHOOTING.md#performance-issues)
- Debugging: [TROUBLESHOOTING.md: Debugging Strategies](TROUBLESHOOTING.md#debugging-strategies)

**Workflows**
- Setup: [WORKFLOWS.md: Setup](WORKFLOWS.md#setup--environment)
- Bug fixing: [WORKFLOWS.md: Fixing a Bug](WORKFLOWS.md#workflow-fixing-a-bug)
- Features: [WORKFLOWS.md: Adding Features](WORKFLOWS.md#workflow-adding-a-new-api-endpoint) or [FEATURE_GUIDE.md](FEATURE_GUIDE.md)
- Testing: [WORKFLOWS.md: Writing Tests](WORKFLOWS.md#workflow-writing-tests)
- Refactoring: [WORKFLOWS.md: Refactoring](WORKFLOWS.md#workflow-refactoring-code)

---

## 📋 Quick Links by File

| When editing... | Read this first |
|---|---|
| task.py | [.github/instructions/task.instructions.md](.github/instructions/task.instructions.md) |
| database.py | [.github/instructions/database.instructions.md](.github/instructions/database.instructions.md) |
| app.py | [.github/instructions/app.instructions.md](.github/instructions/app.instructions.md) |
| main.py | [.github/instructions/main.instructions.md](.github/instructions/main.instructions.md) |
| Any file | [copilot-instructions.md](copilot-instructions.md) |
| Not sure | [ARCHITECTURE.md](ARCHITECTURE.md) |

---

## 💡 Pro Tips for Agents

1. **Read instructions before editing** - Each file has specific guidelines
2. **Check ARCHITECTURE.md for dependencies** - Understand what depends on what
3. **Use FEATURE_GUIDE.md for multi-step tasks** - It provides complete checklists
4. **Refer to WORKFLOWS.md for common operations** - Copy patterns from here
5. **Check TROUBLESHOOTING.md first** - Your issue might already be documented
6. **Tests verify correctness** - If tests pass, code works
7. **Follow patterns, don't invent** - Use existing code as template

---

## 📞 When You Need Help

1. **Implementation question** → [AGENT_GUIDE.md](AGENT_GUIDE.md)
2. **Architecture question** → [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Testing question** → [TESTING_GUIDE.md](TESTING_GUIDE.md)
4. **Error/bug** → [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
5. **Feature workflow** → [FEATURE_GUIDE.md](FEATURE_GUIDE.md)
6. **Common tasks** → [WORKFLOWS.md](WORKFLOWS.md)
7. **File-specific rules** → `.github/instructions/` folder

---

## 📊 Documentation Stats

| Guide | Purpose | Length | Read Time |
|-------|---------|--------|-----------|
| AGENT_GUIDE.md | Main agent guide | Comprehensive | 20 min |
| ARCHITECTURE.md | Structure & dependencies | Detailed | 15 min |
| copilot-instructions.md | Coding guidelines | Standards | 10 min |
| FEATURE_GUIDE.md | Implementation workflow | Step-by-step | 25 min |
| TESTING_GUIDE.md | Testing framework | Reference | 20 min |
| WORKFLOWS.md | Common tasks | Quick ref | 15 min |
| TROUBLESHOOTING.md | Issues & solutions | Reference | 20 min |
| .github/instructions/* | File-specific rules | Focused | 5-10 min each |

---

## 🎯 TL;DR (Executive Summary)

**For a new agent joining the project:**

1. Read [AGENT_GUIDE.md](AGENT_GUIDE.md) (sets up context and principles)
2. Understand [ARCHITECTURE.md](ARCHITECTURE.md) (knows where everything is)
3. Follow [copilot-instructions.md](copilot-instructions.md) (writes code correctly)
4. Use task-specific guides for each project ([FEATURE_GUIDE.md](FEATURE_GUIDE.md), [TESTING_GUIDE.md](TESTING_GUIDE.md), etc.)
5. Reference file-specific instructions before editing (`.github/instructions/`)
6. Consult [TROUBLESHOOTING.md](TROUBLESHOOTING.md) when issues arise

**Key Principle:** *Different docs for different questions. Choose the one that matches your immediate need.*

---

**Last updated:** March 12, 2026  
**Project:** Task Manager  
**Status:** ✅ Well-documented and agent-ready
