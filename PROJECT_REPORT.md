# PROJECT REPORT

## ToDo List Manager — CLI-Based Task Management System

---

**Submitted by**
Student Name: [Your Name]
Reg No: [Your Registration Number]
Course: Fundamentals in AI and ML — CSA2001

---

---

## TABLE OF CONTENTS

1. Title
2. Introduction
3. Motivation of the Project
4. Problem Statement
5. Objective of the Project
6. Existing Methods
7. Pros and Cons of Stated Methods
8. Hardware and Software Requirements
9. Methodology and Goal
10. Functional Modules Design and Analysis
11. Algorithm Development
12. Software Architectural Diagram
13. Coding
14. Output
15. Key Implementations Outline of the System
16. Significant Project Outcomes
17. Testing and Refinement
18. Project Applicability on Real-World Applications
19. Contribution / Findings of the Project
20. Limitation / Constraints of the System
21. Conclusions
22. Future Enhancements
23. References

---

---

## 1. TITLE

**ToDo List Manager: A CLI-Based Task Management System**

---

## 2. INTRODUCTION

In the modern era of information overload and increasing personal and academic commitments, effective task management has become essential for productivity. While numerous web and mobile applications offer task management capabilities, there remains a compelling case for a lightweight, terminal-based solution that works without internet access, requires no installation of heavy frameworks, and can be used on any machine with a Python interpreter.

This project presents a complete Command-Line Interface (CLI) based ToDo List Manager developed in Python. The system allows users to create, read, update, and delete tasks (CRUD operations), assign priorities and categories, set due dates, search and filter tasks, and view progress statistics — all from the terminal.

The application is built using only Python's standard library, with SQLite as the persistence layer. It supports both an interactive menu-driven mode and direct command-line invocations, making it flexible for both casual users and developers who prefer scriptable operations.

---

## 3. MOTIVATION OF THE PROJECT

The motivation for this project stems from a real observation in daily student and professional life:

- Students juggle multiple assignments, projects, and deadlines simultaneously
- Existing tools like Google Tasks, Todoist, or Notion require internet access and account creation
- Many CS students work extensively in terminals and find switching to a browser app disruptive
- Lightweight tools are needed in low-resource or offline environments

During the course of this semester, it became clear that keeping track of assignment deadlines, lab submissions, and personal tasks in a systematic way was a genuine pain point. A terminal-based task manager that can be invoked with a single command — without launching a browser — directly addresses this need.

Additionally, this project provided an opportunity to apply core programming concepts learned in this course: data structures, file I/O, database operations, modular programming, and user interface design through CLI design patterns.

---

## 4. PROBLEM STATEMENT

**Problem:** Students and working professionals frequently lose track of tasks, miss deadlines, or waste time context-switching between browser-based productivity tools and their development environment (terminal).

**Gap:** Existing CLI tools either require complex installation, depend on external APIs, or lack features like priority management, category filtering, and statistical reporting.

**Proposed Solution:** A self-contained, Python-based CLI task manager that:
- Runs on any system with Python 3.7+
- Requires zero external dependencies
- Stores data locally using SQLite
- Offers both interactive and command-line modes
- Provides actionable insights via statistics

---

## 5. OBJECTIVE OF THE PROJECT

The primary objectives of this project are:

1. **Functional Completeness:** Implement all core task management operations — Create, Read, Update, Delete, and Complete.
2. **Usability:** Provide an intuitive interactive menu and direct CLI commands.
3. **Data Persistence:** Store all tasks reliably using a local SQLite database.
4. **Filtering and Search:** Allow users to search tasks by keyword and filter by priority or category.
5. **Insights:** Display a progress dashboard with statistics and a visual completion bar.
6. **Portability:** Ensure the application runs on Windows, macOS, and Linux with no external packages.
7. **Error Handling:** Gracefully handle invalid inputs, missing tasks, and incorrect date formats.
8. **Import/Export:** Allow data backup and restore via JSON format.

---

## 6. EXISTING METHODS

Several existing task management tools and methods were considered before designing this solution:

### 6.1 Paper-Based To-Do Lists
Traditional method of writing tasks in a physical notebook or planner.

### 6.2 Spreadsheet-Based Management
Using Microsoft Excel or Google Sheets to track tasks with manual columns for priority, due date, and status.

### 6.3 Web-Based Applications
Tools like Todoist, Trello, Asana, and Notion provide feature-rich task management through browser interfaces.

### 6.4 Mobile Applications
Apps like Microsoft To Do, TickTick, and Any.do provide task management on smartphones.

### 6.5 Existing CLI Tools
Tools like `taskwarrior` (C++) and `todo.txt` (shell scripts) provide terminal-based task management but require complex installation or lack a beginner-friendly interface.

---

## 7. PROS AND CONS OF STATED METHODS

| Method | Pros | Cons |
|---|---|---|
| Paper-based | Simple, no tech required | Not searchable, easily lost |
| Spreadsheet | Flexible, familiar | No reminders, manual work |
| Web apps (Todoist, etc.) | Feature-rich, synced | Requires internet, account, heavy |
| Mobile apps | Portable, notifications | Not usable in terminal workflows |
| Existing CLI tools (taskwarrior) | Powerful | Complex setup, steep learning curve |
| **This project (CLI ToDo Manager)** | No dependencies, offline, fast, scriptable | No GUI, no notifications (yet) |

---

## 8. HARDWARE AND SOFTWARE REQUIREMENTS

### Hardware Requirements
- Any computer with a keyboard and terminal/console access
- Minimum 512 MB RAM
- At least 10 MB free disk space

### Software Requirements

| Component | Requirement |
|---|---|
| Operating System | Windows 10/11, macOS 10.13+, or any Linux distribution |
| Python Version | Python 3.7 or higher |
| Database | SQLite3 (bundled with Python) |
| External Libraries | None — uses Python standard library only |
| Terminal | Command Prompt, PowerShell, Bash, Zsh, or any POSIX terminal |

---

## 9. METHODOLOGY AND GOAL

### Development Methodology: Iterative Incremental Development

The project was developed in three iterative phases:

**Phase 1 — Core CRUD:**
Implemented the database schema and core add/list/complete/delete functions. Verified data persistence across sessions.

**Phase 2 — Enhanced Features:**
Added priority levels, categories, due dates, overdue detection, update functionality, search, and filtering.

**Phase 3 — Polish and UX:**
Added the interactive menu system, colorized output, statistics dashboard with progress bar, import/export capability, and direct CLI command mode.

### Goal
To deliver a fully functional, well-documented, zero-dependency CLI application that meaningfully solves the task management problem for students and developers.

---

## 10. FUNCTIONAL MODULES DESIGN AND ANALYSIS

The application is organized into the following functional modules:

### 10.1 Database Layer
- `init_db()` — Creates the SQLite database and `tasks` table on first run
- `get_conn()` — Returns a database connection object

### 10.2 Task Operations
- `add_task()` — Validates input and inserts a new task record
- `list_tasks()` — Queries tasks with optional filters and displays a formatted table
- `complete_task()` — Marks a task as completed with a timestamp
- `delete_task()` — Removes a task after confirmation
- `update_task()` — Updates one or more task fields
- `view_task()` — Displays full details of a single task

### 10.3 Analytics Module
- `show_stats()` — Queries aggregated data and displays a statistics dashboard

### 10.4 Import/Export Module
- `export_tasks()` — Serializes all tasks to a JSON file
- `import_tasks()` — Reads a JSON file and inserts tasks into the database

### 10.5 User Interface Layer
- `interactive()` — The main menu loop for interactive mode
- `main()` — Entry point that routes between interactive and direct CLI modes
- `print_banner()`, `print_menu()` — Display helpers
- `c()` — Color/style formatting utility using ANSI escape codes

---

## 11. ALGORITHM DEVELOPMENT

### Algorithm: Add Task

```
BEGIN AddTask(title, description, priority, category, due_date)
  IF title is empty THEN
    PRINT error; RETURN
  END IF
  IF priority NOT IN {high, medium, low} THEN
    PRINT error; RETURN
  END IF
  IF due_date is provided AND format != YYYY-MM-DD THEN
    PRINT error; RETURN
  END IF
  SET created_at = current timestamp
  INSERT INTO tasks(title, description, priority, category, due_date, created_at)
  PRINT success message with new task ID
END
```

### Algorithm: List Tasks with Filters

```
BEGIN ListTasks(status, priority, category, search)
  BUILD SQL query with WHERE 1=1
  IF status == "pending" THEN ADD "AND completed = 0"
  IF status == "done"    THEN ADD "AND completed = 1"
  IF priority provided   THEN ADD "AND priority = ?"
  IF category provided   THEN ADD "AND LOWER(category) = LOWER(?)"
  IF search provided     THEN ADD "AND title LIKE ? OR description LIKE ?"
  ADD ORDER BY priority rank, then id
  EXECUTE query
  FOR EACH task:
    FORMAT row with colored priority, overdue detection
    PRINT formatted row
  END FOR
END
```

### Algorithm: Statistics

```
BEGIN ShowStats
  QUERY total, completed, pending, overdue counts
  QUERY pending counts grouped by priority
  QUERY top 5 categories by count
  CALCULATE completion percentage
  RENDER progress bar (filled / empty blocks)
  PRINT dashboard
END
```

---

## 12. SOFTWARE ARCHITECTURAL DIAGRAM

```
┌─────────────────────────────────────────────────────┐
│                  todo.py (Entry Point)               │
│                    main() / interactive()            │
└────────────────────────┬────────────────────────────┘
                         │
         ┌───────────────┼────────────────────┐
         │               │                    │
         ▼               ▼                    ▼
┌─────────────┐  ┌──────────────┐   ┌─────────────────┐
│  Task CRUD  │  │  UI / Menu   │   │  Import/Export  │
│  Operations │  │  Layer       │   │  Module         │
│             │  │              │   │                 │
│ add_task()  │  │ interactive()│   │ export_tasks()  │
│ list_tasks()│  │ print_menu() │   │ import_tasks()  │
│ complete()  │  │ print_banner │   └─────────────────┘
│ delete()    │  │ c() colors   │
│ update()    │  └──────────────┘
│ view()      │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Database Layer     │
│  (SQLite)           │
│  init_db()          │
│  get_conn()         │
│  tasks.db           │
└─────────────────────┘
```

---

## 13. CODING

The complete source code is available in the GitHub repository at:
`https://github.com/<your-username>/todo-list-manager`

The main file `todo.py` contains approximately 370 lines of well-commented Python code, organized into clearly separated sections:

- Database Layer (lines 1–50)
- Core Operations (lines 51–250)
- Interactive Menu (lines 251–330)
- CLI Entry Point (lines 331–370)

Key code patterns used:

**SQLite parameterized query (prevents SQL injection):**
```python
cur.execute("INSERT INTO tasks (...) VALUES (?, ?, ?, ?, ?, ?)",
            (title, description, priority, category, due_date, created_at))
```

**Dynamic filter building:**
```python
query = "SELECT ... FROM tasks WHERE 1=1"
if filter_status == "pending":
    query += " AND completed = 0"
if filter_priority:
    query += " AND priority = ?"
    params.append(filter_priority)
```

**ANSI color formatting utility:**
```python
def c(text, *styles):
    codes = "".join(COLORS.get(s, "") for s in styles)
    return f"{codes}{text}{COLORS['reset']}"
```

---

## 14. OUTPUT

### Sample: Main Menu
```
  ╔════════════════════════════════════════════╗
  ║        📝  ToDo List Manager  📝           ║
  ║     CLI Task Management System v1.0        ║
  ╚════════════════════════════════════════════╝
```

### Sample: Task List Output
```
  ID    Title                          Priority   Category        Due Date     Status
  ──────────────────────────────────────────────────────────────────────────────────
  1     Submit ML assignment           🔴 high    College         2025-05-30   ○ Pending
  2     Buy groceries                  🟡 medium  Personal        None         ○ Pending
  3     Read Chapter 5                 🟢 low     Study           2025-06-01   ✓ Done
```

### Sample: Statistics Output
```
  ╔══ Task Statistics ═══════════════════════╗
  ║  Total Tasks    : 8                      ║
  ║  Completed      : 3                      ║
  ║  Pending        : 5                      ║
  ║  Overdue        : 1                      ║
  ╠══ Completion Progress ════════════════════╣
  ║  ████████░░░░░░░░░░░░░░░░░░░░  37%       ║
  ╠══ Pending by Priority ════════════════════╣
  ║  🔴 high      : 2                        ║
  ║  🟡 medium    : 2                        ║
  ║  🟢 low       : 1                        ║
  ╚══════════════════════════════════════════╝
```

---

## 15. KEY IMPLEMENTATIONS OUTLINE OF THE SYSTEM

1. **Zero-dependency design:** The entire application uses only Python's built-in modules — no `pip install` required.
2. **SQLite persistence:** Tasks survive program restarts. The database is automatically initialized on first run.
3. **Overdue detection:** When listing tasks, any task with a past due date that is not yet completed is highlighted in red.
4. **Dynamic SQL filtering:** The `list_tasks()` function builds SQL queries dynamically based on active filters, efficiently handling all combinations.
5. **Confirmation on delete:** Destructive operations require the user to type "yes" to proceed, preventing accidental deletion.
6. **Dual-mode operation:** The same `todo.py` file works both as an interactive menu application and as a scriptable CLI tool.
7. **ANSI color coding:** Output uses color coding to improve readability — red for high priority/overdue, yellow for medium/pending, green for low/completed.

---

## 16. SIGNIFICANT PROJECT OUTCOMES

- A fully working CLI application that can be immediately used for real task management
- Zero external dependencies — runs on any standard Python 3.7+ installation
- Handles all core task management workflows in under 400 lines of clean, documented code
- Successfully demonstrates: database design, CRUD operations, query filtering, input validation, error handling, modular design, and CLI UX patterns
- The import/export feature enables data portability and backup

---

## 17. TESTING AND REFINEMENT

The following test scenarios were executed manually:

| Test Case | Input | Expected Output | Result |
|---|---|---|---|
| Add task with empty title | "" | Error message | PASS |
| Add task with invalid priority | "urgent" | Error message | PASS |
| Add task with invalid date | "30-05-2025" | Error message | PASS |
| Complete non-existent task | ID = 9999 | "Task not found" | PASS |
| Delete with "no" confirmation | "n" | "Deletion cancelled" | PASS |
| List with no tasks in DB | — | "No tasks found" | PASS |
| Filter by category (case insensitive) | "college" vs "College" | Same results | PASS |
| Export and re-import tasks | — | Task count matches | PASS |
| Direct CLI: `python todo.py done 1` | — | Task marked complete | PASS |
| Direct CLI: invalid command | `python todo.py fly` | "Unknown command" | PASS |

**Refinements made during testing:**
- Added `LOWER()` on category filter for case-insensitive matching
- Added overdue flag using Python `date` comparison (not just SQL) for accurate coloring
- Added progress bar to statistics for better visual feedback
- Unified color utility function `c()` to reduce code repetition

---

## 18. PROJECT APPLICABILITY ON REAL-WORLD APPLICATIONS

1. **Students:** Track assignment deadlines, study schedules, exam preparation tasks
2. **Developers/DevOps:** Manage ticket-like tasks directly from terminal without switching to a browser
3. **Remote/Offline Workers:** Works without internet connection, ideal for areas with poor connectivity
4. **Server Environments:** Can be deployed on a remote Linux server and accessed via SSH for team-shared task tracking (with multi-user extensions)
5. **Scripted Workflows:** The CLI command mode allows integration into shell scripts and cron jobs (e.g., automated daily task reminders)

---

## 19. CONTRIBUTION / FINDINGS OF THE PROJECT

- Demonstrated that a fully functional productivity tool can be built with zero external dependencies using Python's standard library
- Found that SQLite is well-suited for local single-user applications — fast, reliable, and requires no server setup
- Discovered that ANSI escape codes provide a rich enough color system for clear terminal UX without any UI framework
- Confirmed that separating the database layer, business logic, and presentation layer (even in a single-file app) greatly improves maintainability
- The project reinforced the value of input validation at every entry point — most user errors come from unexpected formats

---

## 20. LIMITATION / CONSTRAINTS OF THE SYSTEM

1. **No GUI:** The application is terminal-only; users unfamiliar with terminals may find it less accessible
2. **No notifications/reminders:** There is no built-in reminder system for upcoming due dates
3. **Single-user:** The SQLite database is local and not designed for concurrent multi-user access
4. **No cloud sync:** Tasks are stored locally only — no backup or sync across devices
5. **No recurring tasks:** Does not support repeating tasks (e.g., "every Monday")
6. **ANSI colors may not render on all terminals:** Older Windows Command Prompt versions may show escape codes as raw text (resolved in Windows Terminal and PowerShell 7+)

---

## 21. CONCLUSIONS

This project successfully delivers a complete, well-structured CLI-based To-Do List Manager that addresses a genuine real-world need — organized task management for students and developers who spend significant time in terminal environments.

The application demonstrates practical application of key computer science concepts: relational database design, structured query language, object-oriented and functional programming patterns, input validation, error handling, and user interface design.

By restricting the project to Python's standard library, the system achieves maximum portability — it runs identically on Windows, macOS, and Linux without any setup beyond having Python installed. The dual-mode design (interactive menu + direct CLI commands) makes it both approachable for new users and powerful for experienced ones.

The project met all stated objectives: full CRUD operations, persistent storage, priority/category management, search and filter, statistics, and import/export functionality. It represents a purposeful, well-executed solution to a real problem.

---

## 22. FUTURE ENHANCEMENTS

1. **Reminders/Notifications:** Integrate with OS notification systems (desktop notifications for due tasks)
2. **Recurring Tasks:** Support for daily/weekly/monthly repeating tasks
3. **Cloud Sync:** Optional sync with a simple REST API backend or Google Tasks API
4. **Sub-tasks:** Allow tasks to have child subtasks for complex project breakdown
5. **Tags:** Add a tagging system for flexible cross-category organization
6. **Time Tracking:** Record time spent on each task
7. **Web Interface:** Add an optional lightweight web UI (Flask) that serves the same SQLite data
8. **CSV Export:** Add CSV export format for spreadsheet compatibility
9. **Natural Language Due Dates:** Accept inputs like "tomorrow", "next Monday" in addition to YYYY-MM-DD
10. **Multi-user Support:** Implement user accounts with a shared SQLite database for team use

---

## 23. REFERENCES

1. Python Software Foundation. (2024). *Python 3 Documentation — sqlite3 module*. https://docs.python.org/3/library/sqlite3.html
2. Python Software Foundation. (2024). *Python 3 Documentation — sys module*. https://docs.python.org/3/library/sys.html
3. Python Software Foundation. (2024). *Python 3 Documentation — json module*. https://docs.python.org/3/library/json.html
4. SQLite Consortium. (2024). *SQLite Documentation*. https://www.sqlite.org/docs.html
5. ANSI/VT100 Terminal Escape Codes Reference. https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
6. Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley.
7. Hunt, A., & Thomas, D. (1999). *The Pragmatic Programmer*. Addison-Wesley.
8. VITyarthi Course Material — Fundamentals in AI and ML (CSA2001).

---

*End of Project Report*
