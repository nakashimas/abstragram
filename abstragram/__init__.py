# __init__.py

try:
    from . import colorpicker
    from . import composition
    from .core import *
except Exception as _:
    import colorpicker
    import composition
    from core import *
