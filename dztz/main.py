import tkinter as tk
from tkinter import ttk
from login_window import LoginWindow
from database_manager import DatabaseManager
from request_manager import RequestManager

# Global variables
root = tk.Tk()
root.title("Лифаге индастрес")
root.geometry("800x600")

# Center the main window
root.update_idletasks()  # Required to get accurate size information
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = root.winfo_width()
window_height = root.winfo_height()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"+{x}+{y}")
current_user_role = None

def create_main_window():
    # Создание блокнота для разных вкладок
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Создание вкладок и соответствующих им рамок
    add_tab = tk.Frame(notebook)
    edit_tab = tk.Frame(notebook)
    track_tab = tk.Frame(notebook)
    assign_tab = tk.Frame(notebook)
    stats_tab = tk.Frame(notebook)

    notebook.add(add_tab, text="Добавить запрос")
    notebook.add(edit_tab, text="Изменение запроса")
    notebook.add(track_tab, text="Отслеживание заявки")

    # Создание экземпляря менеджера запросов и передача необходимых объектов
    request_manager = RequestManager(db_manager, add_tab, edit_tab, track_tab, assign_tab, stats_tab, current_user_role)

    # Инициализация элементов пользовательского интерфейса и связка их с методами RequestManager
    request_manager.create_add_request_ui()
    request_manager.create_edit_request_ui()
    request_manager.create_track_status_ui()

def on_login_success(user_role):
    global current_user_role
    current_user_role = user_role
    create_main_window()

def main():
    global db_manager
    # Создание бд и подключение к ней
    db_manager = DatabaseManager()

    # Создание окна авторизации
    login_window = LoginWindow(root, db_manager, on_login_success)
    login_window.show()

    root.mainloop()

if __name__ == "__main__":
    main()