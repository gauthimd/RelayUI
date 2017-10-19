#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_mongoengine import MongoEngine
from flask_security import Security

db = MongoEngine()
security = Security()
