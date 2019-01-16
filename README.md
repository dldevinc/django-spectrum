# django-spectrum
Provides an colorpicker field for use in Django models.

## Compatibility
* `django` >= 2.1.5
* `python` >= 3.6

## Quickstart
Install django-spectrum:
```bash
pip install django-spectrum
```

Then add it to your models:
```python
from spectrum.fields import ColorField

class MyModel(models.Model):
    color = ColorField(_('color'), default='#FFFF00')
```

![django-spectrum](http://dl3.joxi.net/drive/2019/01/16/0025/1750/1701590/90/52ee08bef0.png)

## License
Copyright (c) 2018 Mihail Mishakin Released under the MIT license (see LICENSE)
