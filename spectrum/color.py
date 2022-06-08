import array
import colorsys
import copy
from decimal import Decimal

from . import exceptions, helpers
from .typing import ColorInputType


class Color:
    """
    Possible inputs:
        Color("FFFF00")
        Color("#FFFF00")
        Color("#ffff0080")

        Color("rgb(255, 255, 0)")
        Color("rgba(255, 255, 0, 0.5)")
        Color("rgba(255 255 0 / 50%)")

        Color([255, 255, 0])
        Color([255, 255, 0, 128])
    """

    __slots__ = ("_rgba", )

    def __init__(self, color: ColorInputType):
        color_bytes = helpers.format_color(color)
        self._rgba = array.array("B", color_bytes)

    def __str__(self):
        return self.hex if self.opaque else self.rgba

    def __repr__(self):
        return "%s('%s')" % (
            self.__class__.__name__,
            self.hex if self.opaque else self.hexa,
        )

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._rgba == other._rgba

        try:
            other_color = self.__class__(other)
        except exceptions.InvalidColorError:
            return super().__eq__(other)
        else:
            return self._rgba == other_color._rgba

    def __iter__(self):
        return iter(self._rgba)

    def __getitem__(self, item):
        return self._rgba[item]

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result._rgba = copy.copy(self._rgba)
        return result

    def __hash__(self):
        return int(self.hexa, 16)

    @property
    def red(self) -> int:
        return self._rgba[0]

    @property
    def green(self) -> int:
        return self._rgba[1]

    @property
    def blue(self) -> int:
        return self._rgba[2]

    @property
    def alpha(self) -> int:
        """
        :return: number between 0 and 255
        """
        return self._rgba[3]

    @property
    def opacity(self) -> Decimal:
        """
        :return: percentage of opacity from 0 to 1
        """
        return helpers.color_byte_to_percentage(self.alpha)

    @property
    def opaque(self) -> bool:
        return self.alpha == 255

    @property
    def transparent(self) -> bool:
        return self.alpha == 0

    @property
    def hex(self):
        return "#{:02X}{:02X}{:02X}".format(*self._rgba[:3])

    @property
    def hexa(self):
        return "#{:02X}{:02X}{:02X}{:02X}".format(*self._rgba)

    @property
    def rgb(self):
        return "rgb({:d}, {:d}, {:d})".format(*self._rgba[:3])

    @property
    def rgba(self):
        return "rgba({:d}, {:d}, {:d}, {:f})".format(
            self._rgba[0],
            self._rgba[1],
            self._rgba[2],
            self.opacity
        )

    @property
    def hsl(self):
        h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in self._rgba[:3]))
        return "hsl({:d}, {}%, {}%)".format(
            round(h * 360),
            round(s * 100),
            round(l * 100)
        )

    @property
    def hsla(self):
        h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in self._rgba[:3]))
        return "hsla({:d}, {:d}%, {:d}%, {})".format(
            round(h * 360),
            round(s * 100),
            round(l * 100),
            self.opacity
        )

    def as_tuple(self):
        return tuple(self._rgba)
