"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE

This is a simple model for example flask_restful application
"""

import sqlite3
from flask import current_app


class TodoModel(object):
    """
    Abstract interface for interacting with todo table in database
    """

    def open_connection(self):
        self.db = sqlite3.connect(current_app.config["DATABASE"])

    def close_connection(self):
        if hasattr(self, "db"):
            self.db.close()

    def setup_init_data(self):
        self.open_connection()
        try:
            self.db.cursor().execute("DROP TABLE main.Tasks")
        except:
            # table is not exist.
            pass
        self.db.cursor().execute("CREATE TABLE IF NOT EXISTS main.Tasks(ID integer PRIMARY KEY AUTOINCREMENT, Name varchar(255), Content varchar(255));")
        self.db.cursor().execute("INSERT INTO main.Tasks(ID, Name, Content) VALUES (1, 'todo1', 'build an API');")
        self.db.cursor().execute("INSERT INTO main.Tasks(ID, Name, Content) VALUES (2, 'todo2', '?????');")
        self.db.cursor().execute("INSERT INTO main.Tasks(ID, Name, Content) VALUES (3, 'todo3', 'profit!');")
        self.db.commit()

    def get_todo_list(self):
        self.open_connection()
        r = self.db.cursor().execute("SELECT * FROM main.Tasks;")
        self.db.commit()
        return r.fetchall()

    def get_todo(self, todoid):
        self.open_connection()
        todoid_str = str(todoid)
        r = self.db.cursor().execute("SELECT * FROM main.Tasks WHERE ID=?;", (todoid_str))
        self.db.commit()
        return r.fetchone()

    def del_todo(self, todoid):
        self.open_connection()
        todoid_str = str(todoid)
        self.db.cursor().execute("DELETE FROM main.Tasks WHERE ID=?;", (todoid_str))
        self.db.commit()

    def put_todo(self, todoid, name, content):
        self.open_connection()
        todoid_str, name_str, content_str = str(todoid), str(name), str(content)
        if self.db.cursor().execute("SELECT * FROM main.Tasks WHERE ID=?;", (todoid_str)).fetchone():
            self.db.cursor().execute("UPDATE main.Tasks SET Name=?,Content=? WHERE ID=?;", (name_str, content_str, todoid_str))
        else:
            r = self.db.cursor().execute("SELECT * FROM main.Tasks ORDER BY ID DESC LIMIT 1")
            new_id = r.fetchone()[0]+1
            self.db.cursor().execute("INSERT INTO main.Tasks(ID, Name, Content) VALUES (?, ?, ?);", (new_id, name_str, content_str))
        self.db.commit()
