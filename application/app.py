#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (Flask, g, abort, render_template, request, jsonify, get_flashed_messages, current_app)
from flask_security import UserMixin, RoleMixin
from models import Data
from datastore import RelayUIDatastore
from extensions import db, security
from forms import ChannelForm


#################################################
# BUILD OUR FLASK APPLICATION
#################################################

def create_app(settings_override=None):
    app = Flask(import_name=__name__)
    app.config['SECRET_KEY'] = 'nomorestupidfuckinguuidscuztheybreakeverything'
    app.config['MONGODB_DB'] = 'RelayUI'
    app.config['MONGODB_HOST'] = 'localhost'
    app.config['MONGODB_PORT'] = 27017  # this should never change
    app.config['MONGODB_CONNECT'] = False

    app.debug = True

    app.logger.info('Loaded app with configs, launching datastore')
    user_datastore = RelayUIDatastore(db=db, user_model=UserMixin, role_model=RoleMixin, data_model=Data)

    app.logger.info('Launching extensions')

    security.init_app(app=app,
                      datastore=user_datastore,
                      register_blueprint=False)
    db.init_app(app=app)

    @app.before_request
    def before_request():
        try:
            g.datastore = app.extensions['security'].datastore
        except Exception, e:
            app.logger.critical('Critical error before request: {}'.format(e))
            abort(500)

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html',
                               channel_form=ChannelForm())

    @app.route('/submit_channel/', methods=['POST'])
    def submit_channel():
        try:
            form = ChannelForm()
            if form.validate_on_submit():
                if form.update_data():
                    return jsonify({'message': get_flashed_messages(category_filter='success')}), 200, {}
        except Exception, e:
            current_app.logger.error('Fatal error updating data; error: {}'.format(e))
            jsonify({'message_modal': get_flashed_messages(category_filter='error')}), 500, {}

        return jsonify({'message': get_flashed_messages(category_filter='error')}), 500, {}

    return app
