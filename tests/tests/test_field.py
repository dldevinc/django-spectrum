from collections import namedtuple

import pytest
from django.core.exceptions import ValidationError

from spectrum.color import Color
from spectrum.fields import ColorField, encode_color, parse_color


ModelMock = namedtuple("Model", ["color"])


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


class TestColorField:
    def test_from_db_value(self):
        field = ColorField()

        assert field.from_db_value(None) is None
        assert field.from_db_value("") is None

        color = field.from_db_value("#FFFF00")
        assert type(color) is Color
        assert color == "#FFFF00"

        # v0.1.0 compat
        color = field.from_db_value("#FFFF00:0.5")
        assert type(color) is Color
        assert color == "#FFFF0080"

    def test_get_prep_value(self):
        field = ColorField()

        assert field.get_prep_value(None) is ""
        assert field.get_prep_value("") is ""

        color = field.get_prep_value("#FFFF00")
        assert type(color) is str
        assert color == "#FFFF00"

        color = field.get_prep_value("rgb(255, 255, 0)")
        assert type(color) is str
        assert color == "#FFFF00"

        color = field.get_prep_value([255, 255, 0, 128])
        assert type(color) is str
        assert color == "#FFFF0080"

        color = field.get_prep_value(Color("#FFFF00"))
        assert type(color) is str
        assert color == "#FFFF00"

    def test_to_python(self):
        field = ColorField()

        assert field.to_python(None) is None
        assert field.to_python("") is None

        color = field.to_python("#FFFF00")
        assert type(color) is Color
        assert color == "#FFFF00"

        color = field.to_python("rgb(255, 255, 0)")
        assert type(color) is Color
        assert color == "#FFFF00"

        color = field.to_python([255, 255, 0, 128])
        assert type(color) is Color
        assert color == "#FFFF0080"

        color = field.to_python(Color("#FFFF00"))
        assert type(color) is Color
        assert color == "#FFFF00"

        with pytest.raises(ValidationError):
            field.to_python("mouse")

    def test_value_to_string(self):
        field = ColorField()
        field.set_attributes_from_name("color")

        assert field.value_to_string(ModelMock(color=None)) is ""
        assert field.value_to_string(ModelMock(color="")) is ""

        color = field.value_to_string(ModelMock(color="FFFF00"))
        assert type(color) is str
        assert color == "#FFFF00"

        color = field.value_to_string(ModelMock(color="rgb(255, 255, 0)"))
        assert type(color) is str
        assert color == "#FFFF00"

        color = field.value_to_string(ModelMock(color=[255, 255, 0, 128]))
        assert type(color) is str
        assert color == "#FFFF0080"

        color = field.value_to_string(ModelMock(color=Color("ffff0080")))
        assert type(color) is str
        assert color == "#FFFF0080"
