import sqlite3 as sql
from logger import *

class Database:
    """
    Database class to manage SQLite operations.
    """
    def __init__(self):
        try:
            self.connection = sql.connect('sticky_notes_db.db')
            self.cursor = self.connection.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS sticky_notes_db
                             (title text, notes text, color text, font text)''')
            message = ("self.connection to Database")
            log_message(message)
        except Exception as e:
            logging.exception(e)