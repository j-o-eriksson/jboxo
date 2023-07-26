import ast
import json
import shlex
import subprocess
from pathlib import Path
from datetime import timedelta
from typing import Optional

from flask import Flask, render_template, request


class VLCWrapper:
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
        self.m[cmd]()

    def get_videos(self):
        return {
            "data": [
                {"name": _clean_string(p.stem), "path": str(p)}
                for p in self.root.rglob("*.mp4")
            ]
        }

    def get_subtitles(self):
        return {
            "data": [
                {"name": _clean_string(p.stem), "path": str(p)}
                for p in self.root.rglob("*.srt")
            ]
        }

    def get_selected_info(self) -> str:
        duration = _get_duration(self.video_path)
        return json.dumps(
            {
                "video_name": _clean_string(Path(self.video_path).stem),
                "video_duration": duration,
                "video_duration_str": str(timedelta(seconds=duration)),
                "subtitle_name": _clean_string(Path(self.subtitle_path).stem),
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

    dummy = VLCWrapper()
    app = Flask(__name__)

    @app.post("/control/<cmd>")
    def execute_command(cmd):
        try:
            dummy.execute(cmd)
            return "Success", 200
        except Exception as ex:
            return f"Error: {str(ex)}", 404

    @app.get("/videos")
    def list_videos():
        return json.dumps(dummy.get_videos(), indent=2)

    @app.get("/subtitles")
    def list_subtitles():
        return json.dumps(dummy.get_subtitles(), indent=2)

    @app.get("/selected")
    def get_selected_info():
        return dummy.get_selected_info()

    @app.route("/")
    def hello_world():
        return render_template("index.html")

    return app


def _get_duration(path: Path) -> int:
    """Uses ffmpeg to get the duration in seconds of a video."""
    cmd = f"ffprobe -i '{path}' -show_entries format=duration -v quiet -of csv='p=0'"
    return int(float(subprocess.check_output(cmd, shell=True).decode("utf-8").strip()))


def _clean_string(s: str) -> str:
    d = {ord(c): " " for c in ".-[]"}
    return s.translate(d)
