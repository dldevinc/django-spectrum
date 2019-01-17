from django import forms
from django.core import exceptions
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .color import Color
from .widgets import ColorWidget


class ColorField(forms.MultiValueField):
    widget = ColorWidget
    default_error_messages = {
        'invalid_color': _('Enter a valid color.'),
        'invalid_opacity': _('Enter a valid opacity.'),
    }

    def __init__(self, fields=(), *args, **kwargs):
        if not fields:
            fields = (
                forms.CharField(
                    validators=[
                        RegexValidator(r'^#?(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$', code='invalid_color'),
                    ],
                    error_messages={
                        'incomplete': _('Hex value required.'),
                    }
                ),
                forms.DecimalField(
                    min_value=0,
                    max_value=1,
                    max_digits=3,
                    decimal_places=2,
                    error_messages={
                        'incomplete': _('Opacity required.'),
                        'min_value': _('Ensure opacity is greater than or equal to %(limit_value)s.'),
                        'max_value': _('Ensure opacity is less than or equal to %(limit_value)s.'),
                    }
                ),
            )
        kwargs['require_all_fields'] = False
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in self.empty_values:
                raise exceptions.ValidationError(
                    self.error_messages['invalid_color'],
                    code='invalid_color'
                )
            if data_list[1] in self.empty_values:
                raise exceptions.ValidationError(
                    self.error_messages['invalid_opacity'],
                    code='invalid_opacity'
                )
            try:
                return Color(*data_list)
            except (TypeError, ValueError):
                raise exceptions.ValidationError(
                    self.error_messages['invalid_color'],
                    code='invalid_color'
                )
        return None
