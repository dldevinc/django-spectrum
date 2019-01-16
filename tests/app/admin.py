from django.contrib import admin
from .models import Example


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__', 'color')
    list_display_links = ('__str__', )
