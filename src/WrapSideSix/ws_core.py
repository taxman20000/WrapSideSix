# ws_core.py

import enum
from dataclasses import dataclass

class WSSortOrder(enum.Enum):
    ASCENDING = "asc"
    DESCENDING = "desc"

    def label(self):
        return "Ascending (A → Z)" if self is WSSortOrder.ASCENDING else "Descending (Z → A)"


class WSActions(enum.Enum):
    SAVE = "save"
    OPEN = "open"
    DELETE = "delete"

class WSAlignment(enum.Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"

class WSEditOptions:
    CUT = "Cut"
    COPY = "Copy"
    PASTE = "Paste"
    CLEAR = "Clear"

@dataclass(frozen=True)
class WSNavDefaults:
    MARGINS: tuple[int, int, int, int] = (5, 5, 5, 5)
    SPACING: int = 10
    NAV_BUTTON_WIDTH: int = 30


