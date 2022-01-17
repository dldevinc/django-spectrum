from django.db import models
from django.utils.translation import gettext_lazy as _
from spectrum.fields import ColorField


class Example(models.Model):
    name = models.CharField(_('name'), max_length=128)
    color = ColorField(_('color'), default='#FFFF00', blank=True)

    def __str__(self):
        return self.name
