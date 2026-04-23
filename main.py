import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")

        # Предопределённые задачи
        self.tasks = {
            "учёба": ["Прочитать статью", "Сделать конспект", "Решить задачу"],
            "спорт": ["Сделать зарядку", "Пробежать 5 км", "Посетить тренажёрный зал"],
            "работа": ["Написать отчёт", "Подготовить презентацию", "Провести встречу"]
        }

        # История задач
        self.history = []

        # Загрузка истории из файла
        self.load_history()

        # GUI элементы
        self.create_widgets()

    def create_widgets(self):
        # Кнопка генерации задачи
        self.generate_button = tk.Button(
            self.root,
            text="Сгенерировать задачу",
            command=self.generate_task
        )
        self.generate_button.pack(pady=10)

        # Выпадающий список для фильтрации
        self.filter_label = tk.Label(self.root, text="Фильтр по типу:")
        self.filter_label.pack()
        self.filter_var = tk.StringVar()
        self.filter_combobox = ttk.Combobox(
            self.root,
            textvariable=self.filter_var,
            values=["все", "учёба", "спорт", "работа"]
        )
        self.filter_combobox.current(0)
        self.filter_combobox.pack(pady=5)

        # Поле для добавления новой задачи
        self.new_task_label = tk.Label(self.root, text="Добавить новую задачу:")
        self.new_task_label.pack()
        self.new_task_entry = tk.Entry(self.root, width=40)
        self.new_task_entry.pack(pady=5)

        # Выпадающий список для выбора типа новой задачи
        self.new_task_type_label = tk.Label(self.root, text="Тип задачи:")
        self.new_task_type_label.pack()
        self.new_task_type_var = tk.StringVar()
        self.new_task_type_combobox = ttk.Combobox(
            self.root,
            textvariable=self.new_task_type_var,
            values=["учёба", "спорт", "работа"]
        )
        self.new_task_type_combobox.current(0)
        self.new_task_type_combobox.pack(pady=5)

        # Кнопка добавления задачи
        self.add_task_button = tk.Button(
            self.root,
            text="Добавить задачу",
            command=self.add_task
        )
        self.add_task_button.pack(pady=5)

        # История задач
        self.history_label = tk.Label(self.root, text="История задач:")
        self.history_label.pack()
        self.history_listbox = tk.Listbox(self.root, width=50, height=10)
        self.history_listbox.pack(pady=10)

        # Обновление истории
        self.update_history()

    def generate_task(self):
        filter_type = self.filter_var.get()
        if filter_type == "все":
            all_tasks = []
            for task_type in self.tasks:
                all_tasks.extend(self.tasks[task_type])
            task = random.choice(all_tasks)
        else:
            task = random.choice(self.tasks[filter_type])

        self.history.append(task)
        self.update_history()
        self.save_history()

    def add_task(self):
        new_task = self.new_task_entry.get().strip()
        task_type = self.new_task_type_var.get()

        if not new_task:
            messagebox.showerror("Ошибка", "Задача не может быть пустой!")
            return

        self.tasks[task_type].append(new_task)
        self.new_task_entry.delete(0, tk.END)

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for task in self.history:
            self.history_listbox.insert(tk.END, task)

    def save_history(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r", encoding="utf-8") as f:
                self.history = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
