import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_TASKS = os.path.join(SCRIPT_DIR, "tasks.json")

def load_tasks():
    if not os.path.exists(FILE_TASKS):
        return []
    
    try:
        with open(FILE_TASKS, "r", encoding='utf-8') as file:
            return json.load(file)                    
    except:                                               
        print("Файл tasks.json повреждён или пустой — создаём новый список задач.")
        return []                                          

def save_tasks(tasks):
    with open(FILE_TASKS, "w", encoding='utf-8') as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)
        
def add_task(title):
    tasks = load_tasks()
    tasks.append({"Задача: ": title, "Статус": "Не выполнено"})
    save_tasks(tasks)
    
def toggle_task(idx):
    tasks = load_tasks()
    
    real_idx = idx - 1
    if 0 <= real_idx < len(tasks):
        if tasks[real_idx]["Статус"] == "Не выполнено":
            tasks[real_idx]["Статус"] = "Выполнено"
        else:
            tasks[real_idx]["Статус"] = "Не выполнено"
        save_tasks(tasks)
        print(f"Статус задачи '{tasks[real_idx]['Задача: ']}' изменён на {tasks[real_idx]['Статус']}")
    else:
        print("Нет задач с таким номером!")
        
def delete_task(idx):
    tasks = load_tasks()
    real_idx = idx - 1
    if 0 <= real_idx < len(tasks):
        removed_tasks = tasks.pop(real_idx)
        save_tasks(tasks)
        print(f"Задача '{removed_tasks['Задача: ']}' удалена.")
    else:
        print("Нет задач с таким номером.")
        
def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Список задач пуст!")
    else:
        for i, task in enumerate(tasks):
            print(f"{i}. {task['Задача: ']} — {task['Статус']}")
        
def main():
    while True:
        print("\n--- To-Do List ---")
        print("1. Список задач.")
        print("2. Добавить задачу.")
        print("3. Изменить статус задачи.")
        print("4. Удалить задачу.")
        print("5. Выход")
        
        choice = input("Выберите действие(1-5): ")
        
        if choice == "1":
            view_tasks()
        elif choice == "2":
            title = input("Введите название задачи: ")
            if title.strip():
                add_task(title)
                print(f"Задача {title} успешно добавлена!")
            else:
                print("Задача не может быть пустой!")
        elif choice == "3":
            view_tasks()
            idx = input("Введите номер задачи для изменения статуса: ")
            try:
                toggle_task(int(idx)) 
            except ValueError:
                print("Нужно ввести число!")
        elif choice == "4":
            view_tasks()
            idx = input("Введите номер задачи для удаления: ")
            try:
                delete_task(int(idx))
            except ValueError:
                print("Нужно ввести число!")
        elif choice == "5":
            print("Выход из программы!")
            break
        else:
            print("Некорректный выбор действия!")
            
if __name__ == "__main__":
    main()