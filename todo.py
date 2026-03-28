#!/usr/bin/env python3
"""
ToDo List Manager - CLI Application
A complete command-line task management system with priorities, categories, and due dates.
"""

import json
import os
import sys
import sqlite3
from datetime import datetime, date
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.db")

PRIORITIES = {"high": "🔴", "medium": "🟡", "low": "🟢"}
COLORS = {
    "red":    "\033[91m",
    "yellow": "\033[93m",
    "green":  "\033[92m",
    "cyan":   "\033[96m",
    "bold":   "\033[1m",
    "reset":  "\033[0m",
    "dim":    "\033[2m",
    "blue":   "\033[94m",
    "magenta":"\033[95m",
}

def c(text, *styles):
    codes = "".join(COLORS.get(s, "") for s in styles)
    return f"{codes}{text}{COLORS['reset']}"


# ─────────────────────────────────────────────
# DATABASE LAYER
# ─────────────────────────────────────────────

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            description TEXT    DEFAULT '',
            priority    TEXT    DEFAULT 'medium',
            category    TEXT    DEFAULT 'General',
            due_date    TEXT    DEFAULT NULL,
            completed   INTEGER DEFAULT 0,
            created_at  TEXT    NOT NULL,
            completed_at TEXT   DEFAULT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_conn():
    return sqlite3.connect(DB_PATH)


# ─────────────────────────────────────────────
# CORE OPERATIONS
# ─────────────────────────────────────────────

def add_task(title: str, description: str = "", priority: str = "medium",
             category: str = "General", due_date: Optional[str] = None):
    """Insert a new task into the database."""
    if not title.strip():
        print(c("Error: Task title cannot be empty.", "red"))
        return None

    if priority not in PRIORITIES:
        print(c(f"Error: Priority must be one of {list(PRIORITIES.keys())}.", "red"))
        return None

    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print(c("Error: Due date must be in YYYY-MM-DD format.", "red"))
            return None

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (title, description, priority, category, due_date, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (title.strip(), description.strip(), priority, category.strip(), due_date, created_at)
        )
        task_id = cur.lastrowid
        conn.commit()
    print(c(f"\n✅ Task #{task_id} added successfully!", "green", "bold"))
    return task_id


def list_tasks(filter_status: str = "pending", filter_priority: Optional[str] = None,
               filter_category: Optional[str] = None, search: Optional[str] = None):
    """Display tasks based on filters."""
    query = "SELECT id, title, description, priority, category, due_date, completed, created_at FROM tasks WHERE 1=1"
    params = []

    if filter_status == "pending":
        query += " AND completed = 0"
    elif filter_status == "done":
        query += " AND completed = 1"
    # "all" — no filter

    if filter_priority:
        query += " AND priority = ?"
        params.append(filter_priority)

    if filter_category:
        query += " AND LOWER(category) = LOWER(?)"
        params.append(filter_category)

    if search:
        query += " AND (LOWER(title) LIKE LOWER(?) OR LOWER(description) LIKE LOWER(?))"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, id"

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()

    if not rows:
        print(c("\n  No tasks found.", "dim"))
        return

    today = date.today()
    print()
    print(c(f"  {'ID':<5} {'Title':<30} {'Priority':<10} {'Category':<15} {'Due Date':<12} {'Status'}", "bold"))
    print(c("  " + "─" * 85, "dim"))

    for row in rows:
        tid, title, desc, priority, category, due_date, completed, created_at = row

        pri_icon = PRIORITIES.get(priority, "⬜")
        status = c("✓ Done", "green") if completed else c("○ Pending", "yellow")
        title_display = (title[:27] + "...") if len(title) > 30 else title

        due_display = ""
        if due_date:
            due_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
            overdue = not completed and due_obj < today
            due_display = c(due_date, "red") if overdue else due_date
        else:
            due_display = c("None", "dim")

        pri_color = {"high": "red", "medium": "yellow", "low": "green"}.get(priority, "reset")
        pri_display = c(f"{pri_icon} {priority}", pri_color)

        print(f"  {tid:<5} {title_display:<30} {pri_display:<20} {category:<15} {due_display:<20} {status}")

    print()


def complete_task(task_id: int):
    """Mark a task as completed."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if not row:
            print(c(f"Error: Task #{task_id} not found.", "red"))
            return
        if row[2]:
            print(c(f"Task #{task_id} is already completed.", "yellow"))
            return
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("UPDATE tasks SET completed = 1, completed_at = ? WHERE id = ?",
                    (completed_at, task_id))
        conn.commit()
    print(c(f"\n🎉 Task #{task_id} '{row[1]}' marked as complete!", "green", "bold"))


def delete_task(task_id: int):
    """Delete a task permanently."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT title FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if not row:
            print(c(f"Error: Task #{task_id} not found.", "red"))
            return
        confirm = input(c(f"  Delete task '{row[0]}'? (yes/no): ", "yellow")).strip().lower()
        if confirm in ("yes", "y"):
            cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            print(c(f"\n🗑  Task #{task_id} deleted.", "red"))
        else:
            print(c("  Deletion cancelled.", "dim"))


def update_task(task_id: int, **kwargs):
    """Update one or more fields of a task."""
    allowed = {"title", "description", "priority", "category", "due_date"}
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}

    if not updates:
        print(c("Nothing to update.", "dim"))
        return

    if "priority" in updates and updates["priority"] not in PRIORITIES:
        print(c(f"Error: Priority must be one of {list(PRIORITIES.keys())}.", "red"))
        return

    if "due_date" in updates and updates["due_date"]:
        try:
            datetime.strptime(updates["due_date"], "%Y-%m-%d")
        except ValueError:
            print(c("Error: Due date must be in YYYY-MM-DD format.", "red"))
            return

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [task_id]

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM tasks WHERE id = ?", (task_id,))
        if not cur.fetchone():
            print(c(f"Error: Task #{task_id} not found.", "red"))
            return
        cur.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
        conn.commit()
    print(c(f"\n✏️  Task #{task_id} updated successfully!", "cyan", "bold"))


def view_task(task_id: int):
    """Show full details of a single task."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()

    if not row:
        print(c(f"Error: Task #{task_id} not found.", "red"))
        return

    tid, title, description, priority, category, due_date, completed, created_at, completed_at = row
    today = date.today()
    overdue = ""
    if due_date and not completed:
        due_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
        if due_obj < today:
            overdue = c("  ⚠️  OVERDUE!", "red", "bold")

    print()
    print(c("  ┌── Task Details ──────────────────────────", "cyan"))
    print(c(f"  │  ID       : ", "dim") + c(str(tid), "bold"))
    print(c(f"  │  Title    : ", "dim") + c(title, "bold"))
    print(c(f"  │  Desc     : ", "dim") + (description or c("(none)", "dim")))
    print(c(f"  │  Priority : ", "dim") + c(f"{PRIORITIES[priority]} {priority}", {"high":"red","medium":"yellow","low":"green"}[priority]))
    print(c(f"  │  Category : ", "dim") + category)
    print(c(f"  │  Due Date : ", "dim") + (due_date or c("Not set", "dim")) + overdue)
    print(c(f"  │  Status   : ", "dim") + (c("✓ Completed", "green") if completed else c("○ Pending", "yellow")))
    print(c(f"  │  Created  : ", "dim") + created_at)
    if completed_at:
        print(c(f"  │  Finished : ", "dim") + completed_at)
    print(c("  └──────────────────────────────────────────", "cyan"))
    print()


def show_stats():
    """Display summary statistics."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tasks")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
        done = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tasks WHERE completed = 0")
        pending = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tasks WHERE completed = 0 AND due_date < date('now')")
        overdue = cur.fetchone()[0]
        cur.execute("SELECT priority, COUNT(*) FROM tasks WHERE completed = 0 GROUP BY priority")
        by_priority = dict(cur.fetchall())
        cur.execute("SELECT category, COUNT(*) FROM tasks GROUP BY category ORDER BY COUNT(*) DESC LIMIT 5")
        by_category = cur.fetchall()

    pct = int((done / total * 100) if total else 0)
    bar_len = 30
    filled = int(bar_len * pct / 100)
    bar = c("█" * filled, "green") + c("░" * (bar_len - filled), "dim")

    print()
    print(c("  ╔══ Task Statistics ═══════════════════════╗", "cyan", "bold"))
    print(c(f"  ║  Total Tasks    : {total:<24}║", "cyan"))
    print(c(f"  ║  Completed      : {done:<24}║", "cyan"))
    print(c(f"  ║  Pending        : {pending:<24}║", "cyan"))
    print(c(f"  ║  Overdue        : {overdue:<24}║", "cyan"))
    print(c(f"  ╠══ Completion Progress ════════════════════╣", "cyan", "bold"))
    print(f"  {c('║', 'cyan')}  {bar}  {c(str(pct)+'%','bold')}           {c('║','cyan')}")
    print(c(f"  ╠══ Pending by Priority ════════════════════╣", "cyan", "bold"))
    for pri, icon in PRIORITIES.items():
        cnt = by_priority.get(pri, 0)
        print(c(f"  ║  {icon} {pri:<10}: {cnt:<24}║", "cyan"))
    print(c(f"  ╠══ Top Categories ═════════════════════════╣", "cyan", "bold"))
    for cat, cnt in by_category:
        line = f"  ║  {cat:<15}: {cnt:<24}║"
        print(c(line, "cyan"))
    print(c("  ╚══════════════════════════════════════════╝", "cyan", "bold"))
    print()


def export_tasks(filepath: str):
    """Export all tasks to a JSON file."""
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks")
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]

    with open(filepath, "w") as f:
        json.dump(rows, f, indent=2)
    print(c(f"\n📤 {len(rows)} tasks exported to {filepath}", "green"))


def import_tasks(filepath: str):
    """Import tasks from a JSON file."""
    if not os.path.exists(filepath):
        print(c(f"Error: File '{filepath}' not found.", "red"))
        return
    with open(filepath) as f:
        rows = json.load(f)

    count = 0
    with get_conn() as conn:
        cur = conn.cursor()
        for r in rows:
            cur.execute(
                "INSERT INTO tasks (title, description, priority, category, due_date, completed, created_at, completed_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (r.get("title",""), r.get("description",""), r.get("priority","medium"),
                 r.get("category","General"), r.get("due_date"), r.get("completed",0),
                 r.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                 r.get("completed_at"))
            )
            count += 1
        conn.commit()
    print(c(f"\n📥 {count} tasks imported successfully!", "green"))


# ─────────────────────────────────────────────
# INTERACTIVE MENU
# ─────────────────────────────────────────────

def print_banner():
    print(c("""
  ╔════════════════════════════════════════════╗
  ║        📝  ToDo List Manager  📝           ║
  ║     CLI Task Management System v1.0        ║
  ╚════════════════════════════════════════════╝
""", "cyan", "bold"))


def print_menu():
    print(c("  ─── Main Menu ─────────────────────────────", "dim"))
    items = [
        ("1", "Add Task"),
        ("2", "List Pending Tasks"),
        ("3", "List All Tasks"),
        ("4", "View Task Details"),
        ("5", "Mark Task Complete"),
        ("6", "Update Task"),
        ("7", "Delete Task"),
        ("8", "Search Tasks"),
        ("9", "Filter by Priority"),
        ("10","Filter by Category"),
        ("11","Statistics"),
        ("12","Export Tasks (JSON)"),
        ("13","Import Tasks (JSON)"),
        ("0", "Exit"),
    ]
    for num, label in items:
        print(f"  {c(num+')', 'cyan', 'bold'):<18} {label}")
    print(c("  ────────────────────────────────────────────", "dim"))


def prompt(msg: str, default: str = "") -> str:
    val = input(c(f"  {msg}", "blue")).strip()
    return val if val else default


def interactive():
    init_db()
    print_banner()
    while True:
        print_menu()
        choice = prompt("Enter choice: ").strip()

        if choice == "0":
            print(c("\n  👋 Goodbye!\n", "cyan", "bold"))
            sys.exit(0)

        elif choice == "1":
            print(c("\n  ── Add New Task ──", "cyan", "bold"))
            title = prompt("Title (required): ")
            if not title:
                print(c("  Title is required.", "red"))
                continue
            desc = prompt("Description (optional): ")
            priority = prompt("Priority [high/medium/low] (default: medium): ", "medium")
            category = prompt("Category (default: General): ", "General")
            due_date = prompt("Due date YYYY-MM-DD (optional, press Enter to skip): ")
            add_task(title, desc, priority, category, due_date or None)

        elif choice == "2":
            print(c("\n  ── Pending Tasks ──", "cyan", "bold"))
            list_tasks(filter_status="pending")

        elif choice == "3":
            print(c("\n  ── All Tasks ──", "cyan", "bold"))
            list_tasks(filter_status="all")

        elif choice == "4":
            tid = prompt("Task ID: ")
            if tid.isdigit():
                view_task(int(tid))
            else:
                print(c("  Invalid ID.", "red"))

        elif choice == "5":
            tid = prompt("Task ID to mark complete: ")
            if tid.isdigit():
                complete_task(int(tid))
            else:
                print(c("  Invalid ID.", "red"))

        elif choice == "6":
            tid = prompt("Task ID to update: ")
            if not tid.isdigit():
                print(c("  Invalid ID.", "red"))
                continue
            print(c("  Leave field blank to keep current value.", "dim"))
            title    = prompt("New title: ") or None
            desc     = prompt("New description: ") or None
            priority = prompt("New priority [high/medium/low]: ") or None
            category = prompt("New category: ") or None
            due_date = prompt("New due date YYYY-MM-DD: ") or None
            update_task(int(tid), title=title, description=desc,
                        priority=priority, category=category, due_date=due_date)

        elif choice == "7":
            tid = prompt("Task ID to delete: ")
            if tid.isdigit():
                delete_task(int(tid))
            else:
                print(c("  Invalid ID.", "red"))

        elif choice == "8":
            keyword = prompt("Search keyword: ")
            if keyword:
                print(c(f"\n  ── Search Results for '{keyword}' ──", "cyan", "bold"))
                list_tasks(filter_status="all", search=keyword)
            else:
                print(c("  No keyword entered.", "dim"))

        elif choice == "9":
            pri = prompt("Priority to filter [high/medium/low]: ").lower()
            if pri in PRIORITIES:
                print(c(f"\n  ── Tasks with priority '{pri}' ──", "cyan", "bold"))
                list_tasks(filter_status="all", filter_priority=pri)
            else:
                print(c("  Invalid priority.", "red"))

        elif choice == "10":
            cat = prompt("Category name: ")
            if cat:
                print(c(f"\n  ── Tasks in category '{cat}' ──", "cyan", "bold"))
                list_tasks(filter_status="all", filter_category=cat)
            else:
                print(c("  No category entered.", "dim"))

        elif choice == "11":
            show_stats()

        elif choice == "12":
            filepath = prompt("Export file path (default: tasks_export.json): ", "tasks_export.json")
            export_tasks(filepath)

        elif choice == "13":
            filepath = prompt("Import file path: ")
            if filepath:
                import_tasks(filepath)
            else:
                print(c("  No file path provided.", "dim"))

        else:
            print(c("  ⚠️  Invalid choice. Please try again.", "yellow"))

        print()


# ─────────────────────────────────────────────
# CLI ENTRY POINT (non-interactive / flags)
# ─────────────────────────────────────────────

def print_help():
    print(c("""
  Usage: python todo.py [command] [options]

  Commands:
    (no args)              Launch interactive menu
    add      <title>       Add a task quickly
    list                   List pending tasks
    done     <id>          Mark task complete
    delete   <id>          Delete a task
    stats                  Show statistics
    help                   Show this help message

  Options for 'add':
    --desc       "description"
    --priority   high|medium|low
    --category   "name"
    --due        YYYY-MM-DD

  Examples:
    python todo.py
    python todo.py add "Buy groceries" --priority high --due 2025-06-01
    python todo.py list
    python todo.py done 3
    python todo.py stats
""", "cyan"))


def main():
    init_db()
    args = sys.argv[1:]

    if not args:
        interactive()
        return

    cmd = args[0].lower()

    if cmd in ("help", "--help", "-h"):
        print_banner()
        print_help()

    elif cmd == "add":
        if len(args) < 2:
            print(c("Error: Please provide a task title.", "red"))
            return
        title = args[1]
        desc = ""
        priority = "medium"
        category = "General"
        due_date = None
        i = 2
        while i < len(args):
            if args[i] == "--desc" and i + 1 < len(args):
                desc = args[i + 1]; i += 2
            elif args[i] == "--priority" and i + 1 < len(args):
                priority = args[i + 1]; i += 2
            elif args[i] == "--category" and i + 1 < len(args):
                category = args[i + 1]; i += 2
            elif args[i] == "--due" and i + 1 < len(args):
                due_date = args[i + 1]; i += 2
            else:
                i += 1
        add_task(title, desc, priority, category, due_date)

    elif cmd == "list":
        list_tasks(filter_status="pending")

    elif cmd == "done":
        if len(args) < 2 or not args[1].isdigit():
            print(c("Error: Provide a valid task ID.", "red"))
            return
        complete_task(int(args[1]))

    elif cmd == "delete":
        if len(args) < 2 or not args[1].isdigit():
            print(c("Error: Provide a valid task ID.", "red"))
            return
        delete_task(int(args[1]))

    elif cmd == "stats":
        show_stats()

    else:
        print(c(f"Unknown command: '{cmd}'. Run 'python todo.py help' for usage.", "red"))


if __name__ == "__main__":
    main()
