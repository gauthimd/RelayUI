#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (Flask, render_template, request)
from json import dumps


def create_app():
    app = Flask(import_name=__name__)

    @app.route('/', methods=['GET', 'POST'])
    def homepage():
        if request.method.lower() == 'post':
            if request.form.get('color'):
                color = request.form['color']
                with open('/home/pi/LED_Project/input.json', 'w') as outfile:
                    outfile.write(dumps({'color': color}))
        return render_template('homepage.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.testing = True
    app.run(port=5000)