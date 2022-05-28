import copy
import pickle
from decimal import Decimal

from spectrum.color import Color


class TestColor:
    def setup_class(self):
        self.color = Color("#d2ceb080")

    def test_red(self):
        assert self.color.red == 210

    def test_green(self):
        assert self.color.green == 206

    def test_blue(self):
        assert self.color.blue == 176

    def test_alpha(self):
        assert self.color.alpha == 128

    def test_opacity(self):
        assert self.color.opacity == Decimal("0.5")

    def test_opaque(self):
        assert self.color.opaque is False
        assert Color("dadada").opaque is True

    def test_transparent(self):
        assert self.color.transparent is False
        assert Color("dadada00").transparent is True

    def test_hex(self):
        assert self.color.hex == "#D2CEB0"

    def test_hexa(self):
        assert self.color.hexa == "#D2CEB080"

    def test_rgb(self):
        assert self.color.rgb == "rgb(210, 206, 176)"

    def test_rgba(self):
        assert self.color.rgba == "rgba(210, 206, 176, 0.5)"

    def test_hsl(self):
        assert self.color.hsl == "hsl(53, 27%, 76%)"

    def test_hsla(self):
        assert self.color.hsla == "hsla(53, 27%, 76%, 0.5)"

    def test_as_tuple(self):
        assert self.color.as_tuple() == (210, 206, 176, 128)


class TestSerialization:
    def test_str_opaque(self):
        color = Color("#da60ec")
        assert str(color) == "#DA60EC"

    def test_str_transparent(self):
        color = Color("#da60ecde")
        assert str(color) == "rgba(218, 96, 236, 0.87)"

    def test_repr_opaque(self):
        color = Color("#da60ec")
        assert repr(color) == "Color('#DA60EC')"

    def test_repr_transparent(self):
        color = Color("#da60ecde")
        assert repr(color) == "Color('#DA60ECDE')"

    def test_pickle(self):
        color = Color("rgba(218, 96, 236, 0.87)")
        unpickled = pickle.loads(pickle.dumps(color))
        assert color == unpickled


class TestCopy:
    def setup_class(self):
        self.color = Color("#D2CEB080")

    def test_copy(self):
        clone = copy.copy(self.color)
        clone._rgba[1] = 220
        assert self.color._rgba[1] == 206


class TestComparison:
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
