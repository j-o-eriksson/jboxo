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
    subtitle_name: str = ""
    subtitle_path: Path | None = None


class VideoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, VideoInfo):
            return {
                "id": o.id,
                "name": o.name,
                "duration": o.duration,
                "video_duration_str": str(timedelta(seconds=o.duration)),
                "thumbnail": o.thumbnail,
                "subtitle_name": o.subtitle_name,
            }
        return super().default(o)


class VideoProvider:
    def __init__(self):
        self.movies_path = Path("~/Downloads/bbo/movies").expanduser()
        self.series_path = Path("~/Downloads/bbo/series").expanduser()
        self.data_path = Path(__file__).parents[1] / "data"
        self.database: dict[int, VideoInfo] = {}
        self.subtitles: dict[int, tuple[int, str, Path]] = {}
        self.refresh()

    def get_movie_data(self) -> str:
        return json.dumps(list(self.database.values()), cls=VideoJSONEncoder, indent=2)

    def get_series_data(self) -> str:
        vs = list(self.database.values())
        return json.dumps(vs[-2:], cls=VideoJSONEncoder, indent=2)

    def get_subtitle_data(self) -> str:
        return json.dumps(
            [{"id": i, "name": name} for i, name, _ in self.subtitles.values()],
            indent=2,
        )

    def refresh(self):
        video_paths = self._get_paths({".mp4"})
        self.database = {
            i: VideoInfo(
                i, clean_string(p.stem), p, _get_duration(p), self._get_thumbnail(p)
            )
            for i, p in enumerate(video_paths)
        }

        sub_paths = self._get_paths({".srt"})
        self.subtitles = {
            i: (i, clean_string(p.stem), p) for i, p in enumerate(sub_paths)
        }

    def _get_paths(self, extentions):
        return [f for f in self.movies_path.rglob("*") if f.suffix in extentions]

    def _get_thumbnail(self, video_id: Path) -> str:
        ps = list((self.data_path / "thumbnails").iterdir())
        p = choice(ps)
        return b64encode(p.read_bytes()).decode()


def _get_duration(path: Path) -> int:
    cmd = f"ffprobe -i '{path}' -show_entries format=duration -v quiet -of csv='p=0'"
    return int(float(subprocess.check_output(cmd, shell=True).decode("utf-8").strip()))
