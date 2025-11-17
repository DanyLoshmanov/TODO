import json, os

FILE_TASKS = "tasks.json"

def load_tasks():
    if os.path.exists(FILE_TASKS):
        with open(FILE_TASKS, "r", encoding='utf-8') as file:
            return json.load(file)
    else:
        raise FileNotFoundError("Файл не найден!")
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
    if 0 <= idx < len(tasks):
        if tasks[idx]["Статус"] == "Не выполнено":
            tasks[idx]["Статус"] = "Выполнено"
        else:
            tasks[idx]["Статус"] = "Не выполнено"
        save_tasks(tasks)
        print(f"Статус задачи '{tasks[idx]["Задача: "]}' изменен на на {tasks[idx]["Статус: "]}")
    else:
        print("Нет задач с таким номером!")