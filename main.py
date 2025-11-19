import json
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_TASKS = os.path.join(SCRIPT_DIR, "tasks.json")

STATUS_DONE = "Выполнено"
STATUS_PENDING = "Не выполнено"


def load_tasks():
    """
    Загружает список задач из файла tasks.json.
    Возвращает пустой список, если файл отсутствует или поврежден.
    """
    if not os.path.exists(FILE_TASKS):
        return []

    try:
        with open(FILE_TASKS, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Файл tasks.json повреждён или пустой. Создан новый список задач.")
        return []


def save_tasks(tasks):
    """
    Сохраняет список задач в файл tasks.json.
    """
    with open(FILE_TASKS, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def add_task(title):
    """
    Добавляет новую задачу в список.
    """
    tasks = load_tasks()
    tasks.append({
        "title": title,
        "status": STATUS_PENDING
    })
    save_tasks(tasks)


def toggle_task(index):
    """
    Переключает статус задачи по индексу (1-based).
    """
    tasks = load_tasks()
    real_index = index - 1

    if 0 <= real_index < len(tasks):
        task = tasks[real_index]
        task["status"] = STATUS_DONE if task["status"] == STATUS_PENDING else STATUS_PENDING
        save_tasks(tasks)
        print(f"Статус задачи '{task['title']}' изменён на {task['status']}.")
    else:
        print("Нет задачи с таким номером.")


def delete_task(index):
    """
    Удаляет задачу по индексу (1-based).
    """
    tasks = load_tasks()
    real_index = index - 1

    if 0 <= real_index < len(tasks):
        removed = tasks.pop(real_index)
        save_tasks(tasks)
        print(f"Задача '{removed['title']}' удалена.")
    else:
        print("Нет задачи с таким номером.")


def view_tasks():
    """
    Выводит список всех задач.
    """
    tasks = load_tasks()

    if not tasks:
        print("Список задач пуст.")
        return

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['title']} — {task['status']}")


def main():
    """
    Точка входа в программу.
    """
    while True:
        print("\n--- To-Do List ---")
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Изменить статус задачи")
        print("4. Удалить задачу")
        print("5. Выход")

        choice = input("Выберите действие (1–5): ")

        if choice == "1":
            view_tasks()

        elif choice == "2":
            title = input("Введите название задачи: ").strip()
            if title:
                add_task(title)
                print("Задача успешно добавлена.")
            else:
                print("Название задачи не может быть пустым.")

        elif choice == "3":
            view_tasks()
            idx = input("Введите номер задачи: ")
            if idx.isdigit():
                toggle_task(int(idx))
            else:
                print("Нужно ввести число.")

        elif choice == "4":
            view_tasks()
            idx = input("Введите номер задачи: ")
            if idx.isdigit():
                delete_task(int(idx))
            else:
                print("Нужно ввести число.")

        elif choice == "5":
            print("Выход из программы...")
            break

        else:
            print("Некорректный выбор действия.")


if __name__ == "__main__":
    main()
