import subprocess


def clean_string(s: str) -> str:
    clean = s.translate({ord(c): " " for c in ".-[]"})
    MAX_LEN = 35
    return f"{clean[:MAX_LEN]}..." if len(clean) > MAX_LEN else clean


def wake_screen() -> None:
    cmd = f"xset -dpms && xset +dpms"
    subprocess.run(cmd, shell=True)
