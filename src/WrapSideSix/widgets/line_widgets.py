# widgets/line_widgets.py

from PySide6.QtWidgets import (QFrame)
import logging

# Logger Configuration
logger = logging.getLogger(__name__)


class WSHorizontalLine(QFrame):
    """
    A custom widget representing a horizontal line separator.
    """
    def __init__(self, thickness=2, shadow_thickness=2):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setLineWidth(thickness)
        self.setMidLineWidth(shadow_thickness)


class WSVerticalLine(QFrame):
    """
    A custom widget representing a vertical line separator.
    """
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.VLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
