# django-spectrum
Provides an colorpicker field for use in Django models.

![django-spectrum](http://dl3.joxi.net/drive/2019/01/16/0025/1750/1701590/90/52ee08bef0.png)

## Compatibility
* `django` >= 2.0
* `python` >= 3.4

## Quickstart
Install django-spectrum:
```bash
pip install django-spectrum
```

Add it to your `INSTALLED_APPS` list:

```python
INSTALLED_APPS = (
    ...
    'spectrum',
)
```

Then add it to your models:
```python
from spectrum.fields import ColorField

class MyModel(models.Model):
    color = ColorField(_('color'), default='#FFFF00')
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

## License
Copyright (c) 2018 Mihail Mishakin Released under the MIT license (see LICENSE)
