# toolbar_icon.py

from PySide6.QtWidgets import QToolBar, QToolButton, QMenu
from PySide6.QtGui import QAction, QIcon
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

class DropdownItem:
    def __init__(self, label, callback, icon=None):
        self.label = label
        self.callback = callback
        self.icon = QIcon(icon) if isinstance(icon, str) else icon

    def to_action(self, parent):
        action = QAction(self.icon, self.label, parent) if self.icon else QAction(self.label, parent)
        action.triggered.connect(self.callback)
        return action


class WSToolbarIcon(QToolBar):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)
        self.actions = {}
        self.dropdowns = {}

    def add_action_to_toolbar(self, name, text, tooltip, slot, icon=None):
        """
        Add a single action to the toolbar.
        """
        action = QAction(QIcon(icon), text, self) if icon else QAction(text, self)
        action.setToolTip(tooltip)
        action.triggered.connect(slot)
        self.addAction(action)
        self.actions[name] = action

    def add_actions_to_toolbar(self, actions):
        """
        Add multiple actions to the toolbar.

        :param actions: List of tuples in the format (name, text, tooltip, slot, icon).
        """
        for action_def in actions:
            self.add_action_to_toolbar(*action_def)

    def add_dropdown_menu_to_toolbar(self, name, icon, items):
        """
        Create a dropdown menu button with an icon and optional icons in dropdown items.
        """
        if name in self.dropdowns:
            logger.info(f"Dropdown '{name}' already exists. Skipping.")
            return

        tool_button = QToolButton(self)
        tool_button.setIcon(QIcon(icon))
        tool_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        # menu = QMenu(self)
        # for item in items:
        #     action = item.to_action(self)
        #     menu.addAction(action)

        menu = QMenu(self)
        for item in items:
            if item == "separator":
                menu.addSeparator()
                continue  # Skip the rest of this loop iteration
            # Otherwise, assume it's a DropdownItem
            action = item.to_action(self)
            menu.addAction(action)

        tool_button.setMenu(menu)

        # ⬇️ Notice we capture the QAction returned by addWidget
        action_for_dropdown = self.addWidget(tool_button)

        # Store both the QToolButton and its associated QAction.
        self.dropdowns[name] = (tool_button, action_for_dropdown)

    def insert_dropdown_menu(self, position, name, icon, items):
        """
        Insert a dropdown menu (QToolButton) at a specific position in the toolbar.
        If the position is out of range, the dropdown is appended at the end.
        """
        if name in self.dropdowns:
            logger.info(f"Dropdown '{name}' already exists. Skipping.")
            return

        tool_button = QToolButton(self)
        tool_button.setIcon(QIcon(icon))
        tool_button.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        menu = QMenu(self)
        for item in items:
            action = item.to_action(self)
            menu.addAction(action)

        tool_button.setMenu(menu)

        actions_list = list(self.actions.values())
        if 0 <= position < len(actions_list):
            reference_action = actions_list[position]
        else:
            reference_action = None

        # ⬇️ This returns the QAction referencing the new widget
        action_for_dropdown = self.insertWidget(reference_action, tool_button)
        self.dropdowns[name] = (tool_button, action_for_dropdown)

    def update_dropdown_menu(self, name, icon, dropdown_definitions):
        """
        Update a dropdown menu in the toolbar.
        """
        # If it exists, remove it first
        if name in self.dropdowns:
            tool_button, dropdown_action = self.dropdowns.pop(name)
            self.removeAction(dropdown_action)

        # Now add the updated version
        self.add_dropdown_menu_to_toolbar(name, icon, dropdown_definitions)

    def add_dropdown_menus(self, dropdown_definitions):
        for name, icon, items in dropdown_definitions:
            self.add_dropdown_menu_to_toolbar(name, icon, items)

    def remove_action(self, name):
        if name in self.actions:
            action = self.actions.pop(name)
            self.removeAction(action)

    # 🚀 New method to insert an action at a specific position
    def insert_action(self, position, name, text, tooltip, slot, icon=None):
        action = QAction(QIcon(icon), text, self) if icon else QAction(text, self)
        action.setToolTip(tooltip)
        action.triggered.connect(slot)

        actions_list = list(self.actions.values())  # current actions in the order they were added
        if 0 <= position < len(actions_list):
            reference_action = actions_list[position]
        else:
            # If position is out of range, we can append at the end
            reference_action = None

        self.insertAction(reference_action, action)
        self.actions[name] = action

    # Show and Hide methods
    def hide_action_by_name(self, name):
        """
        Hide the action and its associated widget (if available) by name.
        """
        if name in self.actions:
            self.actions[name].setVisible(False)
            widget = self.widgetForAction(self.actions[name])
            if widget:
                widget.hide()
        else:
            logger.warning(f"Action '{name}' not found.")

    def show_action_by_name(self, name):
        """
        Show the action and its associated widget (if available) by name.
        """
        if name in self.actions:
            self.actions[name].setVisible(True)
            widget = self.widgetForAction(self.actions[name])
            if widget:
                widget.show()
        else:
            logger.warning(f"Action '{name}' not found.")

    def hide_dropdown_by_name(self, name):
        """
        Hide a dropdown (QToolButton and its action) by name.
        """
        if name in self.dropdowns:
            tool_button, action = self.dropdowns[name]
            action.setVisible(False)
            tool_button.hide()
        else:
            logger.warning("Dropdown '{name}' not found.")

    def show_dropdown_by_name(self, name):
        """
        Show a dropdown (QToolButton and its action) by name.
        """
        if name in self.dropdowns:
            tool_button, action = self.dropdowns[name]
            action.setVisible(True)
            tool_button.show()
        else:
            logger.warning(f"Dropdown '{name}' not found.")

    # 🚀 New method to clear the entire toolbar
    def clear_toolbar(self):
        self.clear()
        self.actions.clear()
        self.dropdowns.clear()
