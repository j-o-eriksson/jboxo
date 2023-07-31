import ast
import shlex
import subprocess
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Optional

from flask import request

from jboxo.utils import VideoProvider, clean_string


@dataclass
class VideoData:
    video_name: str = ""
    video_path: Path = Path()
    duration: int = 0
    subtitle_name: str = ""
    subtitle_path: Path = Path()


class VLCWrapper:
    def __init__(self):
        """ """
        self.root = Path("/home/jon/Downloads")
        self.callbacks = {
            "add": self._add,
            "play": self._play,
            "stop": self._stop,
        }
        self.video_meta = VideoData()
        self.video_provider = VideoProvider()
        self.vlcprocess: Optional[subprocess.Popen] = None

    def __del__(self):
        if self.vlcprocess is not None:
            self.vlcprocess.kill()

    def execute(self, cmd: str) -> None:
        self.callbacks[cmd]()

    def get_videos(self):
        return self._get_paths(self.video_provider.video_paths)

    def get_subtitles(self):
        return self._get_paths(self.video_provider.sub_paths)

    def get_selected_info(self):
        return {
            "data": {
                "name": self.video_meta.video_name,
                "subtitle_name": self.video_meta.subtitle_name,
                "video_duration": self.video_meta.duration,
                "video_duration_str": str(timedelta(seconds=self.video_meta.duration)),
            }
        }

    def _get_paths(self, paths):
        return {"data": [{"name": clean_string(p.stem), "path": str(p)} for p in paths]}

    def _add(self) -> None:
        data = ast.literal_eval(request.data.decode("utf-8"))
        path = Path(data["path"])
        datatype = data["type"]

        if datatype == "video":
            name = clean_string(path.stem)
            self.video_meta.video_name = name
            self.video_meta.video_path = path
            self.video_meta.duration = self.video_provider.get_meta(name)
        elif datatype == "subtitles":
            self.video_meta.subtitle_name = clean_string(path.stem)
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
