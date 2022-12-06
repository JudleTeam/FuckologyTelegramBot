from .commands import register_commands
from .main import register_main
from .pay import register_pay
from .admin import register_admin

register_functions = (
    register_commands,
    register_main,
    register_pay,
    register_admin
)
