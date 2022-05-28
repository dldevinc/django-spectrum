(function($) {
    'use strict';

    function initWidgets(root) {
        root = (typeof root === "undefined") ? document.body : root;
        root.querySelectorAll(".vColorField").forEach(function(widget) {
            if (!widget.closest(".empty-form")) {
                var input = widget.querySelector("input");

                Pickr.create({
                    el: widget.querySelector(".pickr"),
                    theme: "monolith",
                    default: input.value,

                    components: {
                        preview: true,
                        opacity: true,
                        hue: true,

                        // Input / output Options
                        interaction: {
                            hex: true,
                            rgba: true,

                            input: true,
                            save: true,
                            clear: true
                        }
                    }
                }).on("init", function(instance) {
                    if (input.value) {
                        instance.setColor(input.value);
                    } else {
                        instance._clearColor();
                    }
                }).on("show", function(color, instance) {
                    instance.setColor(input.value || "000000", true);
                }).on('save', function(color, instance) {
                    if (color) {
                        input.value = color.toHEXA();
                    } else {
                        input.value = "";
                    }
                    instance.hide();
                })
            }
        });
    }

    $(document).ready(function() {
        initWidgets();
    }).on('formset:added', function(event, $row, prefix) {
        initWidgets($row.get(0));
    });

})(django.jQuery || jQuery);
