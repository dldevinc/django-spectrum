(function($) {
    'use strict';

    function initWidgets(root = document.body) {
        root.querySelectorAll('.vColorField input[type="text"]').forEach(function(widget) {
            if (!widget.closest('.empty-form')) {
                $(widget).spectrum({
                    preferredFormat: "hex",
                    showInput: true,
                    showInitial: true,
                    showButtons: false
                });
            }
        });
    }

    $(document).ready(function() {
        initWidgets();
    }).on('formset:added', function(event, $row, prefix) {
        initWidgets($row.get(0));
    });

})(django.jQuery || jQuery);
