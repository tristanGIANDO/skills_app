import os
import sqlite3


class Database:
    def __init__(self) -> None:
        self._path = os.path.dirname(__file__)
        self._name = os.path.basename(self._path)

        self._db = self.connect()
        self._cursor = self._db.cursor()

        self._modeling_table = ModelingTable(self._db)

    def connect(self):
        return sqlite3.connect(os.path.join(self._path,
                                            f"{self._name}_database.db"))

    def close(self) -> None:
        self._db.close()


class Table:
    def __init__(self, database) -> None:
        self._db = database
        self._cursor = self._db.cursor()
        self._name = "baseTable"

    def create(self) -> str:
        self._cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._name}
                (
                    ["skill_and_soft"] TEXT,
                    ["level"] REAL
                )
                """)

    def _row_exists(self, name: str) -> bool:
        for file in self.read():
            if file[0] == name:
                return True

    def insert_data(self, skill: str, level: int) -> None:
        if self._row_exists(skill):
            self.delete_object(skill)

        self._cursor.execute(f"""
                INSERT INTO {self._name}
                (["skill_and_soft"],["level"])

                VALUES(?,?)
                """, (skill, level)
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


class ModelingTable(Table):
    def __init__(self, database) -> None:
        super().__init__(database)

        self._name = "modeling"
        self.create()
