import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_TASKS = os.path.join(SCRIPT_DIR, "tasks.json")

STATUS_DONE = "Выполнено"
STATUS_PENDING = "Не выполнено"

def load_tasks():
    if not os.path.exists(FILE_TASKS):
        return []
    try:
        with open(FILE_TASKS, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks):
    with open(FILE_TASKS, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def add_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "status": STATUS_PENDING})
    save_tasks(tasks)

def toggle_task(index):
    tasks = load_tasks()
    real_index = index - 1
    if 0 <= real_index < len(tasks):
        task = tasks[real_index]
        task["status"] = STATUS_DONE if task["status"] == STATUS_PENDING else STATUS_PENDING
        save_tasks(tasks)

def delete_task(index):
    tasks = load_tasks()
    real_index = index - 1
    if 0 <= real_index < len(tasks):
        tasks.pop(real_index)
        save_tasks(tasks)

def view_tasks():
    tasks = load_tasks()
    return tasks  # для тестов лучше просто возвращать список
