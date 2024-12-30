import json
from pathlib import Path
from shutil import rmtree

import requests
from bs4 import BeautifulSoup


def download_image(url) -> tuple[bytes, str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tags = soup.find_all("img")
    for tag in tags:
        src = tag.get("src")
        if "upload" in src:
            w = int(tag.get("width"))
            h = int(tag.get("height"))
            if h * w < 100**2:
                print(f"to small: w: {w}, h: {h}")
                continue
            *_, suffix = src.split(".")
            r2 = requests.get(f"https:{src}")
            print(w / h, len(r2.content), src)
            return r2.content, suffix
    return b"", "jpg"


def get_image_link(query: str):
    url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=10&namespace=0&format=json"
    response = requests.get(url)
    d = json.loads(response.text)
    idx = next(
        (
            i
            for i, x in enumerate(d[1])
            if any(s in x for s in ["film)", "TV series)"])  # use regex?
        ),
        0,
    )
    print(d[1][idx])
    return d[3][idx]


if __name__ == "__main__":
    queries = [
        "gladiator",
        "invincible",
        "the expanse",
        "the matrix",
        "elf",
        "fellowship of the ring",
        "kill bill",
        "kill bill 2",
        "the wire",
        "trash",
        "memories of murder",
        "memories of murder 2003",
        "oldboy",
        "alien romulus",
    ]
    path = Path("trash")
    if path.exists():
        rmtree(path)
    path.mkdir()
    for q in queries:
        link = get_image_link(q)
        print(link)
        img, suffix = download_image(link)
        (path / f"{q}.{suffix}").write_bytes(img)
