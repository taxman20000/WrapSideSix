# io/gui_binder.py

from dataclasses import fields, is_dataclass
from typing import Type, Any
from PySide6.QtWidgets import QWidget, QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit, QDateEdit, QDateTimeEdit, QLabel
from PySide6.QtCore import Qt, QDate, QDateTime
import json
from pathlib import Path
import copy

from ..widgets.line_edit_widget import WSLineButton

class WSGuiBinder:
    DEFAULT_VALUES = {
        QLineEdit: '',
        QTextEdit: '',
        QSpinBox: 0,
        QDoubleSpinBox: 0.0,
        QComboBox: '',
        QDateTimeEdit: QDateTime.currentDateTime(),
        QDateEdit: QDate.currentDate(),
        QLabel: '',

        WSLineButton: '',
    }

    def __init__(self, dataclass_type: Type[Any], widgets: dict[str, QWidget]):
        assert is_dataclass(dataclass_type), "Expected a dataclass type"
        self.dataclass_type = dataclass_type
        self.widgets = widgets
        self.instance = dataclass_type()
        self.original_data = copy.deepcopy(self.instance)

    def _get_get_method(self, widget):
        if isinstance(widget, QLineEdit): return lambda w: w.text()
        if isinstance(widget, QTextEdit): return lambda w: w.toPlainText()
        if isinstance(widget, QSpinBox): return lambda w: w.value()
        if isinstance(widget, QDoubleSpinBox): return lambda w: w.value()
        if isinstance(widget, QComboBox): return lambda w: w.currentText()
        if isinstance(widget, QDateTimeEdit): return lambda w: w.dateTime().toString(Qt.ISODate)
        if isinstance(widget, QDateEdit): return lambda w: w.date().toString(Qt.ISODate)
        if isinstance(widget, QLabel): return lambda w: w.text()
        raise TypeError(f"Unsupported widget type: {type(widget)}")

    def _get_set_method(self, widget):
        if isinstance(widget, QLineEdit): return lambda w, v: w.setText(v)
        if isinstance(widget, QTextEdit): return lambda w, v: w.setPlainText(v)
        if isinstance(widget, QSpinBox): return lambda w, v: w.setValue(int(v))
        if isinstance(widget, QDoubleSpinBox): return lambda w, v: w.setValue(float(v))
        if isinstance(widget, QComboBox): return lambda w, v: w.setCurrentText(v)
        if isinstance(widget, QDateTimeEdit):
            return lambda w, v: (
                w.setDateTime(QDateTime.fromString(v, Qt.ISODate)) if isinstance(v, str)
                else w.setDateTime(
                    v if isinstance(v, QDateTime)
                    else QDateTime(v, QDateTime.currentDateTime().time()) if isinstance(v, QDate)
                    else QDateTime()
                )
            )

        if isinstance(widget, QDateEdit):
            return lambda w, v: (
                w.setDate(QDate.fromString(v, Qt.ISODate)) if isinstance(v, str)
                else w.setDate(v if isinstance(v, QDate) else QDate(v))
            )

        if isinstance(widget, WSLineButton):
            return lambda w, v: w.setText(v)

        if isinstance(widget, QLabel): return lambda w, v: w.setText(v)
        raise TypeError(f"Unsupported widget type: {type(widget)}")

    def from_gui(self):
        for field in fields(self.instance):
            widget = self.widgets.get(field.name)
            if widget:
                method = self._get_get_method(widget)
                setattr(self.instance, field.name, method(widget))

    def to_gui(self):
        for field in fields(self.instance):
            widget = self.widgets.get(field.name)
            if widget:
                method = self._get_set_method(widget)
                method(widget, getattr(self.instance, field.name))

    def clear_gui(self):
        for field in fields(self.instance):
            widget = self.widgets.get(field.name)
            if widget:
                default = next(
                    (v for cls, v in self.DEFAULT_VALUES.items() if isinstance(widget, cls)),
                    None
                )

                if default is not None:
                    method = self._get_set_method(widget)
                    method(widget, default)

    def has_changed(self) -> bool:
        return self.instance != self.original_data

    def all_fields_filled(self, required_fields: list[str]) -> bool:
        for field_name in required_fields:
            widget = self.widgets.get(field_name)
            if not widget:
                continue

            if isinstance(widget, QLineEdit):
                if not widget.text().strip():
                    return False
            elif isinstance(widget, QTextEdit):
                if not widget.toPlainText().strip():
                    return False
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                if widget.value() == 0:
                    return False
            elif isinstance(widget, QComboBox):
                if widget.currentText().strip() == "":
                    return False
            elif isinstance(widget, QDateEdit):
                if not widget.date().isValid():
                    return False
            elif isinstance(widget, QDateTimeEdit):
                if not widget.dateTime().isValid():
                    return False

        return True


class JsonIO:
    def save(self, instance: Any, path: str | Path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(instance.__dict__, f, indent=2)

    def load(self, path: str | Path, cls: Type[Any]) -> Any:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)
