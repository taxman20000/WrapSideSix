# records_navigation_widget.py

from PySide6.QtWidgets import (QWidget, QMenu, QLabel, QVBoxLayout, QListWidget, QListWidgetItem,
                               QAbstractItemView, QPushButton, QHBoxLayout)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, Qt
import logging

# Logger Configuration
logger = logging.getLogger(__name__)


from ..icons import icons_mat_des
icons_mat_des.qInitResources()

class NavWidget(QWidget):
    # Define signals for navigation
    firstClicked = Signal()
    previousClicked = Signal()
    nextClicked = Signal()
    lastClicked = Signal()
    clearClicked = Signal()

    def __init__(self, parent=None, use_icons=False, clear_button=False, margins=(5, 5, 5, 5),
                 spacing=10, align='left'):
        super().__init__(parent)
        self.use_icons = use_icons
        self.clear_button = clear_button
        self.margins = margins
        self.spacing = spacing
        self.align = align

        self.firstButton = None
        self.previousButton = None
        self.nextButton = None
        self.lastButton = None
        self.clearButton = None
        self.record_info_label = None

        self.setup_ui()

    def setup_ui(self):
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(*self.margins)
        layout.setSpacing(self.spacing)

        # Initialize buttons with icons or text
        if self.use_icons:
            self.firstButton = QPushButton(QIcon(":/icons/mat_des/skip_previous_24dp.png"), "")
            self.previousButton = QPushButton(QIcon(":/icons/mat_des/fast_rewind_24dp.png"), "")
            self.nextButton = QPushButton(QIcon(":/icons/mat_des/fast_forward_24dp.png"), "")
            self.lastButton = QPushButton(QIcon(":/icons/mat_des/skip_next_24dp"), "")

        else:
            self.firstButton = QPushButton("<<")
            self.previousButton = QPushButton("<")
            self.nextButton = QPushButton(">")
            self.lastButton = QPushButton(">>")
        self.clearButton = QPushButton("X")

        # Set a fixed width for the buttons
        button_width = 30  # Adjust this value as needed to fit your design
        self.firstButton.setFixedWidth(button_width)
        self.previousButton.setFixedWidth(button_width)
        self.nextButton.setFixedWidth(button_width)
        self.lastButton.setFixedWidth(button_width)
        self.clearButton.setFixedWidth(button_width)

        # Initialize the record info label
        self.record_info_label = QLabel("0 of 0")

        # Add widgets to layout
        if self.align == 'right' or self.align == 'center':
            layout.addStretch()
        layout.addWidget(self.firstButton)
        layout.addWidget(self.previousButton)
        layout.addWidget(self.record_info_label)
        layout.addWidget(self.nextButton)
        layout.addWidget(self.lastButton)
        if self.clear_button is True:
            layout.addWidget(self.clearButton)
        if self.align == 'left' or self.align == "center":
            layout.addStretch()

        # Connect signals
        self.firstButton.clicked.connect(self.firstClicked.emit)
        self.previousButton.clicked.connect(self.previousClicked.emit)
        self.nextButton.clicked.connect(self.nextClicked.emit)
        self.lastButton.clicked.connect(self.lastClicked.emit)
        self.clearButton.clicked.connect(self.clearClicked.emit)

    def update_record_info(self, current, total):
        """Method to update the record info label."""
        self.record_info_label.setText(f"{current} of {total}")

