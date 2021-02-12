from django import forms
from spectrum.forms import ColorField


class ColorForm(forms.Form):
    color = ColorField()


class ColorFieldTest:
    def test_valid(self):
        form = ColorForm({
            'color_0': '#daBAcc',
            'color_1': '0.5'
        })

        assert form.is_valid() is True

        color = form.cleaned_data['color']
        assert color.hex == '#DABACC'
        assert color.opacity == 0.5

    def test_invalid_color(self):
        form = ColorForm({
            'color_0': '#AABBCCDD',
            'color_1': '1'
        })

        assert form.is_valid() is False
        assert form.errors['color'].data[0].code == 'invalid_color'

        form = ColorForm({
            'color_0': '#FF',
            'color_1': '1'
        })
        assert form.is_valid() is False
        assert form.errors['color'].data[0].code == 'invalid_color'

        form = ColorForm({
            'color_0': 'yellow',
            'color_1': '1'
        })
        assert form.is_valid() is False
        assert form.errors['color'].data[0].code == 'invalid_color'

    def test_invalid_opacity(self):
        form = ColorForm({
            'color_0': '#daBAcc',
            'color_1': '-0.5'
        })
        assert form.is_valid() is False
        assert form.errors['color'].data[0].code == 'min_value'

        form = ColorForm({
            'color_0': '#daBAcc',
            'color_1': '2'
        })
        assert form.is_valid() is False
        assert form.errors['color'].data[0].code == 'max_value'
