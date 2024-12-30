import json
from base64 import b64encode

from flask import Flask, render_template, send_from_directory

from jboxo.thumbnail import download_image, get_image_link
from jboxo.utils import wake_screen
from jboxo.videoprovider import VideoProvider
from jboxo.wrapper import VLCWrapper


def create_app():
    """Initializes REST backend."""

    provider = VideoProvider()
    wrapper = VLCWrapper(provider)

    app = Flask(__name__)

    @app.get("/movies")
    def list_movies():
        return provider.get_movie_data()

    @app.get("/series")
    def list_series():
        return provider.get_series_data()

    @app.get("/subtitles")
    def list_subtitles():
        return json.dumps(wrapper.get_subtitles(), indent=2)

    @app.get("/thumbnail/<query>")
    def get_thumbnail(query):
        link = get_image_link(query)
        img, suffix = download_image(link)
        return f'<img src="data:image/{suffix};base64,{b64encode(img).decode()}" />'

    @app.get("/selected")
    def get_selected_info():
        return wrapper.get_selected_info()

    @app.post("/control/<cmd>")
    def execute_command(cmd):
        wrapper.execute(cmd)
        return "Success", 200

    @app.post("/wake")
    def wake():
        wake_screen()
        return "Success", 200

    @app.route("/")
    def index():
        # return send_from_directory(f"{app.root_path}/../frontend/build", "index.html")
        return render_template("index.html")

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            f"{app.root_path}/static",
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app
