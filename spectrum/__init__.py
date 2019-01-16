"""
    =====================
      Поле выбора цвета
    =====================

    Установка
    ---------
    Добавить "paper_color" в INSTALLED_APPS:
        INSTALLED_APPS = [
            ...
            'paper_color',
        ]

    Примеры
    -------
    # models.py
        color = ColorField(_('color'), blank=True, default='#F00')
        color = ColorField(_('color'), blank=True, default='#FF0000')
        color = ColorField(_('color'), blank=True, default='#FF0000:0.75')

    # shell
        > instance.color.hex
        '#FF0000'

        > instance.color.opacity
        Decimal('0.75')

        > instance.color.rgb
        'rgb(255, 0, 0)'

        > instance.color.rgba
        'rgb(255, 0, 0, 0.75)'
"""
