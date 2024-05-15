import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import CTkListbox
import sqlite3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Создание базы данных и таблицы (если они не существуют)
def create_database():
    conn = sqlite3.connect('repair_requests.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_type TEXT,
            serial_number TEXT,
            description TEXT,
            priority TEXT,
            assigned_to TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Функция для центрирования окна
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'+{x}+{y}')

# Создание нового окна для добавления заявки
def add_request_window():
    add_window = ctk.CTkToplevel(root)
    add_window.title("Новая заявка")

    # Поля ввода
    equipment_type_label = ctk.CTkLabel(add_window, text="Тип оборудования:")
    equipment_type_entry = ctk.CTkEntry(add_window)
    serial_number_label = ctk.CTkLabel(add_window, text="Серийный номер:")
    serial_number_entry = ctk.CTkEntry(add_window)
    description_label = ctk.CTkLabel(add_window, text="Описание проблемы:")
    description_entry = ctk.CTkTextbox(add_window)
    
    priority_label = ctk.CTkLabel(add_window, text="Приоритет:")
    priority_combobox = ctk.CTkComboBox(add_window, values=["Низкий", "Средний", "Высокий"])
    assigned_to_label = ctk.CTkLabel(add_window, text="Назначен:")
    assigned_to_combobox = ctk.CTkComboBox(add_window, values=["Иванов", "Куватов", "Леванюк"])

    # Центрирование окна добавления заявки
    center_window(add_window)

    # Функция сохранения заявки
    def save_request():
        equipment_type = equipment_type_entry.get()
        serial_number = serial_number_entry.get()
        description = description_entry.get("1.0", ctk.END).strip()
        priority = priority_combobox.get()
        assigned_to = assigned_to_combobox.get()

        # Проверка на пустые поля
        if not all([equipment_type, serial_number, description, priority, assigned_to]):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        # Сохранение в базу данных
        conn = sqlite3.connect('repair_requests.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO requests (equipment_type, serial_number, description, priority, assigned_to)
            VALUES (?, ?, ?, ?, ?)
        ''', (equipment_type, serial_number, description, priority, assigned_to))
        conn.commit()
        conn.close()

        # Очистка полей ввода
        equipment_type_entry.delete(0, ctk.END)
        serial_number_entry.delete(0, ctk.END)
        description_entry.delete("1.0", ctk.END)
        priority_combobox.set("")
        assigned_to_combobox.set("")

        # Обновление списка заявок
        update_request_list()

    # Размещение элементов
    equipment_type_label.grid(row=0, column=0, padx=5, pady=5)
    equipment_type_entry.grid(row=0, column=1, padx=5, pady=5)
    serial_number_label.grid(row=1, column=0, padx=5, pady=5)
    serial_number_entry.grid(row=1, column=1, padx=5, pady=5)
    description_label.grid(row=2, column=0, padx=5, pady=5)
    description_entry.grid(row=2, column=1, padx=5, pady=5)
    priority_label.grid(row=3, column=0, padx=5, pady=5)
    priority_combobox.grid(row=3, column=1, padx=5, pady=5)
    assigned_to_label.grid(row=4, column=0, padx=5, pady=5)
    assigned_to_combobox.grid(row=4, column=1, padx=5, pady=5)

    # Кнопка "Сохранить"
    save_button = ctk.CTkButton(add_window, text="Сохранить", command=save_request)
    save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Функция отображения полной информации о заявке
def show_request_details(event):
    
        # Получаем индекс выбранной строки
        selection = request_list.curselection()

        # Проверяем тип selection
        if isinstance(selection, tuple):
            index = selection[0]
        elif isinstance(selection, int):
            index = selection
        else:
            return  # Обработка некорректного типа selection

        # Получаем ID заявки из текста строки
        request_id = request_list.get(index).split("|")[0].split(":")[1].strip()

        # Загружаем полную информацию о заявке из базы данных
        conn = sqlite3.connect('repair_requests.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests WHERE id=?", (request_id,))
        request = cursor.fetchone()
        conn.close()

        # Создаем окно для отображения полной информации
        details_window = ctk.CTkToplevel(root)
        details_window.title("Подробная информация о заявке")
        details_window.geometry("400x300")

        # Отображаем информацию о заявке
        for i, label in enumerate(["ID:", "Тип оборудования:", "Серийный номер:", "Описание:", "Приоритет:", "Назначен:"]):
            ctk.CTkLabel(details_window, text=f"{label} {request[i]}").pack()

        # Функция открытия окна для редактирования
        def open_edit_window():
            edit_window = ctk.CTkToplevel(details_window)
            edit_window.title("Редактирование заявки")

            # Поля для редактирования
            equipment_type_label = ctk.CTkLabel(edit_window, text="Тип оборудования:")
            equipment_type_entry = ctk.CTkEntry(edit_window)
            equipment_type_entry.insert(0, request[1])
            serial_number_label = ctk.CTkLabel(edit_window, text="Серийный номер:")
            serial_number_entry = ctk.CTkEntry(edit_window)
            serial_number_entry.insert(0, request[2])
            description_label = ctk.CTkLabel(edit_window, text="Описание проблемы:")
            description_entry = ctk.CTkTextbox(edit_window, height=5)
            description_entry.grid(padx = 5, pady = 5)
            description_entry.insert("1.0", request[3])
            priority_label = ctk.CTkLabel(edit_window, text="Приоритет:")
            priority_combobox = ctk.CTkComboBox(edit_window, values=["Низкий", "Средний", "Высокий"])
            priority_combobox.set(request[4])
            assigned_to_label = ctk.CTkLabel(edit_window, text="Назначен:")
            assigned_to_combobox = ctk.CTkComboBox(edit_window, values=["Иванов", "Куватов", "Леванюк"])
            assigned_to_combobox.set(request[5])

            # Размещение элементов для редактирования
            equipment_type_label.grid(row=0, column=0, padx=5, pady=5)
            equipment_type_entry.grid(row=0, column=1, padx=5, pady=5)
            serial_number_label.grid(row=1, column=0, padx=5, pady=5)
            serial_number_entry.grid(row=1, column=1, padx=5, pady=5)
            description_label.grid(row=2, column=0, padx=5, pady=5)
            description_entry.grid(row=2, column=1, padx=5, pady=5)
            priority_label.grid(row=3, column=0, padx=5, pady=5)
            priority_combobox.grid(row=3, column=1, padx=5, pady=5)
            assigned_to_label.grid(row=4, column=0, padx=5, pady=5)
            assigned_to_combobox.grid(row=4, column=1, padx=5, pady=5)

            # Функция сохранения изменений в заявке
            def save_changes():
                conn = sqlite3.connect('repair_requests.db')
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE requests SET
                        equipment_type = ?,
                        serial_number = ?,
                        description = ?,
                        priority = ?,
                        assigned_to = ?
                    WHERE id = ?
                ''', (
                    equipment_type_entry.get(),
                    serial_number_entry.get(),
                    description_entry.get("1.0", tk.END).strip(),
                    priority_combobox.get(),
                    assigned_to_combobox.get(),
                    request_id,
                ))
                conn.commit()
                conn.close()

                # Закрываем окна
                edit_window.destroy()
                details_window.destroy()

                # Обновляем список заявок в главном окне
                update_request_list()

            # Кнопка "Сохранить изменения"
            save_button = ctk.CTkButton(edit_window, text="Сохранить", command=save_changes)
            save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

            # Центрирование окна редактирования
            center_window(edit_window)

        # Кнопка "Изменить"
        edit_button = ctk.CTkButton(details_window, text="Изменить", command=open_edit_window)
        edit_button.pack()

        # Центрирование окна с подробной информацией
        center_window(details_window)
# Обновление списка заявок
def update_request_list():
    request_list.delete(0, ctk.END)
    conn = sqlite3.connect('repair_requests.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    requests = cursor.fetchall()
    conn.close()

    for request in requests:
        request_list.insert(ctk.END, f"ID: {request[0]} | Тип: {request[1]} | S/N: {request[2]} | Приоритет: {request[4]} | Назначен: {request[5]}")

# Создание главного окна
root = ctk.CTk()
root.title("Система заявок на ремонт")

# Список заявок
request_list = CTkListbox.CTkListbox(root, width=1000, height=500)
request_list.pack(pady=10)

# Привязываем событие двойного щелчка мыши к функции show_request_details
request_list.bind("<<ListboxSelect>>", show_request_details)

# Кнопка "Новая заявка"
add_button = ctk.CTkButton(root, text="Новая заявка", command=add_request_window)
add_button.pack(pady=10)

# Центрирование главного окна
center_window(root)

# Создание базы данных при запуске
create_database()

# Загрузка списка заявок
update_request_list()

root.mainloop()