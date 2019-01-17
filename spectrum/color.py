import re
from array import array
from decimal import Decimal
from django.utils.deconstruct import deconstructible

re_hexcolor = re.compile(r'#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})')


@deconstructible
class Color:
    __slots__ = ('_rgba', '_constructor_args')

    def __init__(self, color, opacity=1):
        self._rgba = array('B', [0, 0, 0, 100])
        self.hex = color
        self.opacity = opacity

    def __str__(self):
        if self.opacity == 1:
            return self.hex
        else:
            return self.rgba

    def __repr__(self):
        return "%s('%s', %s)" % (self.__class__.__name__, self.hex, self.opacity)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.opacity == 1 and self.hex == other.upper()
        elif isinstance(other, self.__class__):
            return self._rgba == other._rgba
        else:
            return super().__eq__(other)

    @property
    def hex_code(self):
        return '{:02X}{:02X}{:02X}'.format(*self._rgba[:3])

    @property
    def hex(self):
        return '#' + self.hex_code

    @hex.setter
    def hex(self, value):
        if not isinstance(value, str):
            raise TypeError('color must be a string, got %s' % type(value).__name__)

        match = re_hexcolor.fullmatch(value)
        if match is None:
            raise ValueError('Invalid color: %r. Must be RGB, #RGB, RRGGBB or #RRGGBB' % value)

        color = match.group(1)
        if len(color) == 3:
            color = ''.join(letter * 2 for letter in color)

        for index in range(3):
            self._rgba[index] = int(color[index*2:index*2+2], 16)

    @property
    def opacity(self):
        return Decimal(self._rgba[3]) / 100

    @opacity.setter
    def opacity(self, value):
        if not isinstance(value, (str, int, float, Decimal)):
            raise TypeError('%s(%r) is invalid. Opacity must be one of: str, int, float, Decimal' % (value, value))

        try:
            opacity = Decimal(value)
        except Exception:
            raise TypeError('invalid opacity: %s(%r)' % (value, value))
        if opacity < 0 or opacity > 1:
            raise ValueError('opacity must be between 0 and 1')
        self._rgba[3] = round(opacity * 100)

    @property
    def rgb(self):
        return 'rgb({:d},{:d},{:d})'.format(*self._rgba[:3])

    @property
    def rgba(self):
        return 'rgba({:d},{:d},{:d},{})'.format(
            self._rgba[0],
            self._rgba[1],
            self._rgba[2],
            self.opacity
        )
