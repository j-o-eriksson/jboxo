#!/bin/sh
export DISPLAY=:0
export FLASK_APP=jboxo
export FLASK_ENV=development
flask run --host=0.0.0.0 --debug
