import tkinter as tk
from tkinter import ttk, messagebox
from database_manager import *

class RequestManager:
    def __init__(self, db_manager, add_tab, edit_tab, track_tab, assign_tab, stats_tab, current_user_role):
        self.db_manager = db_manager
        self.add_tab = add_tab
        self.edit_tab = edit_tab
        self.track_tab = track_tab
        self.assign_tab = assign_tab
        self.stats_tab = stats_tab
        self.current_user_role = current_user_role

        # --- UI для добавления заявки ---

    def create_add_request_ui(self):
        labels = ["Дата:", "Оборудование:", "Тип неисправности:", "Описание:", "Клиент:"]
        self.entry_fields = []  # Список для хранения полей ввода
        for i, label_text in enumerate(labels):
            label = tk.Label(self.add_tab, text=label_text)
            label.grid(row=i, column=0, padx=5, pady=5)  # Размещение метки

            entry = tk.Entry(self.add_tab)
            entry.grid(row=i, column=1, padx=5, pady=5)  # Размещение поля ввода
            self.entry_fields.append(entry)  # Добавляем поле ввода в список

        add_button = tk.Button(self.add_tab, text="Добавить заявку", command=self.add_request)
        add_button.grid(row=len(labels), column=0, columnspan=2, pady=10)  # Размещение кнопки

    def add_request(self):
        data = [entry.get() for entry in self.entry_fields] + ["В ожидании"]
        self.db_manager.add_request(data)

        for entry in self.entry_fields:
            entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Заявка добавлена!")

    # --- UI для редактирования заявки ---

    def create_edit_request_ui(self):
        # Поиск заявки
        tk.Label(self.edit_tab, text="ID заявки:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.edit_tab)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        search_button = tk.Button(self.edit_tab, text="Найти", command=self.search_request)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        # Поля для редактирования
        labels = ["Статус:", "Описание:", "Назначенный техник:"]
        self.edit_fields = []
        for i, label_text in enumerate(labels):
            label = tk.Label(self.edit_tab, text=label_text)
            label.grid(row=i+1, column=0, padx=5, pady=5)
            entry = tk.Entry(self.edit_tab)
            entry.grid(row=i+1, column=1, columnspan=2, padx=5, pady=5)
            self.edit_fields.append(entry)

        # Checkboxes for request status
        status_label = tk.Label(self.edit_tab, text="Статус:")
        status_label.grid(row=len(labels)+1, column=0, padx=5, pady=5)

        self.edit_status_var = tk.StringVar()  # Variable to store selected status for editing

        status_options = ["В ожидании", "В работе", "Выполнено"]
        for i, status in enumerate(status_options):
            checkbox = tk.Checkbutton(self.edit_tab, text=status, variable=self.edit_status_var, 
                                    onvalue=status, offvalue="", command=self.update_status_entry)
            checkbox.grid(row=len(labels)+1, column=i+1, padx=5, pady=5)

        update_button = tk.Button(self.edit_tab, text="Обновить", command=self.edit_request)
        update_button.grid(row=len(labels)+2, column=0, columnspan=len(status_options)+1, pady=10, sticky=tk.W+tk.E)

        # Ограничение доступа
        if self.current_user_role != "admin":
            self.edit_fields[2].config(state="disabled")  # Только админ может менять техника

    def update_status_entry(self):
        self.edit_fields[0].delete(0, tk.END)
        self.edit_fields[0].insert(0, self.edit_status_var.get()) 

    def update_status_entry(self):
        self.edit_fields[0].delete(0, tk.END)
        self.edit_fields[0].insert(0, self.edit_status_var.get())

    def search_request(self):
        request_id = self.search_entry.get()
        try:
            request_id = int(request_id)
            request_data = self.db_manager.get_requests(f"id = {request_id}")
            if request_data:
                request_data = request_data[0]
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, str(request_id))  # Заполняем ID заявки
                num_fields = len(self.edit_fields)
                for i in range(num_fields):
                    field = self.edit_fields[i]
                    field.delete(0, tk.END)
                    if i == 0:  # Статус
                        field.insert(0, str(request_data[6]))
                    elif i == 1:  # Описание
                        field.insert(0, str(request_data[4]))
                    elif i == 2:  # Назначенный техник
                        field.insert(0, str(request_data[7]))
            else:
                messagebox.showerror("Ошибка", "Заявка не найдена!")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный ID заявки!")
    def edit_request(self):
        request_id = self.search_entry.get()
        data = {
            "status": self.edit_fields[0].get(),
            "description": self.edit_fields[1].get(),
            "assigned_to": self.edit_fields[2].get()
        }
        try:
            request_id = int(request_id)
            self.db_manager.update_request(request_id, data)
            messagebox.showinfo("Успех", "Заявка обновлена!")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный ID заявки!")

    # --- UI для отслеживания статуса ---

    def create_track_status_ui(self):
        self.requests_listbox = tk.Listbox(self.track_tab)
        self.requests_listbox.pack(fill="both", expand=True)

        update_button = tk.Button(self.track_tab, text="Обновить", command=self.update_request_list)
        update_button.pack()

        details_button = tk.Button(self.track_tab, text="Показать детали", command=self.show_request_details)
        details_button.pack()

        self.update_request_list()

    def update_request_list(self):
        self.requests_listbox.delete(0, tk.END)
        requests = self.db_manager.get_requests()
        for request in requests:
            self.requests_listbox.insert(tk.END, f"ID: {request[0]} - {request[5]} - {request[6]}")

    def show_request_details(self):
        selection = self.requests_listbox.curselection()
        if selection:
            request_id = int(self.requests_listbox.get(selection[0]).split()[1])
            request_data = self.db_manager.get_requests(f"id = {request_id}")[0]

            details_window = tk.Toplevel(self.track_tab)
            details_window.title(f"Детали заявки {request_id}")
            details_window.geometry("300x300")
            details_window.update_idletasks()
            screen_width = details_window.winfo_screenwidth()
            screen_height = details_window.winfo_screenheight()
            window_width = details_window.winfo_width()
            window_height = details_window.winfo_height()
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            details_window.geometry(f"+{x}+{y}")

            # Вывод деталей заявки
            for i, value in enumerate(request_data):
                tk.Label(details_window, text=f"{self.db_manager.cursor.description[i][0]}: {value}").pack()

        else:
            messagebox.showwarning("Внимание", "Выберите заявку для просмотра деталей.")