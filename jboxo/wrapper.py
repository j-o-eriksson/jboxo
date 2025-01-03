import json
import shlex
import subprocess
import time
from pathlib import Path

from jboxo.utils import wake_screen
from jboxo.videoprovider import VideoInfo, VideoJSONEncoder, VideoProvider


class VLCWrapper:
    def __init__(self, video_provider: VideoProvider):
        """ """
        self.root = Path("~/Downloads").expanduser()
        self.callbacks = {
            "add": self._add,
            "play": self._play,
            "stop": self._stop,
            "wake": self._wake,
        }
        self.videoinfo = VideoInfo(-1)
        self.video_provider = video_provider
        self.vlcprocess: subprocess.Popen | None = None

        self.elapsed = 0
        self.last_timestamp = time.time()

    def __del__(self):
        if self.vlcprocess is not None:
            self.vlcprocess.kill()

    def execute(self, cmd: str, data: str) -> None:
        d = json.loads(data) if data != "" else {}
        self.callbacks[cmd](d)

    def get_selected_info(self):
        return json.dumps(self.videoinfo, cls=VideoJSONEncoder)

    def get_elapsed(self):
        if self.vlcprocess is not None:
            if self.vlcprocess.poll() is not None:
                self.elapsed = self.videoinfo.duration
            else:
                self._step_time()
        return json.dumps({"elapsed": self.elapsed})

    def _add(self, data: dict) -> None:
        print("Add called with data: ", data)
        asset_id = data["id"]
        datatype = data["type"]

        if datatype == "video":
            self.videoinfo = self.video_provider.database[asset_id]
        elif datatype == "subtitles":
            _, sname, spath = self.video_provider.subtitles[asset_id]
            self.videoinfo.subtitle_name = sname
            self.videoinfo.subtitle_path = spath
        else:
            raise ValueError("Invalid data type.")

        self._stop({})
        self.elapsed = 0

    def _play(self, data: dict) -> None:
        print("Play called with data: ", data)
        if self.vlcprocess is not None:
            self.vlcprocess.kill()

        if self.videoinfo.path is None:
            raise ValueError("Video path not set.")

        seek_time = data["seek_time"]
        cmd = f"cvlc '{str(self.videoinfo.path)}' -f --start-time={seek_time}"

        if self.videoinfo.subtitle_path is not None:
            cmd += f" --sub-file '{str(self.videoinfo.subtitle_path)}'"

        print("opening video with command:", cmd)
        self.vlcprocess = subprocess.Popen(shlex.split(cmd))

        self.elapsed = seek_time
        self.last_timestamp = time.time()

    def _stop(self, data: dict) -> None:
        print("Stop called with data: ", data)
        if self.vlcprocess is not None:
            self.vlcprocess.kill()
            self.vlcprocess = None
            self._step_time()

    def _wake(self, data: dict) -> None:
        print("Wake called with data: ", data)
        wake_screen()

    def _step_time(self):
        timestamp = time.time()
        self.elapsed += timestamp - self.last_timestamp
        self.last_timestamp = timestamp
