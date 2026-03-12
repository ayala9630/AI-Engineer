# Quick Reference: Agentic Tools in Task Manager

## 🎯 At a Glance

| Tool Type | File | Purpose | How to Use |
|-----------|------|---------|-----------|
| **Workspace Instructions** | `copilot-instructions.md` | Project-wide coding guidelines | Always on; auto-loaded for task_manager/* |
| **Task Model Instructions** | `.github/instructions/task.instructions.md` | Task field/validation patterns | Auto-applied to task_manager/task.py |
| **Database Instructions** | `.github/instructions/database.instructions.md` | Security & schema best practices | Auto-applied to task_manager/database.py |
| **Quick Add Task** | `.github/prompts/quick-add-task.prompt.md` | Generate task creation code | Type: `/quick-add-task` |
| **Query Tasks** | `.github/prompts/query-tasks.prompt.md` | Generate task query code | Type: `/query-tasks` |
| **Refactoring Agent** | `.github/agents/refactoring.agent.md` | Improve code quality & architecture | Invoke when suggesting refactoring |
| **Testing Agent** | `.github/agents/testing.agent.md` | Write comprehensive tests | Invoke for "write tests" requests |
| **TaskManager Skill** | `.github/skills/task_manager/SKILL.md` | Complete feature development workflow | Use for end-to-end feature implementation |

---

## 📍 File Structure

```
project/
├── task_manager/              ← Core code
│   ├── task.py               ← Uses task.instructions.md
│   ├── database.py           ← Uses database.instructions.md (HAS BUGS!)
│   └── main.py
├── .github/
│   ├── instructions/         ← File-specific guidance
│   │   ├── task.instructions.md
│   │   └── database.instructions.md
│   ├── prompts/              ← Parameterized tasks
│   │   ├── quick-add-task.prompt.md
│   │   └── query-tasks.prompt.md
│   ├── agents/               ← Custom specialized agents
│   │   ├── refactoring.agent.md
│   │   └── testing.agent.md
│   └── skills/               ← Multi-step workflows
│       └── task_manager/
│           ├── SKILL.md
│           └── README.md (templates & checklists)
├── copilot-instructions.md   ← Workspace guidelines (applies to all)
└── AGENTIC_TOOLS_DOCUMENTATION.md ← Full documentation (this project)
```

---

## 🚀 Common Workflows

### Workflow 1: Add a New Task Quickly
```
User: I need to add a task about fixing the database
↓
Command: Type /quick-add-task
↓
Fill: title="Fix database bugs", priority="high"
↓
Result: Ready-to-use Python code
```

### Workflow 2: Query Tasks by Priority
```
User: Show me all critical tasks
↓
Command: Type /query-tasks
↓
Fill: filter_type="priority", filter_value="critical"
↓
Result: Code with error handling
```

### Workflow 3: Add a New Feature (Due Dates)
```
User: Add due_date support to tasks
↓
Use: TaskManagerDevelopment Skill
↓
Follows 7 stages:
   1. Design feature
   2. Update Task model
   3. Update database schema
   4. Implement in TaskManager
   5. Write comprehensive tests
   6. Update documentation
   7. Review & finalize
```

### Workflow 4: Clean Up Code
```
User: Refactor database module for clarity
↓
Invoke: RefactoringAgent
↓
Agent: Analyzes → Identifies issues → Suggests improvements
↓
Result: Cleaner, more maintainable code
```

### Workflow 5: Write Tests
```
User: Write comprehensive tests for task.py
↓
Invoke: TestingAgent
↓
Agent: Tests happy path → Edge cases → Error handling
↓
Result: >80% coverage test suite
```

---

## 🐛 Known Issues in Code (For Testing)

The code has **3 intentional bugs** for agents to find:

| Line | File | Issue | Detection |
|------|------|-------|-----------|
| ~15 | database.py | `sqlite3ct()` typo | TestingAgent or code review |
| ~56 | database.py | `section.cursor()` typo | Run code; will error |
| ~63 | database.py | `selction.cursor()` typo | Run code; will error |

**Test**: Ask Copilot to review database.py or run tests to find bugs.

---

## 💡 Key Concepts

### Instructions vs. Prompts vs. Agents vs. Skills

```
INSTRUCTIONS
├─ Always-on guidance
├─ Shapes how code is written
└─ "Follow these patterns"

PROMPTS  
├─ Parameterized templates
├─ One-off code generation
└─ "Generate this with these params"

AGENTS
├─ Specialized subagents
├─ Focused on one domain
└─ "Use specialized skills for this task"

SKILLS
├─ Multi-step workflows
├─ Bundled with templates
└─ "Follow this process step-by-step"
```

---

## 🎓 Learning Path

1. **Start Here**: Read [AGENTIC_TOOLS_DOCUMENTATION.md](AGENTIC_TOOLS_DOCUMENTATION.md)
2. **Understand Scope**: Review `copilot-instructions.md`
3. **Explore Files**:
   - Edit `task_manager/task.py` → See instructions auto-apply
   - Edit `task_manager/database.py` → See database instructions
4. **Try Prompts**: Type `/quick-add-task` in chat
5. **Invoke Agents**: Ask Copilot to refactor or test
6. **Follow Skill**: Use TaskManagerDevelopment for a feature

---

## 📋 Checklist: Verify All Tools Exist

- [ ] `copilot-instructions.md` - Workspace guidelines
- [ ] `.github/instructions/task.instructions.md` - Task model
- [ ] `.github/instructions/database.instructions.md` - Database
- [ ] `.github/prompts/quick-add-task.prompt.md` - Add task
- [ ] `.github/prompts/query-tasks.prompt.md` - Query tasks
- [ ] `.github/agents/refactoring.agent.md` - Refactoring
- [ ] `.github/agents/testing.agent.md` - Testing
- [ ] `.github/skills/task_manager/SKILL.md` - Feature workflow
- [ ] `.github/skills/task_manager/README.md` - Templates
- [ ] `AGENTIC_TOOLS_DOCUMENTATION.md` - Full docs
- [ ] `QUICK_REFERENCE.md` - This file

---

## 🔗 Cross-References

See full documentation for:
- **Agent Creation Details**: Section "The Project Code (With Intentional Issues)" in AGENTIC_TOOLS_DOCUMENTATION.md
- **Workflow Details**: Section "Workflow Stages" in SKILL.md
- **Database Best Practices**: .github/instructions/database.instructions.md
- **Testing Guidelines**: .github/agents/testing.agent.md

---

## ❓ FAQ

**Q: How do instructions auto-apply?**  
A: The `applyTo` field in frontmatter triggers auto-inclusion. E.g., `applyTo: "task_manager/database.py"` means database.instructions applies whenever you edit that file.

**Q: Can I use multiple tools together?**  
A: Yes! Use Skill to guide workflow → use Instructions for patterns → invoke Agent for specific task.

**Q: Why intentional bugs?**  
A: To test agent capabilities in finding and suggesting fixes. Real practice scenario.

**Q: How do I customize for my project?**  
A: Copy any file, modify frontmatter and content. Tools auto-discover in `.github/` or root.

**Q: What's the difference between a Skill and an Agent?**  
A: Skill = multi-step workflow with templates. Agent = specialized subagent with restricted tools.

---

## 📞 Support

- Full documentation: `AGENTIC_TOOLS_DOCUMENTATION.md`
- Workspace instructions: `copilot-instructions.md`
- Specific domain help: `.github/instructions/`
- Specialized workflows: `.github/agents/` or `.github/skills/`
