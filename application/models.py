#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime as DT
from mongoengine import (Document,
                         BooleanField,
                         DateTimeField)


class CustomModel(object):
    updated_date = DateTimeField()
    create_date = DateTimeField()

    def update_dates(self):
        date_now = DT.utcnow()
        self.updated_date = date_now
        if not self.create_date:
            self.create_date = date_now


class Data(Document, CustomModel):
    channel_1 = BooleanField(default=False)

    def clean(self):
        self.update_dates()
