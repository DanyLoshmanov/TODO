import json
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_TASKS = os.path.join(SCRIPT_DIR, "tasks.json")

STATUS_DONE = "Выполнено"
STATUS_PENDING = "Не выполнено"

# Формат даты и времени — красивый и читаемый
DT_FORMAT = "%d.%m.%Y %H:%M"  # например: 22.11.2025 14:37


class Task:
    """Одна задача с датой создания и завершения"""
    def __init__(self, title, status=STATUS_PENDING, created_at=None, completed_at=None):
        self.title = title.strip()
        self.status = status
        self.created_at = created_at or datetime.now().strftime(DT_FORMAT)
        self.completed_at = completed_at

    def toggle(self):
        self.status = STATUS_DONE if self.status == STATUS_PENDING else STATUS_PENDING
        if self.status == STATUS_DONE and self.completed_at is None:
            self.completed_at = datetime.now().strftime(DT_FORMAT)
        elif self.status == STATUS_PENDING:
            self.completed_at = None  # Сбрасываем дату завершения, если снова "в работе"

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            status=data.get("status", STATUS_PENDING),
            created_at=data.get("created_at"),
            completed_at=data.get("completed_at")
        )

    def __str__(self):
        base = f"{self.title} — {self.status}"
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
            print("Файл задач повреждён. Начинаем с пустого списка.")
            return []

    def _save(self, tasks_data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, indent=4, ensure_ascii=False)

    def get_all(self):
        raw = self._load()
        return [Task.from_dict(task) for task in raw]

    def save_all(self, tasks):
        data = [task.to_dict() for task in tasks]
        self._save(data)


class TodoApp:
    def __init__(self):
        self.repo = TaskRepository()
        self.tasks = self.repo.get_all()

    def add_task(self, title):
        if not title.strip():
            print("Название задачи не может быть пустым.")
            return
        self.tasks.append(Task(title))
        self._save()
        print(f"Задача добавлена {datetime.now().strftime(DT_FORMAT)}")

    def toggle_task(self, index):
        if 0 <= index < len(self.tasks):
            old_status = self.tasks[index].status
            self.tasks[index].toggle()
            self._save()
            new_status = self.tasks[index].status
            action = "завершена" if new_status == STATUS_DONE else "возобновлена"
            print(f"Задача {action} → {new_status}")
        else:
            print("Нет задачи с таким номером.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self._save()
            print(f"Задача «{removed.title}» удалена.")
        else:
            print("Нет задачи с таким номером.")

    def view_tasks(self):
        if not self.tasks:
            print("Список задач пуст.")
            return
        print("\nВаши задачи:")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")

    def _save(self):
        self.repo.save_all(self.tasks)


class ConsoleUI:
    def __init__(self, app):
        self.app = app

    def run(self):
        print(f"Запущено: {datetime.now().strftime(DT_FORMAT)}")
        while True:
            self._show_menu()
            choice = input("\nВыберите действие (1–5): ").strip()

            if choice == "1":
                self.app.view_tasks()

            elif choice == "2":
                title = input("Введите название задачи: ").strip()
                self.app.add_task(title)

            elif choice == "3":
                self.app.view_tasks()
                if self.app.tasks:
                    idx = input("Номер задачи для изменения статуса: ").strip()
                    if idx.isdigit():
                        self.app.toggle_task(int(idx) - 1)
                    else:
                        print("Нужно ввести число.")

            elif choice == "4":
                self.app.view_tasks()
                if self.app.tasks:
                    idx = input("Номер задачи для удаления: ").strip()
                    if idx.isdigit():
                        self.app.delete_task(int(idx) - 1)
                    else:
                        print("Нужно ввести число.")

            elif choice == "5":
                print(f"До свидания! Закрыто: {datetime.now().strftime(DT_FORMAT)}")
                break

            else:
                print("Пожалуйста, выберите от 1 до 5.")

            input("\nНажмите Enter для продолжения...")
            os.system('cls' if os.name == 'nt' else 'clear')  # Очистка экрана (Windows/Linux/Mac)

    @staticmethod
    def _show_menu():
        print("\n" + "=" * 50)
        print("   КРАСИВЫЙ TO-DO LIST С ДАТАМИ И ВРЕМЕНЕМ")
        print("=" * 50)
        print("1. Показать все задачи")
        print("2. Добавить новую задачу")
        print("3. Отметить задачу (выполнено / в работе)")
        print("4. Удалить задачу")
        print("5. Выход")
        print("=" * 50)


def main():
    app = TodoApp()
    ui = ConsoleUI(app)
    ui.run()


if __name__ == "__main__":
    main()