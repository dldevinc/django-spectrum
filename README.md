# django-spectrum
Provides a colorpicker field for Django

![image](https://user-images.githubusercontent.com/6928240/170836333-eb125dac-e617-44d3-9f3b-eefa8501b373.png)

[![PyPI](https://img.shields.io/pypi/v/django-spectrum.svg)](https://pypi.org/project/django-spectrum/)
[![Build Status](https://travis-ci.com/dldevinc/django-spectrum.svg?branch=master)](https://travis-ci.org/dldevinc/django-spectrum)

## Compatibility
* `python` >= 3.6
* `django` >= 1.11

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

Some examples of funcionality provided by the `Color` class:
```python
from spectrum.color import Color

c = Color("#FFDA0080")

>>> print(c.red)
255

>>> print(c.alpha)
128

>>> print(c.hex)
#FFDA00

>>> print(c.hexa)
#FFDA0080

>>> print(c.rgb)
rgb(255, 218, 0)

>>> print(c.rgba)
rgba(255, 218, 0, 0.5)

>>> print(c.opacity)
0.5

>>> print(c.as_tuple())
(255, 218, 0, 128)
```
