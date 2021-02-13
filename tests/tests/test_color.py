import pytest

from spectrum.color import Color
from spectrum.exceptions import InvalidOpacity


class TestColorComparison:
    def setup_class(self):
        self.color = Color("#D2CEB080")

    def test_string(self):
        assert self.color == "#D2CEB080"

    def test_iterable(self):
        assert self.color == [210, 206, 176, 128]

    def test_color(self):
        assert self.color == Color([210, 206, 176, 128])

    def test_other_opacity(self):
        assert self.color != Color([210, 206, 176])

    def test_invalid_type(self):
        assert self.color != 192


class TestColor:
    def setup_class(self):
        self.color = Color("#d2ceb080")

    def test_hex(self):
        assert self.color.hex() == "#D2CEB0"

    def test_hex_setter(self):
        other_color = self.color.hex("ffff00")
        assert other_color == [255, 255, 0, 128]
        assert self.color is not other_color

    def test_hexa(self):
        assert self.color.hexa() == "#D2CEB080"

    def test_hexa_setter(self):
        other_color = self.color.hexa("aabbccff")
        assert other_color == [170, 187, 204, 255]
        assert self.color is not other_color

    def test_opaque(self):
        assert self.color.opaque is False
        assert Color("dadada").opaque is True

    def test_opacity(self):
        assert self.color.opacity() == 0.5

    def test_opacity_setter(self):
        other_color = self.color.opacity(0.1)
        assert other_color == [210, 206, 176, 26]
        assert self.color is not other_color

    def test_set_invalid_opacity(self):
        with pytest.raises(InvalidOpacity):
            self.color.opacity(2)

    def test_rgb(self):
        assert self.color.rgb() == "rgb(210, 206, 176)"

    def test_rgba(self):
        assert self.color.rgba() == "rgba(210, 206, 176, 0.5)"

    def test_hsl(self):
        assert self.color.hsl() == "hsl(53, 27.4%, 75.7%)"

    def test_hsla(self):
        assert self.color.hsla() == "hsla(53, 27.4%, 75.7%, 0.5)"


class TestColorString:
    def test_opaque(self):
        color = Color("#da60ec")
        assert str(color) == "#DA60EC"

    def test_transparent(self):
        color = Color("#da60ecde")
        assert str(color) == "rgba(218, 96, 236, 0.87)"

    def test_repr(self):
        assert repr(Color("#da60ec")) == "Color('#DA60EC')"
        assert repr(Color("#da60ecde")) == "Color('#DA60ECDE')"
