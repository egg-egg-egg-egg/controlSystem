from enum import Enum
import json

class CommandType(Enum):
    SCREENSHOT = 1
    LOCK_INPUT = 2
    SHOW_ALERT = 3
    CLOSE_BROWSER = 4
    EXECUTE_SCRIPT = 5

def create_command(cmd_type: CommandType, data: dict = None):
    if "data" in data and isinstance(data["data"], bytes):
        data["data"] = list(data["data"])  # 将二进制数据转换为列表
    return json.dumps({
        "type": cmd_type.name,
        "data": data or {}
    }).encode('utf-8')