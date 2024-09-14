import datetime
import json


class Task:
    """Класс для управления задачами."""
    def __init__(self, title, deadline, status="Pending"):
        self.title = title
        self.deadline = deadline
        self.status = status

    def mark_done(self):
        self.status = "Done"

    def __str__(self):
        return f"{self.title} ({self.deadline:%Y-%m-%d}): {self.status}"


def parse_date(date_str):
    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError("no valid date format found")


def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks_data = json.load(file)
            return [Task(task['title'], datetime.datetime.strptime(task['deadline'], '%Y-%m-%d'),
                         task['status']) for task in tasks_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump([{'title': task.title, 'deadline': task.deadline.strftime('%Y-%m-%d'),
                    'status': task.status} for task in tasks], file, indent=4, ensure_ascii=False)


def add_task(tasks):
    title = input("Введите название задачи: ")
    if not title:
        print("Название задачи не может быть пустым.")
        return
    deadline_str = input("Введите срок выполнения (форматы ДД-ММ-ГГГГ или ГГГГ-ММ-ДД): ")
    try:
        deadline = parse_date(deadline_str)
    except ValueError:
        print("Неверный формат даты. Пожалуйста, попробуйте снова.")
        return
    tasks.append(Task(title, deadline))
    save_tasks(tasks)


def edit_task(tasks):
    for index, task in enumerate(tasks):
        print(f"{index + 1}. {task}")
    task_number = int(input("Введите номер задачи для редактирования: ")) - 1
    if 0 <= task_number < len(tasks):
        title = input("Введите новое название задачи (оставьте пустым для сохранения): ")
        if title:
            tasks[task_number].title = title
        deadline_str = input("Введите новый срок выполнения (оставьте пустым для сохранения,"
                             " форматы ДД-ММ-ГГГГ или ГГГГ-ММ-ДД): ")
        if deadline_str:
            try:
                deadline = parse_date(deadline_str)
                tasks[task_number].deadline = deadline
            except ValueError:
                print("Неверный формат даты. Пожалуйста, попробуйте снова.")
                return
        status_str = input("Установить статус задачи как 'Done'? (да/нет): ")
        if status_str.lower() == "да":
            tasks[task_number].mark_done()
        save_tasks(tasks)
    else:
        print("Нет задачи с таким номером.")


def delete_task(tasks):
    for index, task in enumerate(tasks):
        print(f"{index + 1}. {task}")
    task_number = int(input("Введите номер задачи для удаления: ")) - 1
    if 0 <= task_number < len(tasks):
        del tasks[task_number]
        save_tasks(tasks)
    else:
        print("Нет задачи с таким номером.")


def clear_completed_tasks(tasks):
    tasks[:] = [task for task in tasks if task.status != "Done"]
    save_tasks(tasks)
    print("Выполненные задачи удалены.")


def show_all_tasks(tasks):
    if not tasks:
        print("Список задач пуст")
    else:
        print("\n".join(str(task) for task in tasks))


def main():
    tasks = load_tasks()
    actions = {
        "1": lambda: add_task(tasks),
        "2": lambda: show_all_tasks(tasks),
        "3": lambda: edit_task(tasks),
        "4": lambda: delete_task(tasks),
        "5": lambda: clear_completed_tasks(tasks),
        "6": exit
    }
    while True:
        print("\n1. Добавить задачу\n2. Показать все задачи\n3. Редактировать задачу"
              "\n4. Удалить задачу\n5. Очистить выполненные задачи\n6. Выход")
        choice = input("Выберите действие: ")
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
