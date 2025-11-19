import json
import os
import tasks


def test_add_task(tmp_path):
    # Подменяем путь к JSON-файлу
    tasks.FILE_TASKS = tmp_path / "tasks.json"

    tasks.add_task("Купить молоко")
    data = tasks.load_tasks()

    assert len(data) == 1
    assert data[0]["title"] == "Купить молоко"
    assert data[0]["status"] == tasks.STATUS_PENDING


def test_toggle_task(tmp_path):
    tasks.FILE_TASKS = tmp_path / "tasks.json"

    tasks.add_task("Задача")
    tasks.toggle_task(1)

    data = tasks.load_tasks()
    assert data[0]["status"] == tasks.STATUS_DONE

    tasks.toggle_task(1)

    data = tasks.load_tasks()
    assert data[0]["status"] == tasks.STATUS_PENDING


def test_delete_task(tmp_path):
    tasks.FILE_TASKS = tmp_path / "tasks.json"

    tasks.add_task("Удалить меня")
    tasks.delete_task(1)

    data = tasks.load_tasks()
    assert len(data) == 0


def test_load_tasks_with_broken_json(tmp_path):
    bad_file = tmp_path / "tasks.json"
    bad_file.write_text("Не JSON", encoding="utf-8")

    tasks.FILE_TASKS = bad_file

    result = tasks.load_tasks()
    assert result == []  # должен вернуть пустой список


def test_save_and_load_consistency(tmp_path):
    tasks.FILE_TASKS = tmp_path / "tasks.json"

    original = [
        {"title": "A", "status": tasks.STATUS_PENDING},
        {"title": "B", "status": tasks.STATUS_DONE},
    ]
    tasks.save_tasks(original)

    loaded = tasks.load_tasks()
    assert loaded == original
