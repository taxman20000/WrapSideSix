# io/ws_io.py

from contextlib import contextmanager
from PySide6.QtWidgets import (QComboBox, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox,
                               QDateTimeEdit, QDateEdit, QLabel)
from PySide6.QtCore import QDate, QDateTime
import logging

# Logger Configuration
logger = logging.getLogger(__name__)

from ..widgets.line_edit_widget import WSLineButton


class WSGuiIO:
    # Define a lookup dictionary based on widget types.
    WIDGET_LOOKUP = {
        # Standard
        QLineEdit: {'get': 'text', 'set': 'setText'},
        QTextEdit: {'get': 'toPlainText', 'set': 'setPlainText'},
        QSpinBox: {'get': 'value', 'set': 'setValue'},
        QDoubleSpinBox: {'get': 'value', 'set': 'setValue'},
        QComboBox: {'get': 'currentText', 'set': 'setCurrentText'},
        # QCheckBox: {'get': 'isChecked', 'set': 'setChecked'},
        QDateTimeEdit: {'get': 'dateTime', 'set': 'setDateTime'},
        QDateEdit: {'get': 'date', 'set': 'setDate'},
        QLabel: {'get': 'text', 'set': 'setText'},

        # Custom
        WSLineButton: {'get': 'get_list', 'set': 'set_list'},
        # WSLineList: {'get': 'get_list', 'set': 'set_list'},
        # WSMarkdownWidget: {'get': 'get_markdown_data', 'set': 'set_markdown_data'},
        # WSLineListEdit: {'get': 'getList', 'set': 'setList'},
        # WSRichEditor: {'get': 'get_text_content', 'set': 'set_text'},
    }

    DEFAULT_VALUES = {
        QLineEdit: '',
        QTextEdit: '',
        QSpinBox: 0,
        QDoubleSpinBox: 0.0,
        QComboBox: None,
        # QListWidget: [],
        # QCheckBox: False,
        # QRadioButton: None,
        QDateTimeEdit: QDateTime.currentDateTime(),  # Set to current date and time
        QDateEdit: QDate.currentDate(),  # Set to current date
        QLabel: '',

        # Custom
        WSLineButton: '',


    }

    def __init__(self, widget_mapping, current_settings):
        self.widget_mapping = widget_mapping
        self.current_settings = current_settings

    def _get_widget_methods(self, widget):
        for widget_type, methods in self.WIDGET_LOOKUP.items():
            # print(WSRadioButtonBar.__module__)
            if isinstance(widget, widget_type):
                return methods
        raise ValueError(f"No methods found for widget type {type(widget)}")

    def _get_nested_value(self, dictionary, keys):
        """Recursively get a nested value from a dictionary."""
        if "." in keys:
            key, rest = keys.split(".", 1)
            return self._get_nested_value(dictionary.get(key, {}), rest)
        return dictionary.get(keys)

    def _set_nested_value(self, dictionary, keys, value):
        """Recursively set a nested value in a dictionary."""
        if "." in keys:
            key, rest = keys.split(".", 1)
            if key not in dictionary:
                dictionary[key] = {}
            self._set_nested_value(dictionary[key], rest, value)
        else:
            dictionary[keys] = value

    # def set_gui(self):
    #     for key, widget in self.widget_mapping.items():
    #         methods = self._get_widget_methods(widget)
    #         value = self._get_nested_value(self.current_settings, key)
    #         if value is not None:  # Ensure the value exists in the settings
    #             getattr(widget, methods['set'])(value)

    def set_gui(self):
        for key, widget in self.widget_mapping.items():
            methods = self._get_widget_methods(widget)
            value = self._get_nested_value(self.current_settings, key)
            if value is None:
                default_value = self.DEFAULT_VALUES.get(type(widget))  # Get default value for the widget
                getattr(widget, methods['set'])(default_value)  # Set to default
            else:
                getattr(widget, methods['set'])(value)

    def get_gui(self):
        updated_settings = self.current_settings.copy()  # Start with a copy of the current settings
        # print(f"Updated settings {updated_settings}")
        for key, widget in self.widget_mapping.items():
            # print(f"key: {key}")
            methods = self._get_widget_methods(widget)
            value = getattr(widget, methods['get'])()
            # print(f"value: {value}")
            self._set_nested_value(updated_settings, key, value)
        return updated_settings

    def clear_all_widgets(self):
        for widget in self.widget_mapping.values():
            methods = self._get_widget_methods(widget)
            default_value = self.DEFAULT_VALUES.get(type(widget))
            if default_value is not None:  # Ensure a default value exists for the widget type
                getattr(widget, methods['set'])(default_value)


    def all_widgets_have_values(self, ignore_widgets=None):
        """
        Check if all the widgets in the widget mapping have values.

        This method will check each widget in the `widget_mapping` to determine if they have
        values set. If any widget has a value that matches the default blank value (as defined
        in `DEFAULT_VALUES`), the method will return False. Otherwise, it will return True.

        Args:
            ignore_widgets (list of str, optional): List of widget names (keys from `widget_mapping`)
                that should be ignored during the check. These widgets are considered optional
                and their values won't affect the outcome of this method. Defaults to None, meaning
                all widgets are checked.

        Returns:
            bool: True if all non-ignored widgets have values, False otherwise.

        Example:
            If the widget_mapping is:
            {
                "full_name": <Widget1>,
                "nickname": <Widget2>,
                "persona": <Widget3>
            }

            all_widgets_have_values(ignore_widgets=["nickname"])

            This will check values for "full_name" and "persona", but will not check "nickname".
        """

        if ignore_widgets is None:
            ignore_widgets = []

        for widget_name, widget in self.widget_mapping.items():
            # Skip if this widget is in the ignore list
            if widget_name in ignore_widgets:
                continue

            methods = self._get_widget_methods(widget)
            current_value = getattr(widget, methods['get'])()
            blank_value = self.DEFAULT_VALUES.get(type(widget))

            if current_value == blank_value:
                return False

        return True

    def select_widgets_have_values(self, selected_widgets):
        """
        Check if selected widgets in the widget mapping have values.

        This method will check each widget in `selected_widgets` to determine if they have
        values set. If any widget has a value that matches the default blank value (as defined
        in `DEFAULT_VALUES`), the method will return False. Otherwise, it will return True.

        Args:
            selected_widgets (list of str): List of widget names (keys from `widget_mapping`)
                that should be checked during this method.

        Returns:
            bool: True if all selected widgets have values, False otherwise.

        Example:
            If the widget_mapping is:
            {
                "full_name": <Widget1>,
                "nickname": <Widget2>,
                "persona": <Widget3>
            }

            select_widgets_have_values(selected_widgets=["full_name", "persona"])

            This will only check values for "full_name" and "persona".
        """

        for widget_name in selected_widgets:
            widget = self.widget_mapping.get(widget_name)
            if widget is None:
                # print(widget_name)
                return False  # The widget is not in the mapping

            methods = self._get_widget_methods(widget)
            current_value = getattr(widget, methods['get'])()
            blank_value = self.DEFAULT_VALUES.get(type(widget))

            if current_value == blank_value:
                return False

        return True


class WSDbGuiIO:
    def __init__(self, session_manager, model_instance, widget_mapping):
        self.session_manager = session_manager
        self.model_instance = model_instance
        self.widget_mapping = widget_mapping

    def _get_widget_methods(self, widget):
        for widget_type, methods in WSGuiIO.WIDGET_LOOKUP.items():
            if isinstance(widget, widget_type):
                return methods
        raise ValueError(f"No methods found for widget type {type(widget)}")

    @contextmanager
    def managed_session(self):
        """
        Provide a transactional scope around a series of operations.
        """
        session = self.session_manager.create_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def set_gui(self):
        """
        Populate GUI widgets from the database model.
        """
        with self.managed_session() as session:
            model = session.query(type(self.model_instance)).get(self.model_instance.id)
            for attr, widget in self.widget_mapping.items():
                methods = self._get_widget_methods(widget)
                value = getattr(model, attr, None)
                if value is not None:
                    getattr(widget, methods['set'])(value)

    def get_gui(self):
        """
        Update the database model from GUI widgets and save changes to the database.
        """
        with self.managed_session() as session:
            model = session.query(type(self.model_instance)).get(self.model_instance.id)
            for attr, widget in self.widget_mapping.items():
                methods = self._get_widget_methods(widget)
                setattr(model, attr, getattr(widget, methods['get'])())

    def clear_all_widgets(self):
        """
        Reset all widgets to their default values.
        """
        for widget in self.widget_mapping.values():
            methods = self._get_widget_methods(widget)
            default_value = WSGuiIO.DEFAULT_VALUES.get(type(widget))
            if default_value is not None:
                getattr(widget, methods['set'])(default_value)

    def all_widgets_have_values(self):
        """
        Ensure all widgets have meaningful values.
        """
        for widget in self.widget_mapping.values():
            methods = self._get_widget_methods(widget)
            current_value = getattr(widget, methods['get'])()
            default_value = WSGuiIO.DEFAULT_VALUES.get(type(widget))
            if current_value == default_value:
                return False
        return True
