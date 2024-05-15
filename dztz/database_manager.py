import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('service_requests.db')
        self.cursor = self.conn.cursor()

        # Создаем таблицы, если они не существуют
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS requests 
             (id INTEGER PRIMARY KEY, date TEXT, equipment TEXT, 
             fault_type TEXT, description TEXT, client TEXT, status TEXT, 
             assigned_to TEXT, comments TEXT, completed_at TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT)''')
        self.conn.commit()

    # --- Работа с заявками ---

    def add_request(self, data):
        self.cursor.execute("INSERT INTO requests (date, equipment, fault_type, description, client, status) VALUES (?, ?, ?, ?, ?, ?)", data)
        self.conn.commit()

    def get_requests(self, filter_criteria=None):
        if filter_criteria:
            query = "SELECT * FROM requests WHERE " + filter_criteria
        else:
            query = "SELECT * FROM requests"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_request(self, request_id, data):
        set_clause = ", ".join(f"{col} = ?" for col in data)
        query = f"UPDATE requests SET {set_clause} WHERE id = ?"
        self.cursor.execute(query, tuple(data.values()) + (request_id,))
        self.conn.commit()

    def delete_request(self, request_id):
        self.cursor.execute("DELETE FROM requests WHERE id = ?", (request_id,))
        self.conn.commit()

    # --- Работа с пользователями ---

    def verify_credentials(self, username, password):
            self.cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))  # No hashing
            user = self.cursor.fetchone()
            return user[0] if user else None

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def update_user(self, user_id, data):
        set_clause = ", ".join(f"{col} = ?" for col in data)
        query = f"UPDATE users SET {set_clause} WHERE id = ?"
        self.cursor.execute(query, tuple(data.values()) + (user_id,))
        self.conn.commit()

    # --- Статистика ---

    def get_completed_requests_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM requests WHERE status = 'Выполнено'")
        return self.cursor.fetchone()[0]

    def get_average_completion_time(self):
        self.cursor.execute("SELECT julianday(completed_at) - julianday(date) FROM requests WHERE status = 'Выполнено'")
        time_differences = [time_diff[0] for time_diff in self.cursor.fetchall()]
        if time_differences:
            average_time = sum(time_differences) / len(time_differences)
            return f"{average_time:.2f} дней"  # Форматирование вывода
        else: 
            return "Нет данных"

    def get_fault_type_statistics(self):
        self.cursor.execute("SELECT fault_type, COUNT(*) FROM requests GROUP BY fault_type")
        return self.cursor.fetchall()