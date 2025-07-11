import enum

class RoleEnum(enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"
    tool = "tool"