import django

if django.VERSION >= (2, 0):
    from django.urls import re_path as url
else:
    from django.conf.urls import url

from .views import IndexView

app_name = "app"
urlpatterns = [
    url(r"", IndexView.as_view()),
]
