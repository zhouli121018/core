#!coding=utf-8
from django.db import models
from django import forms
import form_fields

class ZeroDateField(models.DateField):
    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts datetimes into the format expected by the backend
        if not prepared:
            value = self.get_prep_value(value)

        # Use zeroed datetime instead of NULL
        if value is None:
            return "0000-00-00"
        else:
            return connection.ops.adapt_datefield_value(value)



class RevCharBooleanField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        super(RevCharBooleanField, self).__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return '-1' if value else '1'


    def formfield(self, **kwargs):
        # Unlike most fields, BooleanField figures out include_blank from
        # self.null instead of self.blank.
        if self.choices:
            include_blank = not (self.has_default() or 'initial' in kwargs)
            defaults = {'choices': self.get_choices(include_blank=include_blank)}
        else:
            defaults = {'form_class': form_fields.RevCharBooleanField}
        defaults.update(kwargs)
        return super(RevCharBooleanField, self).formfield(**defaults)

class CharBooleanField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        super(CharBooleanField, self).__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return '1' if value else '-1'

    def formfield(self, **kwargs):
        # Unlike most fields, BooleanField figures out include_blank from
        # self.null instead of self.blank.
        if self.choices:
            include_blank = not (self.has_default() or 'initial' in kwargs)
            defaults = {'choices': self.get_choices(include_blank=include_blank)}
        else:
            defaults = {'form_class': form_fields.CharBooleanField}
        defaults.update(kwargs)
        return super(CharBooleanField, self).formfield(**defaults)
