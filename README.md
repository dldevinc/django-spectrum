# django-spectrum
Provides a colorpicker field for Django

![django-spectrum](http://joxi.ru/l2ZPn43iRE3yDr.png)

[![PyPI](https://img.shields.io/pypi/v/django-spectrum.svg)](https://pypi.org/project/django-spectrum/)
[![Build Status](https://travis-ci.org/dldevinc/django-spectrum.svg?branch=master)](https://travis-ci.org/dldevinc/django-spectrum)

## Compatibility
* `django` >= 1.11
* `python` >= 3.5

## Quickstart
Install `django-spectrum`:
```bash
pip install django-spectrum
```

Add it to your `INSTALLED_APPS` list:
```python
INSTALLED_APPS = (
    ...
    "spectrum",
)
```

Then add it to your models:
```python
from django.db import models
from spectrum.fields import ColorField

class MyModel(models.Model):
    color = ColorField(_("color"), default="#FFFF00")
```

## Color class
The module defines a `Color` class which is used to represent the `ColorField` 
attribute on the model. The `Color` class can also be used standalone without 
any Django model.

Some examples of funcionality provided by the Color class:
```python
from spectrum.color import Color

c = Color("#FFDA0080")

>>> print(c.opaque)
False

>>> print(c.hex())
"#FFDA00"

>>> print(c.hexa())
"#FFDA0080"

>>> print(c.rgba())
"rgba(255, 218, 0, 0.5)"

>>> print(c.opacity())
0.5

>>> print(c.hsla())
"hsla(51, 100.0%, 50.0%, 0.5)"
```