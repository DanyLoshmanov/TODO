# todo.py
import json
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_TASKS = os.path.join(SCRIPT_DIR, "tasks.json")

# Статусы
STATUS_DONE = "Выполнено"
STATUS_PENDING = "Не выполнено"

# Приоритеты
PRIORITY_HIGH = 1
PRIORITY_MEDIUM = 2
PRIORITY_LOW = 3

PRIORITY_NAMES = {
    PRIORITY_HIGH: "Высокий",
    PRIORITY_MEDIUM: "Средний",
    PRIORITY_LOW: "Низкий"
}

PRIORITY_EMOJI = {
    PRIORITY_HIGH: "High priority",
    PRIORITY_MEDIUM: "Medium priority",
    PRIORITY_LOW: "Low priority"
}

DT_FORMAT = "%d.%m.%Y %H:%M"


class Task:
    def __init__(self, title, status=STATUS_PENDING, priority=PRIORITY_MEDIUM,
                 created_at=None, completed_at=None):
        self.title = title.strip()
        self.status = status
        self.priority = priority
        self.created_at = created_at or datetime.now().strftime(DT_FORMAT)
        self.completed_at = completed_at

    def toggle(self):
        if self.status == STATUS_PENDING:
            self.status = STATUS_DONE
            if self.completed_at is None:
                self.completed_at = datetime.now().strftime(DT_FORMAT)
        else:
            self.status = STATUS_PENDING
            self.completed_at = None

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            status=data.get("status", STATUS_PENDING),
            priority=data.get("priority", PRIORITY_MEDIUM),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at")
        )

    def __str__(self):
        emoji = PRIORITY_EMOJI[self.priority]
        prio = f"{emoji} {PRIORITY_NAMES[self.priority]}"
        base = f"{self.title} — {self.status} [{prio}]"
        info = f" (создана: {self.created_at}"
        if self.completed_at:
            info += f", завершена: {self.completed_at})"
        else:
            info += ")"
        return base + info


class TaskRepository:
    def __init__(self, file_path=FILE_TASKS):
        self.file_path = file_path

    def _load(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Ошибка чтения tasks.json. Создаём новый список.")
            return []

    def _save(self, tasks_data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, indent=4, ensure_ascii=False)

    def get_all(self):
        raw = self._load()
        return [Task.from_dict(t) for t in raw]

    def save_all(self, tasks):
        data = [t.to_dict() for t in tasks]
        self._save(data)


class TodoApp:
    def __init__(self):
        self.repo = TaskRepository()
        self.tasks = self.repo.get_all()
        self._sort_tasks()

    def _sort_tasks(self):
        self.tasks.sort(key=lambda t: (t.priority, t.created_at))

    def add_task(self, title, priority=PRIORITY_MEDIUM):
        if not title.strip():
            print("Ошибка: название задачи не может быть пустым!")
            return False
        self.tasks.append(Task(title, priority=priority))
        self._sort_tasks()
        self.repo.save_all(self.tasks)
        print(f"Задача добавлена → {PRIORITY_EMOJI[priority]} {PRIORITY_NAMES[priority]}")
        return True

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            old_status = self.tasks[index].status
            self.tasks[index].toggle()
            self._sort_tasks()
            self.repo.save_all(self.tasks)
            action = "завершена" if self.tasks[index].status == STATUS_DONE else "возобновлена"
            print(f"Задача «{self.tasks[index].title}» {action}")
        else:
            print("Задача с таким номером не найдена.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.repo.save_all(self.tasks)
            print(f"Задача «{removed.title}» удалена.")
        else:
            print("Задача с таким номером не найдена.")

    def view_tasks(self):
        if not self.tasks:
            print("Список задач пуст. Добавьте первую задачу!")
            return
        print("\nВаши задачи (отсортированы по приоритету):")
        print("─" * 90)
        for i, task in enumerate(self.tasks, 1):
            print(f"{i:2}. {task}")
        print("─" * 90)


class ConsoleUI:
    def __init__(self, app):
        self.app = app

    def run(self):
        self.clear()
        print(f"Запущено: {datetime.now().strftime(DT_FORMAT)}\n")
        while True:
            self.show_menu()
            choice = input("Выберите действие (1–5): ").strip()

            if choice == "1":
                self.clear()
                self.app.view_tasks()

            elif choice == "2":
                self.clear()
                title = input("Название новой задачи:\n➤ ").strip()
                if not title:
                    print("Задача не добавлена — название пустое.")
                    input("\nНажмите Enter...")
                    continue

                print("\nПриоритет:")
                print(f"1. {PRIORITY_EMOJI[1]} Высокий (срочно)")
                print(f"2. {PRIORITY_EMOJI[2]} Средний (по умолчанию)")
                print(f"3. {PRIORITY_EMOJI[3]} Низкий")
                prio = input("\nВыбор (1–3, Enter = 2): ").strip()

                if prio == "1":
                    priority = PRIORITY_HIGH
                elif prio == "3":
                    priority = PRIORITY_LOW
                else:
                    priority = PRIORITY_MEDIUM

                self.app.add_task(title, priority)

            elif choice == "3":
                self.clear()
                self.app.view_tasks()
                if self.app.tasks:
                    idx = input("\nНомер задачи для изменения статуса: ").strip()
                    if idx.isdigit():
                        self.app.toggle_task(int(idx) - 1)
                    else:
                        print("Введите корректный номер.")

            elif choice == "4":
                self.clear()
                self.app.view_tasks()
                if self.app.tasks:
                    idx = input("\nНомер задачи для удаления: ").strip()
                    if idx.isdigit():
                        self.app.delete_task(int(idx) - 1)
                    else:
                        print("Введите корректный номер.")

            elif choice == "5":
                self.clear()
                print(f"До свидания! Закрыто: {datetime.now().strftime(DT_FORMAT)}\n")
                break

            else:
                print("Выберите число от 1 до 5.")

            input("\nНажмите Enter для продолжения...")
            self.clear()

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def show_menu():
        print("=" * 55)
        print("   КОНСОЛЬНЫЙ TO-DO LIST С ПРИОРИТЕТАМИ")
        print("=" * 55)
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Отметить задачу")
        print("4. Удалить задачу")
        print("5. Выход")
        print("=" * 55)


def main():
    app = TodoApp()
    ui = ConsoleUI(app)
    ui.run()


if __name__ == "__main__":
    main()