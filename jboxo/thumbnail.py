import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def download_image(url) -> tuple[bytes, str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tags = soup.find_all("img")
    for i, tag in enumerate(tags):
        src = tag.get("src")
        if "upload" in src:
            *_, suffix = src.split(".")
            r2 = requests.get(f"https:{src}")
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
    queries = ["gladiator II", "invincible", "the expanse", "the matrix", "elf"]
    path = Path("trash")
    for q in queries:
        link = get_image_link(q)
        print(link)
        img, suffix = download_image(link)
        (path / f"{q}.{suffix}").write_bytes(img)
