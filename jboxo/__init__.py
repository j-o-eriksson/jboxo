import ast
from pathlib import Path

from flask import Flask, request

from .vlcsession import VLCSession


class Dummy:
    """ """

    def __init__(self):
        self.root = Path("/home/jon/dev/jboxo/data")
        self.m = {
          "add": self._add,
          "play": self._play,
          "pause": self._pause,
          "stop": self._stop,
        }

    def execute(self, cmd: str, session: VLCSession) -> str:
        if cmd not in self.m:
            return "Error: invalid command."

        f = self.m[cmd]
        return f(session)

    def _add(self, session) -> str:
        data = ast.literal_eval(request.data.decode("utf-8"))
        path = self.root / data["path"]
        return session.send_command(f"add {path}")

    def _play(self, session) -> str:
        return session.send_command("play")

    def _pause(self, session) -> str:
        return session.send_command("pause")

    def _stop(self, session) -> str:
        return session.send_command("stop")


def create_app():
    """Initializes REST backend."""

    dummy = Dummy()

    app = Flask(__name__)

    @app.post('/control/<cmd>')
    def execute_command(cmd):
        session = VLCSession()
        response = dummy.execute(cmd, session)
        return f"<p>{response}</p>"

    @app.get('/list')
    def list_objects():
        items = "".join([f"<p>{p.name}</p>" for p in dummy.root.iterdir()])
        return items

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    
    return app

