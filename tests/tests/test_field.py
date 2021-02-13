from spectrum.color import Color
from spectrum.fields import encode_color, parse_color


class TestEncodeColor:
    def test_opaque(self):
        assert encode_color(Color("dadada")) == "#DADADA"

    def test_transparent(self):
        assert encode_color(Color("dadada80")) == "#DADADA80"


class TestParseColor:
    def test_opaque(self):
        assert parse_color("FFFF00:1") == Color("ffff00")

    def test_transparent(self):
        assert parse_color("FFFF00:0.25") == Color("ffff0040")

    def test_modern(self):
        assert parse_color("FFFF0040") == Color("FFFF0040")
