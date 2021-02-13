import pytest

from spectrum.helpers import (
    format_color_byte,
    format_color_bytes,
    format_hexa,
    format_rgba,
    format_color,
    re_hexa,
    re_rgba,
)
from spectrum.exceptions import InvalidColorValue, InvalidColorType


class TestHexRegex:
    def test_hex_rgb(self):
        match = re_hexa.fullmatch("CB0")
        assert match is not None
        assert match.group(1) == "CB0"

        match = re_hexa.fullmatch("#bd8")
        assert match is not None
        assert match.group(1) == "bd8"

    def test_hex_rgba(self):
        match = re_hexa.fullmatch("da88")
        assert match is not None
        assert match.group(1) == "da88"

        match = re_hexa.fullmatch("#FF00")
        assert match is not None
        assert match.group(1) == "FF00"

    def test_hex_rrggbb(self):
        match = re_hexa.fullmatch("BACCEF")
        assert match is not None
        assert match.group(1) == "BACCEF"

        match = re_hexa.fullmatch("#808080")
        assert match is not None
        assert match.group(1) == "808080"

    def test_hex_rrggbbaa(self):
        match = re_hexa.fullmatch("2fcb60ff")
        assert match is not None
        assert match.group(1) == "2fcb60ff"

        match = re_hexa.fullmatch("#ba200060")
        assert match is not None
        assert match.group(1) == "ba200060"


class TestRGBRegex:
    def test_rgb(self):
        match = re_rgba.fullmatch("rgb(255, 255, 0)")
        assert match is not None
        assert match.groups() == ("255", "255", "0", None)

    def test_rgba(self):
        match = re_rgba.fullmatch("rgba(64, 128, 192, 0.5)")
        assert match is not None
        assert match.groups() == ("64", "128", "192", "0.5")


class TestFormatColorByte:
    def test_none(self):
        with pytest.raises(TypeError):
            format_color_byte(None)

    def test_empty_string(self):
        with pytest.raises(ValueError):
            format_color_byte("")

    def test_nondigit_string(self):
        with pytest.raises(ValueError):
            format_color_byte("FF")

    def test_string(self):
        assert format_color_byte("64") is 64

    def test_int(self):
        assert format_color_byte(64) is 64

    def test_float(self):
        with pytest.raises(TypeError):
            format_color_byte(64.5)

    def test_min_value(self):
        assert format_color_byte("0") is 0

    def test_max_value(self):
        assert format_color_byte("255") is 255

    def test_below_bounds(self):
        with pytest.raises(ValueError):
            format_color_byte("-1")

    def test_above_bounds(self):
        with pytest.raises(ValueError):
            format_color_byte("256")


class TestFormatColorBytes:
    def test_insufficient_length(self):
        with pytest.raises(ValueError):
            format_color_bytes([128, 192])

    def test_excessive_length(self):
        with pytest.raises(ValueError):
            format_color_bytes([128, 192, 64, 0, 128])

    def test_auto_opacity(self):
        assert format_color_bytes([128, "92", 64]) == (128, 92, 64, 255)

    def test_stability(self):
        input = ["192", "128", "64"]
        output = format_color_bytes(input)
        assert format_color_bytes(output) == output == (192, 128, 64, 255)


class TestFormatRGBA:
    def test_short(self):
        assert format_rgba(["192", "128", "64"]) == (192, 128, 64, 255)

    def test_transparent(self):
        assert format_rgba(["192", "128", "64", "0"]) == (192, 128, 64, 0)

    def test_opaque(self):
        assert format_rgba([94, 72, 156]) == (94, 72, 156, 255)
        assert format_rgba([94, 72, 156, 1]) == (94, 72, 156, 255)

    def test_fraction_opacity(self):
        assert format_rgba([92, 40, 128, 0.5]) == (92, 40, 128, 128)


class TestFormatHEXA:
    def test_rgb(self):
        assert format_hexa("bda") == (187, 221, 170, 255)

    def test_rgba(self):
        assert format_hexa("4fcd") == (68, 255, 204, 221)

    def test_rrggbb(self):
        assert format_hexa("60B0C4") == (96, 176, 196, 255)

    def test_rrggbbaa(self):
        assert format_hexa("2BEA40D0") == (43, 234, 64, 208)


class TestFormatColor:
    def test_short_hex(self):
        assert format_color("aac") == (170, 170, 204, 255)
        assert format_color("#da0") == (221, 170, 0, 255)

    def test_short_hexa(self):
        assert format_color("cde0") == (204, 221, 238, 0)
        assert format_color("#ff08") == (255, 255, 0, 136)

    def test_hex(self):
        assert format_color("DDA0C4") == (221, 160, 196, 255)
        assert format_color("#2F4BEF") == (47, 75, 239, 255)

    def test_hexa(self):
        assert format_color("C0B0D080") == (192, 176, 208, 128)
        assert format_color("#4B6D321A") == (75, 109, 50, 26)

    def test_rgb(self):
        assert format_color("rgb(75, 109, 26)") == (75, 109, 26, 255)

    def test_rgba(self):
        assert format_color("rgba(98, 212, 204, 0.89)") == (98, 212, 204, 227)

    def test_short_iterable(self):
        assert format_color(["67", "120", "64"]) == (67, 120, 64, 255)

    def test_iterable(self):
        assert format_color([32, 64, 128, 72]) == (32, 64, 128, 72)

    def test_insufficient_hex_length(self):
        with pytest.raises(InvalidColorValue):
            format_color("FF")

    def test_excessive_hex_length(self):
        with pytest.raises(InvalidColorValue):
            format_color("FFAABBDDEE")

    def test_non_hex(self):
        with pytest.raises(InvalidColorValue):
            format_color("XYZ")

    def test_insufficient_rgb_length(self):
        with pytest.raises(InvalidColorValue):
            format_color("rgb(128, 192)")

    def test_excessive_rgb_length(self):
        with pytest.raises(InvalidColorValue):
            format_color("rgb(32, 64, 92, 128, 255)")

    def test_rgb_negative(self):
        with pytest.raises(InvalidColorValue):
            format_color("rgb(128, -32, 60)")

    def test_rgb_overbound(self):
        with pytest.raises(InvalidColorValue):
            format_color("rgb(128, 192, 999)")

    def test_rgba_negative_opacity(self):
        with pytest.raises(InvalidColorValue):
            format_color("rgb(128, 32, 60, -0.5)")

    def test_rgba_opacity_overbound(self):
        with pytest.raises(InvalidColorValue):
            format_color("rgba(128, 192, 0, 1.5)")

    def test_insufficient_iterable_length(self):
        with pytest.raises(InvalidColorValue):
            format_color([64, 128])

    def test_excessive_iterable_length(self):
        with pytest.raises(InvalidColorValue):
            format_color([128, 96, 48, 255, 255])

    def test_invalid_type(self):
        with pytest.raises(InvalidColorType):
            format_color(None)

        with pytest.raises(InvalidColorType):
            format_color(192)
