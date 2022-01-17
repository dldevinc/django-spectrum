import warnings


class InvalidColor(Exception):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "InvalidColor is deprecated in favor of InvalidColorError",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(*args, **kwargs)


class InvalidColorError(InvalidColor):
    pass


class InvalidColorType(InvalidColorError):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "InvalidColorType is deprecated in favor of InvalidColorTypeError",
            DeprecationWarning,
            stacklevel=2
        )
        super(InvalidColor, self).__init__(*args, **kwargs)


class InvalidColorTypeError(InvalidColorType):
    pass


class InvalidColorValue(InvalidColorError):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "InvalidColorValue is deprecated in favor of InvalidColorValueError",
            DeprecationWarning,
            stacklevel=2
        )
        super(InvalidColor, self).__init__(*args, **kwargs)


class InvalidColorValueError(InvalidColorValue):
    pass


class InvalidOpacity(InvalidColorError):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "InvalidOpacity is deprecated in favor of InvalidOpacityError",
            DeprecationWarning,
            stacklevel=2
        )
        super(InvalidColor, self).__init__(*args, **kwargs)


class InvalidOpacityError(InvalidOpacity):
    pass
