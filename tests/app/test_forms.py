from django import forms
from django.test import TestCase
from spectrum.forms import ColorField


class ColorForm(forms.Form):
    color = ColorField()


class ColorFieldTest(TestCase):
    def test_valid(self):
        form = ColorForm({
            'color_0': '#daBAcc',
            'color_1': '0.5'
        })
        self.assertTrue(form.is_valid())
        color = form.cleaned_data['color']
        self.assertEqual(color.hex, '#DABACC')
        self.assertEqual(color.opacity, 0.5)

    def test_invalid_opacity(self):
        form = ColorForm({
            'color_0': '#daBAcc',
            'color_1': '-0.5'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['color'].data[0].code, 'min_value')

        form = ColorForm({
            'color_0': '#daBAcc',
            'color_1': '2'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['color'].data[0].code, 'max_value')

        form = ColorForm({
            'color_0': '#daBAcc',
            'color_1': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['color'].data[0].code, 'incomplete')
