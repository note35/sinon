"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE

This is an example flask_restful application, which is adapted by that official document
"""

import sqlite3
from flask import Flask, g, jsonify
from flask_restful import reqparse, abort, Api, Resource

from utils.absdb import TodoModel


app = Flask(__name__)
api = Api(app)

app.config["DATABASE"] = "./todo.db"
tmodel = TodoModel()

parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("content")


@app.teardown_appcontext
def close_connection(exception):
    tmodel.close_connection(exception)

def abort_if_todo_doesnt_exist(todo_id):
    r = tmodel.get_todo(todo_id)
    if not r:
        abort(404, message="Todo {} doesn not exist".format(todo_id))


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        r = tmodel.get_todo(todo_id)
        rdic = {
            "id": r[0],
            "Name": r[1],
            "Content": r[2]
        }
        return jsonify(rdic)

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        tmodel.del_todo(todo_id)
        return "", 204

    def put(self, todo_id):
        args = parser.parse_args()
        r = tmodel.put_todo(todo_id, args["name"], args["content"])
        return args, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        rdic = {}
        for item in tmodel.get_todo_list():
            rdic[item[0]] = {
                "id": item[0],
                "Name": item[1],
                "Content": item[2]
            }
        return jsonify(rdic)


##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, "/todos")
api.add_resource(Todo, "/todos/<todo_id>")


if __name__ == "__main__":
    with app.app_context():
        tmodel.setup_init_data()
        app.run(debug=True)
