import colorsys
from decimal import Decimal

from . import exceptions, helpers
from .typing import ColorType


class Color:
    def __init__(self, color: ColorType):
        self._rgba = helpers.format_color(color)

    def __str__(self):
        if self.opaque:
            return self.hex()
        else:
            return self.rgba()

    def __repr__(self):
        return "%s('%s')" % (
            self.__class__.__name__,
            self.hex() if self.opaque else self.hexa(),
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._rgba == other._rgba

        try:
            other_color = self.__class__(other)
        except exceptions.InvalidColor:
            return super().__eq__(other)
        else:
            return self._rgba == other_color._rgba

    def __iter__(self):
        return iter(self._rgba)

    def __getitem__(self, item):
        return self._rgba[item]

    @property
    def opaque(self):
        return self._rgba[3] == 255

    def hex(self, value=None):
        if value is None:
            return '#{:02X}{:02X}{:02X}'.format(*self._rgba[:3])
        else:
            color_bytes = helpers.format_hexa(value)
            color_bytes_list = list(color_bytes)
            color_bytes_list[3] = self._rgba[3]  # keep current opacity
            return type(self)(color_bytes_list)

    def hexa(self, value=None):
        if value is None:
            return '#{:02X}{:02X}{:02X}{:02X}'.format(*self._rgba)
        else:
            return type(self)(helpers.format_hexa(value))

    def opacity(self, value=None):
        if value is None:
            # strip trailing zeros
            return round(Decimal(self._rgba[3]) * 100 / 255) / 100
        else:
            opacity = round(Decimal(str(value)) * 255)
            if not 0 <= opacity <= 255:
                raise exceptions.InvalidOpacity(value)

            color_bytes = list(self._rgba[:3])
            color_bytes.append(opacity)
            return type(self)(color_bytes)

    def rgb(self):
        return "rgb({:d}, {:d}, {:d})".format(*self._rgba[:3])

    def rgba(self):
        return "rgba({:d}, {:d}, {:d}, {})".format(
            self._rgba[0], self._rgba[1], self._rgba[2], self.opacity()
        )

    def hsl(self):
        h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in self._rgba[:3]))
        return "hsl({:d}, {}%, {}%)".format(
            round(h * 360), round(s * 1000) / 10, round(l * 1000) / 10
        )

    def hsla(self):
        h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in self._rgba[:3]))
        return "hsla({:d}, {}%, {}%, {})".format(
            round(h * 360), round(s * 1000) / 10, round(l * 1000) / 10, self.opacity()
        )
