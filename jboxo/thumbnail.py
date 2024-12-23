from io import BytesIO

import requests
from bs4 import BeautifulSoup
from PIL import Image


def download_image(url, path):
    """download the image"""
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # img = img.resize((200, 320))
    img.save(path)


def get_image_link(query):
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    tags = soup.find_all("img")
    for tag in tags:
        src = tag.get("src")
        if src.startswith("http"):
            return src
    return None


# def get_poster(imdb_id: str):
#     # url = f"https://www.imdb.com/title/{imdb_id}/"
#     url = "https://www.imdb.com/title/tt15398776/"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     tag = soup.find("a", {"class": "ipc-lockup-overlay ipc-focusable"})
#     breakpoint()
#     if tag is None:
#         return None
#     href = tag.get("href")
#     return get_image(f"https://www.imdb.com{href}")
#
#
# def get_image(href: str):
#     print(href)
