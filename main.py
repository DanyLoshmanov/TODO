import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_TASKS = os.path.join(SCRIPT_DIR, "tasks.json")

STATUS_DONE = "Выполнено"
STATUS_PENDING = "Не выполнено"


class Task:
    """Одна задача"""
    def __init__(self, title, status=STATUS_PENDING):
        self.title = title.strip()
        self.status = status

    def toggle(self):
        """Меняет статус на противоположный"""
        self.status = STATUS_DONE if self.status == STATUS_PENDING else STATUS_PENDING

    def to_dict(self):
        return {"title": self.title, "status": self.status}

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data.get("status", STATUS_PENDING))

    def __str__(self):
        return f"{self.title} — {self.status}"


class TaskRepository:
    """Работа только с файлом tasks.json"""
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
    """Вся логика приложения"""
    def __init__(self):
        self.repo = TaskRepository()
        self.tasks = self.repo.get_all()

    def add_task(self, title):
        if not title.strip():
            print("Название задачи не может быть пустым.")
            return
        self.tasks.append(Task(title))
        self._save()
        print("Задача успешно добавлена.")

    def toggle_task(self, index):  # index — 0-based
        if 0 <= index < len(self.tasks):
            self.tasks[index].toggle()
            self._save()
            print(f"Статус изменён на {self.tasks[index].status}.")
        else:
            print("Нет задачи с таким номером.")

    def delete_task(self, index):  # index — 0-based
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
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. {task}")

    def _save(self):
        self.repo.save_all(self.tasks)


class ConsoleUI:
    """Интерфейс в консоли"""
    def __init__(self, app):
        self.app = app

    def run(self):
        while True:
            self._show_menu()
            choice = input("Выберите действие (1–5): ").strip()

            if choice == "1":
                self.app.view_tasks()

            elif choice == "2":
                title = input("Введите название задачи: ").strip()
                self.app.add_task(title)

            elif choice == "3":
                self.app.view_tasks()
                idx = input("Введите номер задачи: ").strip()
                if idx.isdigit():
                    self.app.toggle_task(int(idx) - 1)
                else:
                    print("Нужно ввести число.")

            elif choice == "4":
                self.app.view_tasks()
                idx = input("Введите номер задачи: ").strip()
                if idx.isdigit():
                    self.app.delete_task(int(idx) - 1)
                else:
                    print("Нужно ввести число.")

            elif choice == "5":
                print("До свидания!")
                break

            else:
                print("Некорректный выбор.")

    @staticmethod
    def _show_menu():
        print("\n" + "=" * 30)
        print("   To-Do List")
        print("=" * 30)
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Изменить статус задачи")
        print("4. Удалить задачу")
        print("5. Выход")


def main():
    app = TodoApp()
    ui = ConsoleUI(app)
    ui.run()


if __name__ == "__main__":
    main()