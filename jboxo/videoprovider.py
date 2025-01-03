import json
import re
import subprocess
from base64 import b64encode
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from random import choice

from jboxo.utils import prettify


@dataclass
class VideoInfo:
    id: int
    name: str = ""
    path: Path = Path()
    duration: int = 1
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
            }
        return super().default(o)


class VideoProvider:
    def __init__(self):
        self.movies_path = Path("~/Downloads/bbo/movies").expanduser()
        self.series_path = Path("~/Downloads/bbo/series").expanduser()
        self.data_path = Path(__file__).parents[1] / "data"
        self.database: dict[int, VideoInfo] = {}
        self.subtitles: dict[int, tuple[int, str, Path]] = {}
        self.series_data = _load_series_data(self.series_path)
        self.refresh()

    def get_movie_data(self) -> str:
        return json.dumps(list(self.database.values()), cls=VideoJSONEncoder, indent=2)

    def get_series_data(self) -> str:
        out = [
            {
                "id": v["id"],
                "name": v["name"],
                "duration": 1,
                "video_duration_str": str(timedelta(1)),
                "thumbnail": _load_thumbnail(Path(v["thumbnail"])),
            }
            for v in self.series_data.values()
        ]
        return json.dumps(out, indent=2)

    def get_subtitle_data(self) -> str:
        return json.dumps(
            [{"id": i, "name": name} for i, name, _ in self.subtitles.values()],
            indent=2,
        )

    def refresh_series_data(self):
        self.series_data = _load_series_data(self.series_path, False)

    def refresh(self):
        video_paths = _get_paths(self.movies_path, {".mp4"})
        self.database = {
            i: VideoInfo(
                i, prettify(p.stem), p, _get_duration(p), self._get_thumbnail(p)
            )
            for i, p in enumerate(video_paths)
        }

        sub_paths = _get_paths(self.movies_path, {".srt"})
        self.subtitles = {i: (i, prettify(p.stem), p) for i, p in enumerate(sub_paths)}

    def _get_thumbnail(self, video_id: Path) -> str:
        ps = list((self.data_path / "thumbnails").iterdir())
        p = choice(ps)
        return b64encode(p.read_bytes()).decode()


def _load_thumbnail(path: Path):
    return b64encode(path.read_bytes()).decode()


def _get_duration(path: Path) -> int:
    if "'" in path.stem:
        path = path.rename(path.parent / f"{prettify(path.stem)}{path.suffix}")
    cmd = f"ffprobe -i '{path}' -show_entries format=duration -v quiet -of csv='p=0'"
    return int(float(subprocess.check_output(cmd, shell=True).decode("utf-8").strip()))


def _get_paths(path: Path, extentions: set[str]):
    return [f for f in path.rglob("*") if f.suffix in extentions]


def _load_series_data(series_root_path: Path, read_from_cache: bool = True) -> dict:
    cache_path = series_root_path.parent / "cache.json"

    if cache_path.exists() and read_from_cache:
        print("reading series data from cache")
        return json.loads(cache_path.read_text())

    out = {}
    for series_id, series_path in enumerate(series_root_path.iterdir()):
        if not series_path.is_dir():
            continue
        out[series_id] = {
            "id": series_id,
            "name": prettify(series_path.stem),
            "description": "unavailable",
            "thumbnail": str(series_path / "thumbnail.jpg"),
            "seasons": {
                int(season_path.stem[1:]): _get_season_data(season_path)
                for season_path in series_path.iterdir()
                if season_path.is_dir()
            },
        }

    cache_path.write_text(json.dumps(out, indent=2))
    return out


def _get_episode(p: Path):
    m = re.search(r"e(\d+)", p.stem.lower())
    if m is not None:
        return int(m.group(1))
    return -1


def _get_season_data(path: Path) -> dict:
    out = {}
    for p in _get_paths(path, {".mp4", ".mkv"}):
        out[_get_episode(p)] = {"path": str(p), "duration": _get_duration(p)}
    return out
