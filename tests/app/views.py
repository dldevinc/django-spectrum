from django.views.generic import TemplateView

from .models import Example


class IndexView(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Example.objects.order_by("-id")
        return context
