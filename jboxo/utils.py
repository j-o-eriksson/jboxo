import json
import subprocess
from pathlib import Path


class VideoProvider:
    def __init__(self):
        self.meta_path = Path("~/.bbo/meta.json").expanduser()
        self.root_path = Path("~/Downloads").expanduser()
        self.refresh()

    def __del__(self):
        self.meta_path.write_text(json.dumps(self.metadata, indent=2))

    def get_meta(self, video_id: str) -> int:
        return self.metadata[video_id]

    def refresh(self):
        self.video_paths = self._get_paths({".mp4", ".mkv"})
        self.sub_paths = self._get_paths({".srt"})
        self.metadata = self._init_meta()
        print("\n Video Metadata:\n", self.metadata)

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

    def _get_paths(self, extentions):
        return [f for f in self.root_path.rglob("*") if f.suffix in extentions]


def clean_string(s: str) -> str:
    clean = s.translate({ord(c): " " for c in ".-[]"})
    MAX_LEN = 35
    return f"{clean[:MAX_LEN]}..." if len(clean) > MAX_LEN else clean


def wake_screen() -> None:
    cmd = f"xset -dpms && xset +dpms"
    subprocess.run(cmd, shell=True)


def _get_duration(path: Path) -> int:
    cmd = f"ffprobe -i '{path}' -show_entries format=duration -v quiet -of csv='p=0'"
    return int(float(subprocess.check_output(cmd, shell=True).decode("utf-8").strip()))
