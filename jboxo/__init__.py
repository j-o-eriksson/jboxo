import json

from flask import Flask, render_template, send_from_directory

from jboxo.utils import wake_screen
from jboxo.videoprovider import VideoProvider
from jboxo.wrapper import VLCWrapper


def create_app():
    """Initializes REST backend."""

    provider = VideoProvider()
    wrapper = VLCWrapper(provider)

    app = Flask(__name__)

    @app.get("/videos")
    def list_videos():
        return json.dumps(wrapper.get_videos(), indent=2)

    @app.get("/subtitles")
    def list_subtitles():
        return json.dumps(wrapper.get_subtitles(), indent=2)

    @app.get("/selected")
    def get_selected_info():
        return json.dumps(wrapper.get_selected_info(), indent=2)

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
