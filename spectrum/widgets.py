from django import forms


class ColorWidget(forms.HiddenInput):
    template_name = "spectrum/widget.html"

    @property
    def is_hidden(self):
        return False

    @property
    def media(self):
        return forms.Media(
            css={
                "screen": ["spectrum/css/monolith.min.css", "spectrum/css/widget.css"]
            },
            js=["spectrum/js/pickr.es5.min.js", "spectrum/js/widget.js"],
        )
