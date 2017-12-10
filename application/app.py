#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (Flask, render_template, request)
from json import dumps
from os import makedirs, path


def create_app():
    app = Flask(import_name=__name__)

    @app.route('/', methods=['GET', 'POST'])
    def homepage():
        if request.method.lower() == 'post':
            if request.form.get('mode'):
                color = request.form['mode']
                if not path.exists("/home/pi/LED_Project"):
                    makedirs('/home/pi/LED_Project')
                with open('/home/pi/LED_Project/input.json', 'w') as outfile:
                    outfile.write(dumps({'input': color}))
        return render_template('homepage.html')

    return app


if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.testing = True
    app.run(port=5000)
