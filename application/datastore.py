#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_security import MongoEngineUserDatastore
from flask import current_app
from datetime import datetime as DT
from mongoengine.errors import ValidationError, NotUniqueError

try:
    from mongoengine.queryset import Q, QCombination
except ImportError:
    from mongoengine.queryset.visitor import Q, QCombination


class RelayUIDatastore(MongoEngineUserDatastore):
    def __init__(self, db, user_model, role_model, data_model):
        MongoEngineUserDatastore.__init__(self, db=db, user_model=user_model, role_model=role_model)
        self.data_model = data_model

    def update_data(self, data_object):
        try:
            return True, self.put(data_object)
        except Exception, e:
            return False, e

    def find_data(self):
        try:
            return True, self.data_model.objects().first()
        except Exception, e:  # pragma: no cover
            return False, e

