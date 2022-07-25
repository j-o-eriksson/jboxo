import ast
from pathlib import Path

from flask import Flask, request

from .vlcsession import VLCSession


def create_app():
    """Initializes REST backend."""

    root = Path("/home/jon/dev/jboxo/data")

    app = Flask(__name__)

    @app.post('/control')
    def execute_command():
        data = ast.literal_eval(request.data.decode("utf-8"))
        path = root / data["add"]

        session = VLCSession()
        response = session.send_command(f"add {path}")
        return f"<p>{response}</p>"

    @app.get('/list')
    def list_objects():
        items = "".join([f"<p>{p.name}</p>" for p in root.iterdir()])
        return items

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    
    return app

