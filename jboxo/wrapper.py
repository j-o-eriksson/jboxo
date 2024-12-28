import ast
import shlex
import subprocess
from datetime import timedelta
from pathlib import Path

from flask import request

from jboxo.utils import clean_string
from jboxo.videoprovider import VideoInfo, VideoProvider


class VLCWrapper:
    def __init__(self, video_provider: VideoProvider):
        """ """
        self.root = Path("~/Downloads").expanduser()
        self.callbacks = {
            "add": self._add,
            "play": self._play,
            "stop": self._stop,
        }
        self.videoinfo = VideoInfo(-1)
        self.video_provider = video_provider
        self.vlcprocess: subprocess.Popen | None = None

    def __del__(self):
        if self.vlcprocess is not None:
            self.vlcprocess.kill()

    def execute(self, cmd: str) -> None:
        self.callbacks[cmd]()

    def get_subtitles(self):
        return [
            {"name": clean_string(p.stem), "path": str(p)}
            for p in self.video_provider.sub_paths
        ]

    def get_selected_info(self):
        return {
            "data": {
                "name": self.videoinfo.name,
                "subtitle_name": self.videoinfo.subtitle_name,
                "video_duration": self.videoinfo.duration,
                "video_duration_str": str(timedelta(seconds=self.videoinfo.duration)),
            }
        }

    def _add(self) -> None:
        data = ast.literal_eval(request.data.decode("utf-8"))
        path = Path(data["path"])
        datatype = data["type"]

        if datatype == "video":
            name = clean_string(path.stem)
            self.videoinfo.name = name
            self.videoinfo.path = path
            self.videoinfo.duration = self.video_provider.get_meta(name)
        elif datatype == "subtitles":
            self.videoinfo.subtitle_name = clean_string(path.stem)
            self.videoinfo.subtitle_path = path
        else:
            raise ValueError("Invalid data type.")

    def _play(self, seek_time: int | None = None) -> None:
        if self.vlcprocess is not None:
            return

        if self.videoinfo.path is None:
            raise ValueError("Video path not set.")

        cmd = f"cvlc '{str(self.videoinfo.path)}' -f"

        if self.videoinfo.subtitle_path is not None:
            cmd += f" --sub-file '{str(self.videoinfo.subtitle_path)}'"

        if seek_time is not None:
            cmd += f" --start-time={seek_time}"

        print("opening video with command:", cmd)
        self.vlcprocess = subprocess.Popen(shlex.split(cmd))

    def _stop(self) -> None:
        if self.vlcprocess is not None:
            self.vlcprocess.kill()
            self.vlcprocess = None
