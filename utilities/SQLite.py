import sqlite3
from sqlite3 import Error
import os
import pathlib


class SQLite:
    DBName = 'calibration.db'

    def __init__(self):

        self.create_connection(self.DBName)
        print(pathlib.Path().absolute())


    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
