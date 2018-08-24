from django.forms import BooleanField, DateTimeField
from django.utils import six
# from django.utils.timezone import datetime
import datetime
import time
from django.forms.utils import from_current_timezone, to_current_timezone

class RevCharBooleanField(BooleanField):

    def bound_data(self, data, initial):
        """
        Return the value that should be shown for this field on render of a
        bound form, given the submitted POST data for the field and the initial
        data, if any.

        For most fields, this will simply be data; FileFields need to handle it
        a bit differently.
        """
        if self.disabled:
            return initial
        return '-1' if data else '1'

    def prepare_value(self, value):
        if isinstance(value, six.string_types):
            try:
                if int(value) > 0:
                    value = False
            except ValueError:
                pass
        elif isinstance(value, six.integer_types):
            if value > 0:
                value = False
        else:
            value = bool(value)
        return value

class CharBooleanField(BooleanField):


    def bound_data(self, data, initial):
        """
        Return the value that should be shown for this field on render of a
        bound form, given the submitted POST data for the field and the initial
        data, if any.

        For most fields, this will simply be data; FileFields need to handle it
        a bit differently.
        """
        if self.disabled:
            return initial
        return '1' if data else '-1'

    def prepare_value(self, value):
        if isinstance(value, six.string_types):
            try:
                if int(value) <= 0:
                    value = False
            except ValueError:
                pass
        elif isinstance(value, six.integer_types):
            if value <= 0:
                value = False
        else:
            value = bool(value)
        return value

class IntDateTimeField(DateTimeField):
    def to_python(self, value):
        """
        Validates that the input can be converted to a datetime. Returns a
        Python datetime.datetime object.
        """
        result = super(IntDateTimeField, self).to_python(value)
        if result:
            result = int(time.mktime(result.timetuple()))
        return result


    def prepare_value(self, value):
        if not value:
            value = int(time.time())
        if isinstance(value, six.integer_types):
            value = datetime.datetime.fromtimestamp(value)
        return value
