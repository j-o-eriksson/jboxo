import json
import subprocess
from base64 import b64encode
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from random import choice

from jboxo.utils import clean_string


@dataclass
class VideoInfo:
    id: int
    name: str = ""
    path: Path = Path()
    duration: int = 0
    thumbnail: str = ""
    subtitle_name: str | None = None
    subtitle_path: Path | None = None


class VideoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, VideoInfo):
            return {
                "id": o.id,
                "name": o.name,
                "path": str(o.path),
                "duration": o.duration,
                "video_duration_str": str(timedelta(seconds=o.duration)),
                "thumbnail": o.thumbnail,
            }
        return super().default(o)


class VideoProvider:
    def __init__(self):
        self.meta_path = Path("~/.bbo/meta.json").expanduser()
        self.movies_path = Path("~/Downloads/bbo/movies").expanduser()
        self.series_path = Path("~/Downloads/bbo/series").expanduser()
        self.data_path = Path(__file__).parents[1] / "data"
        self.database: dict[int, VideoInfo] = {}
        self.refresh()

    def __del__(self):
        self._dump()

    def get_meta(self, video_id: str) -> int:
        return self.videodata[video_id]

    def get_movie_data(self) -> str:
        vs = list(self.database.values())
        out = json.dumps(vs, cls=VideoJSONEncoder, indent=2)
        print(out)
        return out

    def get_series_data(self) -> str:
        vs = list(self.database.values())
        out = json.dumps(vs[-2:], cls=VideoJSONEncoder, indent=2)
        print(out)
        return out

    def refresh(self):
        self.video_paths = self._get_paths({".mp4"})
        self.sub_paths = self._get_paths({".srt"})
        self.videodata = self._init_meta()
        self.database = {
            i: VideoInfo(
                i, clean_string(p.stem), p, _get_duration(p), self._get_thumbnail(p)
            )
            for i, p in enumerate(self.video_paths)
        }

    def _init_meta(self):
        if not self.meta_path.exists():
            self.meta_path.write_text("{}")

        metadata = json.loads(self.meta_path.read_text())
        for video_path in self.video_paths:
            video_id = clean_string(str(video_path.stem))
            if video_id not in metadata:
                print(f"retrieving duration for {video_id}")
                metadata[video_id] = _get_duration(video_path)
        return metadata

    def _dump(self):
        self.meta_path.write_text(json.dumps(self.videodata, indent=2))

    def _get_paths(self, extentions):
        return [f for f in self.movies_path.rglob("*") if f.suffix in extentions]

    def _get_thumbnail(self, video_id: Path) -> str:
        ps = list((self.data_path / "thumbnails").iterdir())
        p = choice(ps)
        return b64encode(p.read_bytes()).decode()


def _get_duration(path: Path) -> int:
    cmd = f"ffprobe -i '{path}' -show_entries format=duration -v quiet -of csv='p=0'"
    return int(float(subprocess.check_output(cmd, shell=True).decode("utf-8").strip()))
