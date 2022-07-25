from pathlib import Path

from flask import Flask


app = Flask(__name__)
root = Path("/home/jon/dev/jboxo/data")

@app.post('/control')
def execute_command(cmd: str):
    return cmd


@app.get('/list')
def list_objects():
    items = "".join([f"<p>{p.name}</p>" for p in root.iterdir()])
    return items


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

