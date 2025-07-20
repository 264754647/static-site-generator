from enum import auto, Enum

class BlockType(Enum):
    paragraph = auto()
    heading = auto()
    code = auto()
    quote = auto()
    unordered_list = auto()
    ordered_list = auto()
