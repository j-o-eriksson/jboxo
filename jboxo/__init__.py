import ast
import json
import shlex
import subprocess
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Optional

from flask import Flask, render_template, request

import jboxo.utils as ju


@dataclass
class VideoData:
    video_name: str
    video_path: Path
    duration: int = 0
    subtitle_name: str = ""
    subtitle_path: Path = Path("")


class VLCWrapper:
    def __init__(self):
        """ """
        self.root = Path("/home/jon/Downloads")
        self.m = {
            "add": self._add,
            "play": self._play,
            "stop": self._stop,
        }
        self.video_meta = VideoData(video_name="", video_path=Path())
        self.vlcprocess: Optional[subprocess.Popen] = None
        self.video_provider = ju.VideoProvider()

    def __del__(self):
        if self.vlcprocess is not None:
            self.vlcprocess.kill()

    def execute(self, cmd: str) -> None:
        self.m[cmd]()

    def get_videos(self):
        return self._get_paths({".mp4"})

    def get_subtitles(self):
        return self._get_paths({".srt"})

    def get_selected_info(self):
        return {
            "name": self.video_meta.video_name,
            "subtitle_name": self.video_meta.subtitle_name,
            "video_duration": self.video_meta.duration,
            "video_duration_str": str(timedelta(seconds=self.video_meta.duration)),
        }

    def _get_paths(self, extentions):
        files = (f for f in self.root.rglob("*") if f.suffix in extentions)
        return {
            "data": [{"name": ju.clean_string(p.stem), "path": str(p)} for p in files]
        }

    def _add(self) -> None:
        data = ast.literal_eval(request.data.decode("utf-8"))
        path = Path(data["path"])
        datatype = data["type"]

        if datatype == "video":
            name = ju.clean_string(path.stem)
            self.video_meta.video_name = name
            self.video_meta.video_path = path
            self.video_meta.duration = self.video_provider.get_meta(name)
        elif datatype == "subtitles":
            self.video_meta.subtitle_name = ju.clean_string(path.stem)
            self.video_meta.subtitle_path = path
        else:
            raise ValueError("Invalid data type.")

    def _play(self, seek_time: Optional[int] = None) -> None:
        if self.vlcprocess is not None:
            return

        if self.video_meta.video_path is None:
            raise ValueError("Video path not set.")

        cmd = f"cvlc '{str(self.video_meta.video_path)}' -f"

        if self.video_meta.subtitle_path is not None:
            cmd += f" --sub-file '{str(self.video_meta.subtitle_path)}'"

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
        dummy.execute(cmd)
        return "Success", 200

    @app.get("/videos")
    def list_videos():
        return json.dumps(dummy.get_videos(), indent=2)

    @app.get("/subtitles")
    def list_subtitles():
        return json.dumps(dummy.get_subtitles(), indent=2)

    @app.get("/selected")
    def get_selected_info():
        return json.dumps(dummy.get_selected_info(), indent=2)

    @app.route("/")
    def hello_world():
        return render_template("index.html")

    return app
