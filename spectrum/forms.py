from django import forms
from django.core import exceptions
from django.utils.translation import gettext_lazy as _

from .color import Color
from .exceptions import InvalidColorError
from .widgets import ColorWidget


class ColorField(forms.CharField):
    widget = ColorWidget
    default_error_messages = {
        "invalid": _("Enter a valid color."),
    }

    def clean(self, value):
        if value in self.empty_values:
            return self.empty_value

        try:
            return Color(value)
        except InvalidColorError:
            raise exceptions.ValidationError(
                self.error_messages["invalid"], code="invalid"
            )
