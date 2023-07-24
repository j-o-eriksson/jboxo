import ast
import json
import shlex
import subprocess
from pathlib import Path
from typing import Optional

from flask import Flask, render_template, request


class Dummy:
    def __init__(self):
        """ """
        self.root = Path("/home/jon/Downloads")
        self.m = {
            "add": self._add,
            "play": self._play,
            "stop": self._stop,
        }
        self.video_path: Optional[str] = None
        self.subtitle_path: Optional[str] = None
        self.vlcprocess: Optional[subprocess.Popen] = None

    def __del__(self):
        if self.vlcprocess is not None:
            self.vlcprocess.kill()

    def execute(self, cmd: str) -> None:
        if cmd not in self.m:
            raise ValueError("Invalid command.")

        self.m[cmd]()

    def get_video_info(self, video_path: Path) -> str:
        return json.dumps(
            {
                "name": video_path.stem,
                "duration": _get_duration(video_path),
                "subtitles": [],
            }
        )

    def _add(self) -> None:
        data = ast.literal_eval(request.data.decode("utf-8"))
        path = data["path"]
        datatype = data["type"]

        if datatype == "video":
            print(_get_duration(path))
            self.video_path = path
        elif datatype == "subtitles":
            self.subtitle_path = path
        else:
            raise ValueError("Invalid data type.")

    def _play(self, seek_time: Optional[int] = None) -> None:
        if self.video_path is None:
            raise ValueError("Video path not set.")

        cmd = f"cvlc '{self.video_path}' -f"
        if self.subtitle_path is not None:
            cmd += f" --sub-file '{self.subtitle_path}'"

        if seek_time is not None:
            cmd += f" --start-time={seek_time}"

        print("opening video with command:", cmd)
        self.vlcprocess = subprocess.Popen(shlex.split(cmd))

    def _stop(self) -> None:
        if self.vlcprocess is not None:
            self.vlcprocess.kill()


def create_app():
    """Initializes REST backend."""

    dummy = Dummy()

    app = Flask(__name__)

    @app.post("/control/<cmd>")
    def execute_command(cmd):
        try:
            dummy.execute(cmd)
            return "Success", 200
        except:
            return "Not found", 404

    @app.get("/videos")
    def list_videos():
        return json.dumps(
            {
                "data": [
                    {"name": p.stem, "path": str(p)} for p in dummy.root.rglob("*.mp4")
                ]
            }
        )

    @app.get("/subtitles")
    def list_subtitles():
        return json.dumps(
            {
                "data": [
                    {"name": p.stem, "path": str(p)} for p in dummy.root.rglob("*.srt")
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
