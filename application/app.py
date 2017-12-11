#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (Flask, render_template, request)
from json import dumps
from os import makedirs, path


def create_app():
    app = Flask(import_name=__name__)

    submssion_choices = {'0': 'White',
                         '1': 'Red',
                         '2': 'Green',
                         '3': 'Blue',
                         '4': 'Orange',
                         '5': 'Turquoise',
                         '6': 'Purple',
                         '7': 'Yellow',
                         'Ok': 'Off',
                         'Pound': 'Brightness Up',
                         'Star': 'Brightness Down',
                         'Right': 'Speed Up',
                         'Left': 'Speed Down',
                         'Up': 'Mode Up',
                         'Down': 'Mode Down',
                         }

    @app.route('/', methods=['GET', 'POST'])
    def homepage():
        if request.method.lower() == 'post':
            if request.form.get('submission_choice'):
                color = request.form['submission_choice']
                if not path.exists("/home/pi/LED_Project"):
                    makedirs('/home/pi/LED_Project')
                with open('/home/pi/LED_Project/input.json', 'w') as outfile:
                    outfile.write(dumps({'input': color}))
        return render_template('homepage.html',
                               submission_choices=dumps(submssion_choices))

    return app


if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.testing = True
    app.run(port=5000)
