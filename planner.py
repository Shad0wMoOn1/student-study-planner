"""Вспомогательный пример: сортировка задач и определение просрочки. Python 3."""
import argparse
import csv
from datetime import date

DEMO_TASKS = [
    {"id": "1", "title": "Подготовить требования", "course": "Тестирование ПО",
     "due": "2026-11-24", "priority": "1", "status": "Готово"},
    {"id": "2", "title": "Сделать макет интерфейса", "course": "Тестирование ПО",
     "due": "2026-11-25", "priority": "1", "status": "В работе"},
    {"id": "3", "title": "Проверить экспорт задач", "course": "Тестирование ПО",
     "due": "2026-12-03", "priority": "2", "status": "Очередь"},
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="CSV с полями id,title,course,due,priority,status")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(),
                        help="Дата проверки в формате ГГГГ-ММ-ДД")
    args = parser.parse_args()
    try:
        tasks = DEMO_TASKS
        if args.csv:
            with open(args.csv, newline="", encoding="utf-8-sig") as stream:
                tasks = list(csv.DictReader(stream))
        checked = []
        ids = set()
        for task in tasks:
            if not all(task.get(k, "").strip() for k in
                       ("id", "title", "course", "due", "priority", "status")):
                raise ValueError("Все шесть полей задачи должны быть заполнены")
            if task["id"] in ids:
                raise ValueError("Идентификаторы задач должны быть уникальны")
            ids.add(task["id"])
            due = date.fromisoformat(task["due"])
            priority = int(task["priority"])
            if priority not in (1, 2, 3):
                raise ValueError("Приоритет должен быть равен 1, 2 или 3")
            if task["status"] not in ("Очередь", "В работе", "Готово"):
                raise ValueError("Неизвестное состояние задачи")
            if not 1 <= len(task["title"].strip()) <= 120:
                raise ValueError("Название должно содержать 1–120 символов")
            checked.append((due, priority, task))
        for due, priority, task in sorted(checked, key=lambda row: (row[0], row[1], row[2]["id"])):
            overdue = due < args.today and task["status"] != "Готово"
            mark = "ПРОСРОЧЕНО" if overdue else task["status"]
            print(f"{due} | P{priority} | {mark} | {task['title']}")
        if not checked:
            print("Задач пока нет")
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
