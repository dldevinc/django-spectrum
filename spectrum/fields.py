from django.db import models
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from .color import Color
from . import forms


def encode_color(color):
    if color.opacity == 1:
        return color.hex_code
    else:
        return '{}:{}'.format(color.hex_code, color.opacity)


def decode_color(color_string):
    color, _, opacity = color_string.partition(':')
    return Color(color, opacity or 1)


class ColorField(models.Field):
    default_error_messages = {
        'invalid': _("'%(value)s' value must be a RGB/RGBA color."),
    }
    description = _("RGB/RGBA color")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 12
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    @staticmethod
    def from_db_value(value, *args, **kwargs):
        if value is None:
            return value
        return decode_color(value)

    def to_python(self, value):
        if isinstance(value, Color):
            return value

        if value is None:
            return None

        try:
            return decode_color(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        if isinstance(value, Color):
            return encode_color(value)
        return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.ColorField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
