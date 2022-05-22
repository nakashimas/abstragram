# __init__.py

try:
    from .bot_taskmanager import *
    from .bot_timetable import *
except Exception:
    from bot_taskmanager import *
    from bot_timetable import *
