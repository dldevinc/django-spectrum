import re
from decimal import Decimal
from typing import Iterable

from . import exceptions
from .typing import ColorBytes, ColorType

re_hexa = re.compile(r'#?([\dA-Fa-f]{3,4}|[\dA-Fa-f]{6}|[\dA-Fa-f]{8})')
re_rgba = re.compile(
    r'rgba?[\D]+?([-\d]+)[\D]+?([-\d]+)[\D]+?([-\d]+)(?:[\D]+?([-\d.]+))?[\D]+'
)


def format_color_byte(value) -> int:
    if isinstance(value, int):
        component = value
    elif isinstance(value, str):
        component = int(value)
    else:
        raise TypeError(value)

    if not 0 <= component <= 255:
        raise ValueError

    return component


def format_color_bytes(sequence) -> ColorBytes:
    """
    Examples:
      ["128", "192", "128"] => (128, 192, 128, 255)
      ["128", "192", "0", "64"] => (128, 192, 0, 64)
    """
    components = list(sequence)
    if len(components) not in {3, 4}:
        raise ValueError(components)

    if len(components) == 3:
        components.append(255)

    return tuple(map(format_color_byte, components))


def format_rgba(sequence) -> ColorBytes:
    """
    Examples:
      [128, 192, 64] => (128, 192, 64, 255)
      ["128", "192", "64", "0.5"] => (128, 192, 64, 128)
    """
    components = list(sequence)

    # Convert fraction to byte
    # https://stackoverflow.com/questions/5445085/understanding-colors-on-android-six-characters/11019879#11019879
    if len(components) == 4:
        opacity = components[3]

        if not isinstance(opacity, str):
            opacity = str(opacity)

        components[3] = round(Decimal(opacity) * 255)

    return format_color_bytes(components)


def format_hexa(value: str) -> ColorBytes:
    """
    Examples:
      "bda" => (187, 221, 170, 255)
      "4fcd" => (68, 255, 204, 221)
      "60B0C4" => (96, 176, 196, 255)
      "2BEA40D0" => (43, 234, 64, 208)
    """
    if len(value) in {3, 4}:
        expanded_color = ''.join(s * 2 for s in value)
    else:
        expanded_color = value

    length = len(expanded_color)
    if length in {6, 8}:
        hex_parts = [expanded_color[i:(i + 2)] for i in range(0, length, 2)]
        return format_color_bytes([int(v, 16) for v in hex_parts])
    else:
        raise ValueError(value)


def format_color(value: ColorType) -> ColorBytes:
    if isinstance(value, str):
        hexa_match = re_hexa.fullmatch(value)
        if hexa_match is not None:
            try:
                return format_hexa(hexa_match.group(1))
            except (ValueError, TypeError):
                raise exceptions.InvalidColorValue(value)

        rgba_match = re_rgba.fullmatch(value)
        if rgba_match is not None:
            color_items = rgba_match.groups()
            if color_items[3] is None:
                color_items = color_items[:3]

            try:
                return format_rgba(color_items)
            except (ValueError, TypeError):
                raise exceptions.InvalidColorValue(value)

        raise exceptions.InvalidColorValue(value)
    elif isinstance(value, Iterable):
        try:
            return format_color_bytes(value)
        except (ValueError, TypeError):
            raise exceptions.InvalidColorValue(value)
    else:
        raise exceptions.InvalidColorType(value)
