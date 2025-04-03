# widgets/line_edit_widget.py

from PySide6.QtWidgets import (QLineEdit, QMenu, QPushButton, QMessageBox, QFileDialog)
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QContextMenuEvent
from pathlib import Path

import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from ..icons import icons_resource
icons_resource.qInitResources()


class WSLineList(QLineEdit):
    def __init__(self, initial_value=None):
        super().__init__()
        if initial_value is None:
            initial_value = []
        self.setText(self._list_to_string(initial_value))

        self.setReadOnly(True)

    def _list_to_string(self, list_data):
        """
        Convert a list of strings to a single comma-separated string. Handles cases where list_data is not iterable.

        Args:
            list_data (list): The list of strings to convert.

        Returns:
            str: The comma-separated string. Returns an empty string if list_data is not iterable.
        """
        # Check if list_data is indeed iterable
        if isinstance(list_data, (list, tuple, set)):
            # Ensure all elements are strings to avoid another type of TypeError
            return ', '.join(str(item) for item in list_data)
        elif isinstance(list_data, str):
            # If it's already a string, return it as is
            return list_data
        else:
            # Handle the case where list_data is not iterable
            return ''

    def _string_to_list(self, string_data):
        """
        Convert a comma-separated string to a list of strings.

        Args:
            string_data (str): The comma-separated string to convert.

        Returns:
            list: The list of strings.
        """
        return [item.strip() for item in string_data.split(',') if item.strip()]

    def get_list(self):
        """
        Retrieve the list of strings from the input field.

        Returns:
            list: The list of strings.
        """
        return self._string_to_list(self.text())

    def set_list(self, list_data):
        """
        Set the list of strings in the input field.

        Args:
            list_data (list): The list of strings to set.
        """
        self.setText(self._list_to_string(list_data))


class WSLineButton(WSLineList):
    value_changed = Signal(str)

    def __init__(self, parent=None, button_text='...', button_action=None, button_icon=None, use_custom_menu=False):
        super().__init__(parent)
        self.button = QPushButton(button_text, self)
        self.connected = False

        if button_icon:
            self.button.setIcon(QIcon(button_icon))
            self.button.setText("")  # Optionally clear text if you don't need it.
        else:
            self.button.setText(button_text)

        self.button.setFixedSize(QSize(20, self.sizeHint().height()))
        self.button.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Prevent button from taking focus

        # self.button.clicked.connect(button_action or self.default_action)

        self._button_action = button_action
        self.set_button_action(self._button_action)

        self.setContentsMargins(0, 0, self.button.width(), 0)
        self.textChanged.connect(self.adjust_button_position)
        self.resizeEvent = self.adjust_button_position

        self.use_custom_menu = use_custom_menu
        if not self.use_custom_menu:
            # If using default menu, no need to override anything
            return

    def contextMenuEvent(self, event: QContextMenuEvent):
        if not self.use_custom_menu:
            super().contextMenuEvent(event)  # Use the default menu
            return

        # Custom menu logic
        menu = QMenu(self)
        # menu.addAction("Cut", self.cut)
        # menu.addAction("Copy", self.copy)
        # menu.addAction("Paste", self.paste)
        menu.addAction("Clear", self.clear)  # Explicitly adding Clear

        # Custom action
        # custom_action = QAction("Custom Action", self)
        # custom_action.triggered.connect(self.custom_action_triggered)
        # menu.addAction(custom_action)

        menu.exec(event.globalPos())

    def custom_action_triggered(self):
        self.setText("Custom action triggered!")


    def adjust_button_position(self, *args):
        self.button.move(self.width() - self.button.width(), 0)

    def set_button_action(self, action):
        """
        Allows setting (or replacing) the button click action at any time.
        If action is None, we'll connect to the default_action method.
        """
        # First, disconnect the existing action, if any
        try:
            if self.connected:
                self.button.clicked.disconnect()
        except TypeError:
            logger.debug("LineButton not connected, no impact, ignore")

        if action is None:
            self.button.clicked.connect(self.default_action)
            self.connected = True
        else:
            self.button.clicked.connect(action)

    def default_action(self):
        QMessageBox.information(self, "Button Clicked", "No action defined for this button.")

    def get_path(self) -> Path:
        """Returns the contents of the field as a Path object (expanded)."""
        return Path(self.text().strip()).expanduser()


class WSLineButtonDirectory(WSLineButton):
    def __init__(self, parent=None, button_icon=":/icons/mat_des/folder_24dp.png", label="Select Directory", def_dir=None):
        super().__init__(parent, button_icon=button_icon, button_action=self.select_directory)
        self.dialog_label = label
        self.def_dir = Path(def_dir).expanduser() if def_dir else None

    def select_directory(self):
        # Priority: field value > def_dir > home dir
        current_path = Path(self.text().strip()).expanduser()
        if current_path.is_dir():
            start_dir = str(current_path)
        elif self.def_dir and self.def_dir.is_dir():
            start_dir = str(self.def_dir)
        else:
            start_dir = str(Path.home())

        folder_path = QFileDialog.getExistingDirectory(
            self,
            self.dialog_label,
            start_dir
        )

        if folder_path:
            self.setText(folder_path)
            self.value_changed.emit(folder_path)

    def is_valid(self) -> bool:
        """Returns True if the path is a valid directory."""
        return self.get_path().is_dir()


class WSLineButtonFile(WSLineButton):
    def __init__(
        self,
        parent=None,
        button_icon=":/icons/mat_des/file_open_24dp.png",
        label="Select File",
        def_path=None,
        file_filter="All Files (*)"
    ):
        super().__init__(parent, button_icon=button_icon, button_action=self.select_file)
        self.dialog_label = label
        self.def_path = Path(def_path).expanduser() if def_path else None
        self.file_filter = file_filter

    def select_file(self):
        # Priority: field value > def_path > home dir
        current_path = Path(self.text().strip()).expanduser()
        if current_path.is_file():
            start_path = str(current_path.parent)
        elif self.def_path and self.def_path.is_file():
            start_path = str(self.def_path.parent)
        elif self.def_path and self.def_path.is_dir():
            start_path = str(self.def_path)
        else:
            start_path = str(Path.home())

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.dialog_label,
            start_path,
            self.file_filter
        )

        if file_path:
            self.setText(file_path)
            self.value_changed.emit(file_path)

    def is_valid(self) -> bool:
        """Returns True if the path is a valid file."""
        return self.get_path().is_file()


class WSLineButtonList(WSLineButton):
    pass

# class WSComboList(WSLineButton):
#     selectionChanged = Signal(list)
#
#     def __init__(self, parent=None, dialog_title="Select Items",
#                  dialog_multi_select=True,
#                  require_selection=False,
#                  fetch_items=None):
#         super().__init__(parent, button_text="...", button_action=self.open_selection_dialog)
#
#         self.all_items = []
#         self.dialog_title = dialog_title
#         self.dialog_multi_select = dialog_multi_select
#         self.require_selection = require_selection
#         self.fetch_items = fetch_items
#
#     def open_selection_dialog(self):
#         if self.fetch_items:
#             self.all_items = self.fetch_items()
#
#         dialog = ListSelectionDialog(self.all_items,
#                                      self.get_list(),
#                                      title=self.dialog_title,
#                                      multi_select=self.dialog_multi_select)
#         dialog.selected_items_signal.connect(self.set_list)
#         dialog.exec()
#
#     def add_items(self, items):
#         self.all_items.extend(items)
#
#     def clear(self):
#         self.set_list([])
#         self.selectionChanged.emit([])
#
#     def set_dialog_title(self, title):
#         self.dialog_title = title
#
#     def set_multi_select(self, multi_select):
#         self.dialog_multi_select = multi_select
#
#     def set_fetch_items(self, fetch_items):
#         self.fetch_items = fetch_items
#
#     def validate_selection(self, selected_items):
#         if self.require_selection and not selected_items:
#             return False
#         return True
#
#     def set_list(self, list_data):
#         if self.validate_selection(list_data):
#             super().set_list(list_data)
#             self.selectionChanged.emit(list_data)
#         else:
#             QMessageBox.warning(self, "Validation Error", "At least one item must be selected.")

