from base64 import b64encode

from flask import Flask, request, send_from_directory

from jboxo.thumbnail import get_image
from jboxo.videoprovider import VideoProvider
from jboxo.wrapper import VLCWrapper


def create_app():
    """Initializes REST backend."""

    provider = VideoProvider()
    wrapper = VLCWrapper(provider)

    app = Flask(
        __name__, static_folder="../frontend/vite-project/dist", static_url_path="/"
    )

    @app.get("/api/movies")
    def list_movies():
        return provider.get_movie_data()

    @app.get("/api/series")
    def list_series():
        return provider.get_series_data()

    @app.get("/api/subtitles")
    def list_subtitles():
        return provider.get_subtitle_data()

    @app.get("/api/thumbnail/<query>")
    def get_thumbnail(query):
        img, suffix = get_image(query)
        return f'<img src="data:image/{suffix};base64,{b64encode(img).decode()}" />'

    @app.get("/api/selected")
    def get_selected_info():
        return wrapper.get_selected_info()

    @app.post("/api/control/<cmd>")
    def execute_command(cmd):
        data = request.data.decode()
        wrapper.execute(cmd, data)
        return "Success", 200

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            f"{app.root_path}/static",
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app
