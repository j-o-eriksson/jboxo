import ast
import json
import subprocess
from pathlib import Path

from flask import Flask, render_template, request

from .vlcsession import VLCSession


class Dummy:
    """ """

    def __init__(self):
        """ """
        self.root = Path("/home/jon/Downloads")
        self.m = {
            "add": self._add,
            "play": self._play,
            "pause": self._pause,
            "stop": self._stop,
            "seek": self._seek,
        }

    def execute(self, cmd: str, session: VLCSession) -> str:
        """ """
        if cmd not in self.m:
            return "Error: invalid command."

        f = self.m[cmd]
        return f(session)

    def get_video_info(self, video_path: Path) -> str:
        """ """
        return json.dumps(
            {
                "name": video_path.stem,
                "duration": _get_duration(video_path),
                "subtitles": [],
            }
        )

    def _add(self, session) -> str:
        """ """
        data = ast.literal_eval(request.data.decode("utf-8"))
        path = data["videoPath"]
        print(_get_duration(path))
        return session.send_command(f"add {path}")

    def _play(self, session) -> str:
        """ """
        return session.send_command("play")

    def _pause(self, session) -> str:
        """ """
        return session.send_command("pause")

    def _stop(self, session) -> str:
        """ """
        return session.send_command("stop")

    def _seek(self, session) -> str:
        """ """
        data = ast.literal_eval(request.data.decode("utf-8"))
        timestamp = int(data["timestamp"])
        return session.send_command(f"seek {timestamp}")


def create_app():
    """Initializes REST backend."""

    dummy = Dummy()

    app = Flask(__name__)

    @app.post("/control/<cmd>")
    def execute_command(cmd):
        session = VLCSession()
        response = dummy.execute(cmd, session)
        return f"<p>{response}</p>"

    @app.get("/videos")
    def list_objects():
        return json.dumps(
            {
                "data": [
                    {"name": p.stem, "path": str(p)} for p in dummy.root.rglob("*.mp4")
                ]
            }
        )

    @app.post("/info")  # TODO: ideally, this should be GET info/<path>
    def object_info():
        data = ast.literal_eval(request.data.decode("utf-8"))
        return dummy.get_video_info(Path(data["videoPath"]))

    @app.route("/")
    def hello_world():
        return render_template("index.html")

    return app


def _get_duration(path: Path) -> int:
    """Uses ffmpeg to get the duration in seconds of a video."""
    cmd = f"ffprobe -i '{path}' -show_entries format=duration -v quiet -of csv='p=0'"
    return int(float(subprocess.check_output(cmd, shell=True).decode("utf-8").strip()))
