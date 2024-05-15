import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, parent, db_manager, on_login_success):
        self.parent = parent
        self.db_manager = db_manager
        self.on_login_success = on_login_success

        # Создаем окно авторизации
        self.window = tk.Toplevel(self.parent)
        self.window.title("Авторизация")
        self.window.geometry("300x200")
        self.window.grab_set() # Захватывает фокус, блокируя родительское окно

        # Создаем элементы интерфейса
        self.username_label = tk.Label(self.window, text="Имя пользователя:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.window, text="Пароль:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.window, text="Войти", command=self.login)
        self.login_button.pack()

    def show(self):
        self.window.deiconify() # Показать окно (если оно было скрыто)
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"+{x}+{y}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Проверяем учетные данные в базе данных (через DatabaseManager)
        user_role = self.db_manager.verify_credentials(username, password)

        if user_role:
            # Успешная авторизация
            messagebox.showinfo("Успех", "Авторизация прошла успешно!")
            self.window.destroy()
            self.on_login_success(user_role)  # Вызываем функцию обратного вызова
        else:
            # Ошибка авторизации
            messagebox.showerror("Ошибка", "Неверные имя пользователя или пароль!")