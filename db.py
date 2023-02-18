import sqlite3
import db


class BotDB:
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
        self.sql = self.db.cursor()
        self.sql.execute("""CREATE TABLE IF NOT EXISTS films(film TEXT,filmcode INT)""")
        self.db.commit()

    def add_film(self, film, code):
        self.sql.execute(f"INSERT INTO films VALUES (?,?)", (film, code))
        return self.db.commit()

    def get_all_films(self):
        return self.sql.execute("SELECT * FROM films")

    def get_film_for_user(self, code):
        try:
            return self.sql.execute(f"SELECT film FROM films WHERE filmcode={code}").fetchone()
        finally:
            pass

    def close(self):
        self.sql.close()
