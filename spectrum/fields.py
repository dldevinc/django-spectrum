from decimal import Decimal

from django.core import exceptions
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import forms
from .color import Color
from .exceptions import InvalidColorError


def encode_color(color):
    return color.hex if color.opaque else color.hexa


def parse_color(value: str):
    if ":" in value:
        # v0.1.0 compat
        color, _, opacity = value.partition(":")
        hex_opacity = "{:02X}".format(round(Decimal(str(opacity)) * 255))
        return Color(color + hex_opacity)
    else:
        return Color(value)


class ColorField(models.Field):
    default_error_messages = {
        "invalid": _("'%(value)s' value must be a RGB/RGBA color."),
    }
    description = _("RGB/RGBA color")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 12
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.max_length == 12:
            del kwargs["max_length"]
        return name, path, args, kwargs

    def from_db_value(self, value, *args, **kwargs):
        if value in self.empty_values:
            return None

        return parse_color(value)

    def to_python(self, value):
        if isinstance(value, Color):
            return value

        if value in self.empty_values:
            return None

        try:
            return parse_color(value)
        except InvalidColorError:
            raise exceptions.ValidationError(
                self.error_messages["invalid"], code="invalid", params={"value": value},
            )

    def get_prep_value(self, value):
        value = super().get_prep_value(value)

        if value in self.empty_values:
            return ""

        if not isinstance(value, Color):
            value = parse_color(value)

        return encode_color(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.ColorField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
