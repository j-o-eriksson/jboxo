import json
import subprocess
from pathlib import Path


class VideoProvider:
    def __init__(self):
        self.meta_path = Path("/home/jon/.bbo/meta.json")
        self.root_path = Path("/home/jon/Downloads")
        self.video_extensions = {".mp4"}
        self.videopaths = [
            f for f in self.root_path.rglob("*") if f.suffix in self.video_extensions
        ]
        self.metadata = self.init_meta()

    def __del__(self):
        with self.meta_path.open("w") as f:
            json.dump(self.metadata, f, indent=2)

    def init_meta(self):
        if not self.meta_path.exists():
            with self.meta_path.open("w") as f:
                json.dump({}, f)

        with self.meta_path.open() as f:
            metadata = json.load(f)
            for video_path in self.videopaths:
                video_id = clean_string(str(video_path.stem))
                if video_id not in metadata:
                    print(f"retrieving duration for {video_id}")
                    metadata[video_id] = _get_duration(video_path)
            return metadata

    def get_meta(self, video_id: str) -> int:
        return self.metadata[video_id]


def clean_string(s: str) -> str:
    return s.translate({ord(c): " " for c in ".-[]"})


def _get_duration(path: Path) -> int:
    cmd = f"ffprobe -i '{path}' -show_entries format=duration -v quiet -of csv='p=0'"
    return int(float(subprocess.check_output(cmd, shell=True).decode("utf-8").strip()))
