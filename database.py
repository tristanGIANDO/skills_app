import os
import sqlite3


class Database:
    def __init__(self) -> None:
        self._path = os.path.dirname(__file__)
        self._name = os.path.basename(self._path)

        self._db = self.connect()
        self._cursor = self._db.cursor()

        self.create()

    def connect(self):
        return sqlite3.connect(os.path.join(self._path,
                                            f"{self._name}_database.db"))

    def _row_exists(self, name: str) -> bool:
        for file in self.read():
            if file[0] == name:
                return True

    def create(self) -> None:
        self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._name}
                (
                    ["skill_and_soft"] TEXT,
                    ["level"] REAL
                )
                """)

    def insert_object(self, data: dict) -> None:
        object_name = data["skill_and_soft"]
        if self._row_exists(object_name):
            self.delete_object(object_name)

        self._cursor.execute(f"""
                INSERT INTO {self._name}
                (
                    ["skill_and_soft"],
                    ["level"]
                )

                VALUES
                (?,?)
                """, (object_name,
                      data["level"]
                      )
                )

        self._db.commit()

    def read(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
        return self._cursor.fetchall()

    def find_object(self, name: str):
        self._cursor.execute(f"SELECT * FROM {self._name} WHERE [] = '{name}'")
        return self._cursor.fetchall()

    def delete_object(self, name: str):
        sql = f"DELETE FROM {self._name} WHERE [] = '{name}'"
        self._cursor.execute(sql)
        self._db.commit()

    def close(self) -> None:
        self._db.close()
