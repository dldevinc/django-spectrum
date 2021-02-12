# django-spectrum
Provides a colorpicker field for use in Django models

![django-spectrum](http://dl4.joxi.net/drive/2021/02/12/0025/1750/1701590/90/861af67e73.png)

[![PyPI](https://img.shields.io/pypi/v/django-spectrum.svg)](https://pypi.org/project/django-spectrum/)
[![Build Status](https://travis-ci.org/dldevinc/django-spectrum.svg?branch=master)](https://travis-ci.org/dldevinc/django-spectrum)

## Compatibility
* `django` >= 1.11
* `python` >= 3.5

## Quickstart
Install django-spectrum:
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

## Color instance
```
>>> from spectrum.color import Color

>>> rgb_color = Color('#FFFF00')
>>> print(rgb_color)
#FFFF00

>>> rgba_color = Color('#FFFF00', 0.5)
>>> print(rgba_color)
rgba(255,255,0,0.5)

>>> print(rgba_color.hex_code)
FFFF00

>>> print(rgba_color.hex)
#FFFF00

>>> print(rgba_color.opacity)
0.5
```

## Development and Testing
After cloning the Git repository, you should install this
in a virtualenv and set up for development:
```shell script
virtualenv .venv
source .venv/bin/activate
pip install -r ./requirements_dev.txt
pre-commit install
```
