#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import current_app, flash, g
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import NumberRange

from models import Data


class CustomForm(FlaskForm):
    def __init__(self, **kwargs):
        self.validated = False
        self.success_message = None
        self.field_values = {}
        try:
            self.user_input_fields
        except:
            self.user_input_fields = []
        for field in self.user_input_fields:
            self.field_values.update({field: None})
        FlaskForm.__init__(self, **kwargs)

    def validation_success(self):
        current_app.logger.info('Form validated successfully')
        return True

    def validation_error(self):
        current_app.logger.error('Form did not validate: {}'.format(self.errors))
        flash(self.errors, 'error')
        return False

    def update_success(self):
        flash(self.success_message, 'success')
        current_app.logger.info('Successfully updated form data')
        return True

    def update_error(self):
        flash(self.errors, 'error')
        current_app.logger.error('Unable to update values: {}'.format(self.errors))
        return False

    def validate_on_submit(self):
        valid = True
        if not FlaskForm.validate_on_submit(self):
            valid = False
            current_app.logger.error('Validity check failed on FlaskForm fields')
        return valid

    def append_error_with_field_name(self, field_name, message):
        if not self.errors.get(field_name):
            self.errors[field_name] = []
        self.errors[field_name].append(str(message))


class ChannelForm(CustomForm):
    channel_number = HiddenField()
    submit = SubmitField()

    def __init__(self, **kwargs):
        CustomForm.__init__(self, **kwargs)

    def validate_on_submit(self):
        self.submit.data = True
        if not CustomForm.validate_on_submit(self):
            return self.validation_error()
        self.validated = True
        return self.validation_success()

    def update_data(self):
        if not self.validated:
            return False
        success, channel_data = g.datastore.find_data()
        print channel_data.channel_1
        if channel_data.channel_1:
            channel_data.channel_1 = False
        else:
            channel_data.channel_1 = True
        print 'yo'
        success, data = g.datastore.update_data(channel_data)
        print success, data
        if success:
            current_app.logger.info('Donezo')
            return self.update_success()
        else:
            current_app.logger.error('Failure updating data')
            try:
                self.append_error_with_field_name(field_name=data.field_name, message=data)
            except:
                self.channel_number.errors.append(data)
            return self.update_error()
