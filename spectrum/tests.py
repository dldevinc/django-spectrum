from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from .color import Color, DEFAULT_COLOR
from .fields import ColorField
from . import forms
from . import widgets


class TestColorField(TestCase):
    def test_default(self):
        field = ColorField('verbose_name')
        self.assertEqual(field.default, Color())

        field = ColorField('verbose_name', default='#123')
        self.assertEqual(field.default, Color('#112233'))

        field = ColorField('verbose_name', default='A00')
        self.assertEqual(field.default, Color('#AA0000'))

    def test_deconstruct(self):
        field = ColorField('verbose_name')
        name, path, args, kwargs = field.deconstruct()
        self.assertNotIn('default', kwargs)

        field = ColorField('verbose_name', default='FFF')
        name, path, args, kwargs = field.deconstruct()
        self.assertNotIn('default', kwargs)

        field = ColorField('verbose_name', default='FFFFFF')
        name, path, args, kwargs = field.deconstruct()
        self.assertNotIn('default', kwargs)

        field = ColorField('verbose_name', default=Color())
        name, path, args, kwargs = field.deconstruct()
        self.assertNotIn('default', kwargs)

        field = ColorField('verbose_name', default='#DAC')
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(kwargs['default'], Color('#DDAACC'))

    def test_to_python(self):
        field = ColorField('verbose_name')
        self.assertEqual(field.to_python(None), None)
        self.assertEqual(field.to_python('FFF'), Color('#FFFFFF'))
        self.assertEqual(field.to_python(Color('FFF')), Color('#FFFFFF'))
        self.assertRaises(ValidationError, field.to_python, '')
        self.assertRaises(ValidationError, field.to_python, '#FF')

    def test_formfield(self):
        field = ColorField('verbose_name')
        formfield = field.formfield()
        self.assertIsInstance(formfield, forms.ColorField)
        self.assertIsInstance(formfield.widget, widgets.ColorWidget)
