from concurrent import futures

import grpc
import time

from todo_service.todo_grpc import todos_pb2, todos_pb2_grpc
import todo_resources

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def get_todo(todo_db, tid):
    for todo in todo_db:
        if todo.id == tid:
            return todo
    return None


class TodosServicer(todos_pb2_grpc.TodosServicer):

    def __init__(self):
        self.db = todo_resources.read_todo_database()

    def TestTodo(self, request, context):
        return todos_pb2.TestResponse(message="Message: %s" % request.name)

    def GetTodo(self, request, context):
        print("Incoming request for: %s" % request)
        todo = get_todo(self.db, request.id)
        if todo is None:
            print("Is none.")
            return todos_pb2.Todo(id=request.id, name="", data=None)
        else:
            return todo

    def GetTodos(self, request_iterator, context):
        for item in request_iterator:
            print("Incoming requests for: %s" % item.id)
            todo = get_todo(self.db, item.id)
            if todo is None:
                yield todos_pb2.Todo(id=item.id, name="", data=None)
            else:
                yield todo

    def CreateTodo(self, request, context):
        todo = get_todo(self.db, request.id)
        if todo is None:
            new_todo = todos_pb2.Todo(
                id=request.id,
                name=request.name,
                data=request.data
            )
            self.db.append(new_todo)

            return new_todo
        else:
            return todo


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    todos_pb2_grpc.add_TodosServicer_to_server(
        TodosServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Starting Todo Service...")
    try:
        while True:
            print("Started Todo Service.")
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

