# Task Manager Project - Setup Complete ✅

**Date Created**: March 11, 2026  
**Project Type**: Python Task Management System  
**Purpose**: Comprehensive demonstration of VS Code Agentic Coding Tools

---

## 📦 What Was Created

### 1. Core Application Files

```
task_manager/
├── __init__.py              - Package initialization (40 lines)
├── main.py                  - Main application & TaskManager class (75 lines)
├── task.py                  - Task data model with validation (50 lines)
└── database.py              - Database operations with 3 intentional bugs (110 lines)
```

**Total**: ~275 lines of production Python code

### 2. Workspace Instructions

✅ **copilot-instructions.md** (110 lines)
- Project-wide coding guidelines
- Code style and conventions
- Database best practices
- Testing requirements
- Design patterns
- Performance considerations

### 3. File-Specific Instructions

✅ **`.github/instructions/task.instructions.md`** (60 lines)
- Task model structure
- Field addition guidelines
- Validation patterns
- Serialization methods

✅ **`.github/instructions/database.instructions.md`** (100 lines)
- Database design principles
- Connection lifecycle
- Parameterized query requirements
- Schema operation guidelines
- Performance & testing

### 4. Custom Prompts (Slash Commands)

✅ **`.github/prompts/quick-add-task.prompt.md`** (50 lines)
- Parameters: title, priority, description
- Generates ready-to-use code for adding tasks

✅ **`.github/prompts/query-tasks.prompt.md`** (55 lines)
- Parameters: filter_type, filter_value
- Generates query code with error handling

### 5. Custom Agents

✅ **`.github/agents/refactoring.agent.md`** (90 lines)
- Specializations: code organization, performance, architecture
- Tool Filter: Limited to code reading/writing
- Workflow: Analyze → Identify → Plan → Implement → Test

✅ **`.github/agents/testing.agent.md`** (100 lines)
- Specialization: Test-driven development
- Coverage target: >80%
- Test categories: happy path, edge cases, error handling

### 6. Multi-Step Workflow Skill

✅ **`.github/skills/task_manager/SKILL.md`** (180 lines)
- **7 Development Stages**:
  1. Feature Design
  2. Model Updates
  3. Database Schema
  4. Core Implementation
  5. Testing
  6. Documentation
  7. Code Review

✅ **`.github/skills/task_manager/README.md`** (140 lines)
- Feature Template
- Test Template
- Migration Template
- Checklists & Examples
- Troubleshooting Guide

### 7. Documentation

✅ **`README.md`** (45 lines)
- Project overview
- Feature summary
- Quick start guide

✅ **`AGENTIC_TOOLS_DOCUMENTATION.md`** (420 lines) ⭐ **Main Reference**
- Complete explanation of all tools
- How they work together
- Scenario walkthroughs
- Bug discovery examples
- Benefits summary

✅ **`QUICK_REFERENCE.md`** (220 lines) ⭐ **Quick Guide**
- At-a-glance tool table
- Common workflows
- Known issues/bugs
- Learning path
- FAQ

---

## 🎯 Agentic Tools Summary Table

| Tool | Type | File | Lines | Status |
|------|------|------|-------|--------|
| Project Guidelines | Instructions | copilot-instructions.md | 110 | ✅ |
| Task Field Patterns | Instructions | .github/instructions/task.instructions.md | 60 | ✅ |
| Database Patterns | Instructions | .github/instructions/database.instructions.md | 100 | ✅ |
| Quick Add Task | Prompt | .github/prompts/quick-add-task.prompt.md | 50 | ✅ |
| Query Tasks | Prompt | .github/prompts/query-tasks.prompt.md | 55 | ✅ |
| Refactoring Agent | Agent | .github/agents/refactoring.agent.md | 90 | ✅ |
| Testing Agent | Agent | .github/agents/testing.agent.md | 100 | ✅ |
| Feature Development | Skill | .github/skills/task_manager/SKILL.md | 180 | ✅ |
| Skill Resources | Assets | .github/skills/task_manager/README.md | 140 | ✅ |
| **TOTAL TOOLS** | **9** | **9 files** | **885 lines** | **✅** |

---

## 📊 Project Contents Summary

| Category | Count | Files |
|----------|-------|-------|
| Production Code | 4 | task_manager/*.py |
| Instructions | 3 | copilot-instructions.md + 2 in .github/instructions/ |
| Prompts | 2 | .github/prompts/*.prompt.md |
| Agents | 2 | .github/agents/*.agent.md |
| Skills | 2 | .github/skills/task_manager/* |
| Documentation | 3 | README.md, AGENTIC_TOOLS_DOCUMENTATION.md, QUICK_REFERENCE.md |
| **TOTAL** | **16** | **16 files, 1600+ lines** |

---

## 🐛 Intentional Bugs (For Testing Tools)

The project includes 3 real bugs in `task_manager/database.py`:

1. **Line ~15**: `sqlite3ct()` → should be `sqlite3.connect()`
2. **Line ~56**: `section.cursor()` → should be `self.connection.cursor()`
3. **Line ~63**: `selction.cursor()` → should be `self.connection.cursor()`

These demonstrate how agents can:
- Identify syntax errors
- Suggest corrections
- Improve code quality

---

## 🚀 How to Use This Project

### Option 1: Learn the Tools
1. Read `QUICK_REFERENCE.md` (5 min overview)
2. Read `AGENTIC_TOOLS_DOCUMENTATION.md` (20 min deep dive)
3. Try each tool systematically

### Option 2: Test Each Tool
1. Edit `task_manager/database.py` → See instructions auto-apply
2. Type `/quick-add-task` → Generate code
3. Invoke RefactoringAgent → See improvements
4. Invoke TestingAgent → Get test coverage
5. Follow Skill → Complete feature workflow

### Option 3: Find the Bugs
1. Read the code in `task_manager/database.py`
2. Ask Copilot to review for issues
3. Watch RefactoringAgent or TestingAgent find them
4. See agents suggest fixes

---

## ✨ Key Features Demonstrated

✅ **Workspace Instructions**
- Project-wide guidelines auto-applied to all task_manager code
- Ensures consistency across files

✅ **File-Specific Instructions**
- Auto-loaded when editing specific files
- Prevents domain-specific mistakes

✅ **Custom Prompts**
- Parameterized code generation
- Quick boilerplate creation

✅ **Custom Agents**
- Specialized tools for refactoring
- Specialized tools for testing
- Limited tool access for focus

✅ **Multi-Step Skills**
- Complete feature workflows
- Bundled templates and checklists
- Guidance through complexity

✅ **Real Project Code**
- Production-quality code examples
- Intentional bugs for learning
- Best practices demonstrated

---

## 📚 Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Project overview | Everyone |
| `QUICK_REFERENCE.md` | Quick lookup guide | All developers |
| `AGENTIC_TOOLS_DOCUMENTATION.md` | Complete reference | Power users |
| `copilot-instructions.md` | Workspace rules | Auto-applied |
| `.github/instructions/*.md` | File rules | Auto-applied |
| `.github/prompts/*.md` | Slash commands | Type `/` |
| `.github/agents/*.md` | Agent behavior | Invoke agents |
| `.github/skills/*/SKILL.md` | Workflow steps | Multi-step tasks |

---

## 🎓 Learning Resources

**Quick Start**: 15 minutes
- Read QUICK_REFERENCE.md
- Try one prompt (/quick-add-task)
- Edit one file to see instructions

**Deep Understanding**: 1 hour
- Read AGENTIC_TOOLS_DOCUMENTATION.md completely
- Review each tool file individually
- Map how tools interconnect

**Hands-On Practice**: 30-60 minutes
- Invoke RefactoringAgent on database.py
- Request TestingAgent for task.py
- Follow Skill for adding a feature

**Mastery**: Full project experimentation
- Modify agent configurations
- Create new prompts
- Build custom skills for your workflow

---

## 🔄 Tool Interactions

```
User Request
     ↓
Workspace Instructions (copilot-instructions.md) applied automatically
     ↓
File-Specific Instructions auto-loaded if editing specific files
     ↓
   ┌─ Use Quick Prompts (/quick-add-task) for code generation
   ├─ Invoke Agents (RefactoringAgent, TestingAgent) for specialized tasks
   └─ Follow Skills (TaskManagerDevelopment) for multi-step workflows
     ↓
Clean, consistent, quality code following best practices
```

---

## ✅ Verification Checklist

Run through this to verify everything:

- [ ] All 16 project files exist and have content
- [ ] copilot-instructions.md is in root directory
- [ ] .github/instructions/ has 2 files (task, database)
- [ ] .github/prompts/ has 2 files (quick-add-task, query-tasks)
- [ ] .github/agents/ has 2 files (refactoring, testing)
- [ ] .github/skills/task_manager/ has 2 files (SKILL.md, README.md)
- [ ] task_manager/*.py files compile (with 3 known bugs)
- [ ] Documentation files are comprehensive
- [ ] All frontmatter YAML is valid
- [ ] All description fields have meaningful content

---

## 🎉 What You Can Do Now

With this project set up, you can:

1. **Learn Agentic Tools**
   - Understand how each type of tool works
   - See real examples with all types
   - Practice invoking different tools

2. **Practice Development**
   - Use Instructions for guidance
   - Use Prompts for quick generation
   - Use Agents for specialized tasks
   - Use Skills for complete workflows

3. **Customize for Your Project**
   - Copy patterns to your own project
   - Modify instructions for your standards
   - Create custom agents for your domain
   - Build skills for your workflows

4. **Teach Others**
   - Share this as a comprehensive example
   - Use it in team workshops
   - Demonstrate tool capabilities
   - Show best practices

---

## 📝 Notes

- Project uses SQLite for simplicity (easy to test)
- Python 3.8+ required
- All code follows PEP 8 guidelines
- Intentional bugs are clearly marked for testing
- All customization files use standard frontmatter format

---

## 🏁 Next Steps

1. **Explore**: Read QUICK_REFERENCE.md for overview
2. **Understand**: Read AGENTIC_TOOLS_DOCUMENTATION.md for details
3. **Practice**: Try each tool one by one
4. **Experiment**: Modify and extend the tools
5. **Apply**: Use patterns in your own projects

---

**Project Ready for Use!** ✨

All agentic coding tools are configured and documented. Start using them based on your needs.
