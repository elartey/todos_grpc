
from flask import Flask, Response, request

from google.protobuf.json_format import MessageToJson
from client_wrapper.todo_client_wrapper import ServiceClient

import todo_service.todo_grpc.todos_pb2_grpc as todo_service
import todo_service.todo_grpc.todos_pb2 as todo_objects

app = Flask(__name__)
app.config['todos'] = ServiceClient(todo_service, 'TodosStub', 'localhost', 50051)


@app.route('/')
def test_application():
    return 'The todo API is up!'


@app.route('/test', methods=['GET'])
def todos_test():
    if request.method == 'GET':
        ts_request = todo_objects.TestRequest(name="This is a test message")

        def test_todo():
            resp = app.config['todos'].TestTodo(ts_request)
            return MessageToJson(resp)

        return Response(test_todo(), content_type='application/json')


@app.route('/get-todo', methods=['GET'])
def get_todo():
    if request.method == 'GET':
        ts_request = todo_objects.TodoRequest(id=str(request.args.get('todo_id')))

        def fetch():
            resp = app.config['todos'].GetTodo(ts_request)
            return MessageToJson(resp)

        return Response(fetch(), content_type='application/json')


@app.route('/get-todos', methods=['GET'])
def get_todos():

    if request.method == 'GET':

        incoming = request.args.get('todo_list')
        incoming = incoming.split(',')

        def get_ids():
            for item in incoming:
                yield todo_objects.TodoRequest(id=str(item))

        def fetch():
            resp = app.config['todos'].GetTodos(get_ids())
            temp_array = []
            for r in resp:
                temp_array.append(r)
            fetch_data = todo_objects.Response(todo_resp=temp_array)
            return MessageToJson(fetch_data)

        return Response(fetch(), content_type='application/json')


if __name__ == '__main__':
    app.run()
