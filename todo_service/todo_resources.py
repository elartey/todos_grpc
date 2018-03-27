import json
import os
from todo_service.todo_grpc import todos_pb2


def read_todo_database():
    todos_list = []
    with open(os.path.abspath('../data/todos_db.json')) as todo_file:
        for item in json.load(todo_file):
            todo = todos_pb2.Todo(
                id=item["id"],
                name=item["name"],
                data=item["data"])
            todos_list.append(todo)
    return todos_list
