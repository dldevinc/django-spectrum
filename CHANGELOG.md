# Change Log

## [0.5.3](https://github.com/dldevinc/django-spectrum/tree/v0.5.3) - 2023-08-18

### Bug Fixes

-   Issue with `collectstatic` command failing due to missing source map.

### Features

-   Test against Django 4.2.

## [0.5.2](https://github.com/dldevinc/django-spectrum/tree/v0.5.2) - 2023-02-24

### Features

-   Add Wagtail compatibility.

## [0.5.1](https://github.com/dldevinc/django-spectrum/tree/v0.5.1) - 2023-01-09

### Features

-   Add Python 3.11 support (no code changes were needed, but now we test this release).

## [0.5.0](https://github.com/dldevinc/django-spectrum/tree/v0.5.0) - 2022-08-15

### Features

-   Added support for Django 4.1.

## [0.4.1](https://github.com/dldevinc/django-spectrum/tree/v0.4.1) - 2022-06-08

### Bug Fixes

-   Fixed an issue where an `AttributeError` is raised for non-`Color` default values.

## [0.4.0](https://github.com/dldevinc/django-spectrum/tree/v0.4.0) - 2022-05-28

### ⚠ BREAKING CHANGES

-   The `Color` instances now immutable and hashable.
-   All methods of `Color` class was converted to properies.
    So for example instead of `Color.rgb()` you should use `Color.rgb`.
-   `InvalidOpacityError` exception was removed.
-   Deprecated exceptions was removed.

### Features

-   `Color` class now supports new RGBA notation: `rgba(R G B / A%)`.
-   Added some new properties to the `Color` class:
    `red`, `green`, `blue`, and `transparent`.
-   `pickr` library was upgraded from version 1.8.0 to 1.8.2.

## [0.3.0](https://github.com/dldevinc/django-spectrum/tree/v0.3.0) - 2022-01-17

-   Drop support for Python 3.5
-   Add support for Python 3.10, Django 3.2 and Django 4.0
-   Added `Error` suffix to all exceptions.

## [0.2.1](https://github.com/dldevinc/django-spectrum/tree/v0.2.1) - 2021-02-17

-   Fix missing templates

## [0.2.0](https://github.com/dldevinc/django-spectrum/tree/v0.2.0) - 2021-02-13

-   `Color` class has been changed in a **backward incompatible** way
-   Drop Python 3.4 support
-   Migrate to [pickr](https://github.com/Simonwep/pickr)
