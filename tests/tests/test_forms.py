from django import forms

from spectrum.color import Color
from spectrum.forms import ColorField


class ColorForm(forms.Form):
    color = ColorField()


class TestColorField:
    def test_valid_initial(self):
        form = ColorForm({
            "color": "#daBAcc80",
        })

        assert form.is_valid() is True

        color = form.cleaned_data["color"]
        assert type(color) is Color

    def test_invalid_color(self):
        form = ColorForm({
            "color": "#AABBCCDDEE",
        })

        assert form.is_valid() is False
        assert form.errors["color"].data[0].code == "invalid"
