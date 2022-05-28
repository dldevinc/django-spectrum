import re
from decimal import ROUND_HALF_UP, Decimal
from typing import Iterable, Union

from . import exceptions
from .typing import ColorByte, ColorBytes, ColorInputType

# HEX color:
#   RGB / RGBA / RRGGBB / RRGGBBAA /
#   #RGB / #RGBA / #RRGGBB / #RRGGBBAA
re_hexa = re.compile(r'#?([\dA-Fa-f]{3,4}|[\dA-Fa-f]{6}|[\dA-Fa-f]{8})')

# RGBA color in one of two possible notations:
#   rgba(R, G, B, A) or rgba(R G B / A%)
re_rgba = re.compile(
    r'rgba?[\D]+?([-\d]+)[\D]+?([-\d]+)[\D]+?([-\d]+)(?:[\D]+?([-\d.]+%?))?[\D]+'
)


def fraction_to_color_byte(value: Union[str, int, float, Decimal]) -> ColorByte:
    """
    Examples:
        "1" => 255
        "0.5" => 128
        "0.3" => 77
    """
    return int(
        (Decimal(value) * 255).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )


def color_byte_to_percentage(value: ColorByte) -> Decimal:
    """
    Examples:
         0 => Decimal(0)
         128 => Decimal('0.50')
         255 => Decimal('1')

    :param value: often an alpha component from 0 to 255
    :return: percentage from 0 to 1
    """
    percentage = (Decimal(value) / 255).quantize(Decimal("0.01"))
    normalized = percentage.normalize()
    sign, digits, exponent = normalized.as_tuple()
    if exponent > 0:
        return Decimal((sign, digits + (0,) * exponent, 0))
    else:
        return normalized


def format_color_byte(value: Union[int, str]) -> ColorByte:
    """
    :param value: R, G, B or A component
    :raises TypeError:
                value type is not either an int or str
    :raises ValueError:
                value can't be converted to integer
    :raises OverflowError:
                value is out of bounds
    """
    if isinstance(value, int):
        pass
    elif isinstance(value, str):
        value = int(value)
    else:
        raise TypeError(value)

    if not 0 <= value <= 255:
        raise OverflowError(value)

    return value


def format_color_bytes(sequence: Iterable[Union[int, str]]) -> ColorBytes:
    """
    Examples:
      ["128", "192", "128"] => (128, 192, 128, 255)
      ["128", "192", "0", "64"] => (128, 192, 0, 64)

    :return: 4-tuple of (R, G, B, A)
    :raises TypeError:
                type of any component is not either an int or str
    :raises ValueError:
                any component can't be converted to integer
    :raises OverflowError:
                any component is out of bounds
                or component count is not in a range from 3 to 4
    """
    sequence = tuple(map(format_color_byte, sequence))

    length = len(sequence)
    if length == 3:
        sequence = sequence + (255, )
    elif length == 4:
        pass
    else:
        raise OverflowError(sequence)

    return sequence


def format_rgba(sequence) -> ColorBytes:
    """
    Examples:
      [128, 192, 64] => (128, 192, 64, 255)
      ["128", "192", "64", "0.5"] => (128, 192, 64, 128)
      ["128", "192", "64", "50%"] => (128, 192, 64, 128)
    """
    components = list(sequence)

    # Convert fraction to byte
    # https://stackoverflow.com/questions/5445085/understanding-colors-on-android-six-characters/11019879#11019879
    if len(components) == 4:
        opacity = components[3]

        if not isinstance(opacity, str):
            opacity = str(opacity)

        if opacity.endswith("%"):
            opacity = Decimal(opacity.rstrip("%")) / 100
            components[3] = fraction_to_color_byte(opacity)
        else:
            components[3] = fraction_to_color_byte(opacity)

    return format_color_bytes(components)


def format_hexa(value: str) -> ColorBytes:
    """
    Examples:
      "bda" => (187, 221, 170, 255)
      "4fcd" => (68, 255, 204, 221)
      "60B0C4" => (96, 176, 196, 255)
      "2BEA40D0" => (43, 234, 64, 208)
    """
    length = len(value)
    if length in {3, 4}:
        value = "".join(s * 2 for s in value)
        length *= 2
    elif length in {6, 8}:
        pass
    else:
        raise ValueError(value)

    hex_parts = [value[i:(i + 2)] for i in range(0, length, 2)]
    return format_color_bytes(int(v, 16) for v in hex_parts)


def format_color(value: ColorInputType) -> ColorBytes:
    """
    :param value: HEX or RGBA color
    :return: 4-tuple of (R, G, B, A)
    :raises InvalidColorTypeError:
                value is not an iterable
    :raises InvalidColorValueError:
                value can't be converted to Color
    """
    if isinstance(value, str):
        hexa_match = re_hexa.fullmatch(value)
        if hexa_match is not None:
            try:
                return format_hexa(hexa_match.group(1))
            except (ValueError, TypeError):
                raise exceptions.InvalidColorValueError(value)

        rgba_match = re_rgba.fullmatch(value)
        if rgba_match is not None:
            components = rgba_match.groups()
            if components[3] is None:
                components = components[:3]

            try:
                return format_rgba(components)
            except (ValueError, TypeError, OverflowError):
                raise exceptions.InvalidColorValueError(value)

        raise exceptions.InvalidColorValueError(value)
    elif isinstance(value, Iterable):
        try:
            return format_color_bytes(value)
        except (ValueError, TypeError, OverflowError):
            raise exceptions.InvalidColorValueError(value)
    else:
        raise exceptions.InvalidColorTypeError(value)
