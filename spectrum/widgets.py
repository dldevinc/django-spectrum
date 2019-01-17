from django import forms
from django.utils.translation import gettext_lazy as _
from .color import Color


class ColorWidget(forms.MultiWidget):
    template_name = 'spectrum/widget.html'

    def __init__(self,  attrs=None):
        widgets = (
            forms.TextInput(attrs={
                'maxlength': 7,
                'pattern': '#?(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})'
            }),
            forms.NumberInput(attrs={
                'min': 0,
                'max': 1,
                'step': 0.01,
                'placeholder': _('Opacity'),
            }),
        )
        super().__init__(widgets, attrs)

    @property
    def media(self):
        return forms.Media(
            css={
                'screen': [
                    'spectrum/css/spectrum.css',
                    'spectrum/css/widget.css',
                ],
            },
            js=[
                'spectrum/js/spectrum.js',
                'spectrum/js/widget.js',
            ]
        )

    def decompress(self, value):
        if isinstance(value, str):
            return [value, 1]
        elif isinstance(value, Color):
            return [value.hex, value.opacity]
        return [None, None]
