import io
import json
from pathlib import Path
from shutil import rmtree

import requests
from bs4 import BeautifulSoup
from PIL import Image

HEADERS = {
    "User-Agent": "CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)"
}
PLACEHOLDER = Path("data/placeholder.png").read_bytes()


def get_image(query: str):
    link = get_wiki_link(query)
    if link is None:
        return PLACEHOLDER, "png"

    out = download_image(link)
    if out is None:
        return PLACEHOLDER, "png"
    return out


def download_image(url: str) -> tuple[bytes, str] | None:
    html_response = requests.get(url)
    soup = BeautifulSoup(html_response.content, "html.parser")

    tags = soup.find_all("img")
    for tag in tags:
        src = tag.get("src")
        if "upload" in src:
            w = int(tag.get("width"))
            h = int(tag.get("height"))
            *_, suffix = src.split(".")
            if h * w < 100**2:
                print(f"to small: w: {w}, h: {h}")
                continue

            img_response = requests.get(f"https:{src}", headers=HEADERS)
            if img_response.status_code == 200:
                return img_response.content, suffix
            print(f"failed to download {url} due to {img_response.reason}")

    return None


def get_wiki_link(query: str) -> str | None:
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
    if len(d[3]) == 0:
        return None
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
        "the lion king",
        "severance",
    ]

    path = Path("trash")
    if path.exists():
        rmtree(path)
    path.mkdir()

    for q in queries:
        img, suffix = get_image(q)
        im = Image.open(io.BytesIO(img))
        im.save((path / f"{q}.{suffix}"))
