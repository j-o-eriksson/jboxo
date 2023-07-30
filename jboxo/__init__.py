import json

from flask import Flask, render_template, send_from_directory

from jboxo.wrapper import VLCWrapper


def create_app():
    """Initializes REST backend."""

    dummy = VLCWrapper()
    app = Flask(__name__)

    @app.post("/control/<cmd>")
    def execute_command(cmd):
        dummy.execute(cmd)
        return "Success", 200

    @app.get("/videos")
    def list_videos():
        return json.dumps(dummy.get_videos(), indent=2)

    @app.get("/subtitles")
    def list_subtitles():
        return json.dumps(dummy.get_subtitles(), indent=2)

    @app.get("/selected")
    def get_selected_info():
        return json.dumps(dummy.get_selected_info(), indent=2)

    @app.route("/")
    def hello_world():
        return render_template("index.html")

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            f"{app.root_path}/static",
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app
