import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# --- Настройки ---
HISTORY_FILE = "tasks.json"
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
    {"text": "Посмотреть обучающее видео", "type": "учёба"},
    {"text": "Разобрать почту", "type": "работа"},
    {"text": "Погулять на свежем воздухе", "type": "отдых"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Загрузка задач из файла или создание нового
        self.tasks = self.load_tasks()

        # --- Создание виджетов ---
        # Текущая задача
        self.current_task_label = tk.Label(
            self.root, text="Нажмите кнопку, чтобы получить задачу", 
            font=("Arial", 12), wraplength=450, bg="#f0f0f0", relief="solid", pady=10
        )
        self.current_task_label.pack(pady=10, fill=tk.X)

        # Кнопка генерации
        self.generate_btn = ttk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        # Фильтр по типу
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar(value="все")
        filter_options = ["все", "учёба", "спорт", "работа", "отдых"]
        
        for opt in filter_options:
            ttk.Radiobutton(filter_frame, text=opt.capitalize(), variable=self.filter_var, 
                            value=opt, command=self.update_history_list).pack(side=tk.LEFT, padx=2)

        # История задач (Listbox)
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, height=10, font=("Arial", 10))
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Добавление новой задачи
        add_frame = tk.LabelFrame(self.root, text="Добавить новую задачу", pady=10)
        add_frame.pack(padx=10, pady=10, fill=tk.X)

        tk.Label(add_frame, text="Задача:").grid(row=0, column=0, sticky="e")
        self.new_task_entry = ttk.Entry(add_frame, width=30)
        self.new_task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Тип:").grid(row=1, column=0, sticky="e")
        self.new_task_type = ttk.Combobox(add_frame, values=["учёба", "спорт", "работа", "отдых"], state="readonly")
        self.new_task_type.set("учёба")
        self.new_task_type.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(add_frame, text="Добавить", command=self.add_new_task).grid(row=2, columnspan=2, pady=10)

    def load_tasks(self):
        """Загружает задачи из JSON-файла или создаёт новый с дефолтными."""
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Если файл не существует или повреждён — создаём новый
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_TASKS.copy(), f, ensure_ascii=False, indent=2)
        
        return DEFAULT_TASKS.copy()

    def save_tasks(self):
        """Сохраняет текущий список задач в JSON-файл."""
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def generate_task(self):
        """Выбирает и отображает случайную задачу."""
        if not self.tasks:
            messagebox.showwarning("Предупреждение", "Список задач пуст! Добавьте новые задачи.")
            return

        selected_task = random.choice(self.tasks)
        
        self.current_task_label.config(
            text=f"Задача: {selected_task['text']}\nТип: {selected_task['type'].capitalize()}",
            bg="#e6ffe6"  # Зелёный фон для выделения
        )

    def add_new_task(self):
        """Добавляет новую задачу с валидацией."""
        task_text = self.new_task_entry.get().strip()
        
        if not task_text:
            messagebox.showerror("Ошибка", "Поле задачи не может быть пустым!")
            return

        task_type = self.new_task_type.get()
        
        new_task = {"text": task_text, "type": task_type}
        
        # Добавляем в начало списка (самые новые — сверху в истории)
        self.tasks.insert(0, new_task)
        
        self.save_tasks()
        
        # Обновляем историю и очищаем поле ввода
        self.update_history_list()
        self.new_task_entry.delete(0, tk.END)

    def update_history_list(self):
        """Обновляет список истории с учётом фильтра."""
        self.history_listbox.delete(0, tk.END)
        
        filter_type = self.filter_var.get()
        
        for task in reversed(self.tasks):  # Показываем от новых к старым
            if filter_type == "все" or task["type"] == filter_type:
                self.history_listbox.insert(tk.END, f"{task['text']} ({task['type']})")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    app.update_history_list()  # Первоначальная загрузка истории
    root.mainloop()
