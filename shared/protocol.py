from enum import Enum
import json

class CommandType(Enum):
    SCREENSHOT = 1
    LOCK_INPUT = 2
    SHOW_ALERT = 3
    CLOSE_BROWSER = 4
    EXECUTE_SCRIPT = 5

def create_command(cmd_type: CommandType, data: dict = None):
    return json.dumps({
        "type": cmd_type.name,
        "data": data or {}
    }).encode('utf-8')