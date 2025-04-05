# layouts/grid_layout.py

from PySide6.QtWidgets import (QLayout, QWidget, QGroupBox,  QGridLayout,QSizePolicy)
from PySide6.QtCore import Qt
from dataclasses import dataclass
from typing import Optional
from collections import namedtuple
import warnings
import logging

# Logger Configuration
logger = logging.getLogger(__name__)


# Define a named tuple type for grid positions
WSGridPosition = namedtuple('GridPosition', ['row', 'column'])

@dataclass
class WSGridRecord:
    """
    A data class representing a widget and its configuration for inclusion in a custom grid layout.

    Attributes:
        widget (QWidget): The widget to be added to the grid layout.
        position (GridPosition): A named tuple specifying the row and column position of the widget in the grid.
        row_stretch (Optional[int]): The stretch factor of the widget's row. Determines how much the row
            containing the widget will stretch relative to other rows. Defaults to None, meaning no extra stretch.
        col_stretch (Optional[int]): The stretch factor of the widget's column. Determines how much the column
            containing the widget will stretch relative to other columns. Defaults to None, meaning no extra stretch.
        min_width (Optional[int]): The minimum width of the widget. This ensures that the widget's column is at
            least this wide in pixels. Defaults to None, indicating no minimum width constraint.
        col_span (Optional[int]): The number of columns the widget should span across. Defaults to 1, indicating
            no spanning.
        row_span (Optional[int]): The number of rows the widget should span across. Defaults to 1, indicating
            no spanning.
        alignment (Optional[Qt.Alignment]): The alignment of the widget within its grid cell. This can be any
            combination of Qt alignment flags. Defaults to None, indicating the default alignment.  (Qt.AlignLeft,
            Qt.AlignRight, Qt.AlignHCenter, Qt.AlignJustify, Qt.AlignTop, Qt.AlignBottom, Qt.AlignVCenter,
            Qt.AlignBaseline, Qt.AlignCenter, Qt.AlignAbsolute, Qt.AlignLeading, Qt.AlignTrailing)
            Combine with | (alignment = Qt.AlignRight | Qt.AlignBottom)

    """
    widget: QWidget
    position: WSGridPosition
    row_stretch: Optional[int] = None
    col_stretch: Optional[int] = None
    min_width: Optional[int] = None
    col_span: Optional[int] = 1  # Default to 1, meaning no spanning
    row_span: Optional[int] = 1
    # alignment: Optional[Qt.Alignment] = None
    alignment: Optional[Qt.AlignmentFlag] = None


class WSGridLayoutHandler:
    """
      Manages a custom grid layout for a QWidget container, allowing for dynamic addition of widgets,
      specification of row and column stretch factors, and widget alignment within grid cells.

      Attributes:


      Methods:
          add_widget_record(record): Adds a WidgetRecord to the layout, configuring its position,
              size, and alignment according to the record's attributes.
          add_widget_record(record: WidgetRecord): Adds a WidgetRecord to the layout, configuring its position,
              size, and alignment according to the record's attributes.
          set_row_stretch(row, stretch): Sets the stretch factor for a specified row.
          set_column_stretch(column, stretch): Sets the stretch factor for a specified column, with
              the ability to preserve explicit column stretches when aligning widgets.
          set_column_minimum_width(column, min_width): Sets the minimum width for a specified column.
          set_column_maximum_width(column, max_width): Sets the maximum width for a specified column.
          align_widgets_top_left(): Adjusts the layout to align widgets to the top left, applying
              default stretch factors to ensure alignment without overriding explicit configurations.
          align_widgets_top(): Aligns widgets to the top of the container, allowing columns to
              expand evenly across the width unless explicitly configured not to.
          get_current_column_count(): Returns the current number of columns in the layout based on added widgets.
          get_current_row_count(): Returns the current number of rows in the layout based on added widgets.
          get_layout_widget(): Returns the QWidget container managed by this layout manager.
      """

    def __init__(self, spacing=0):
        self.layout = QGridLayout()
        self.layout.setSpacing(spacing)
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.widget_records = []  # Track added widgets for layout adjustments
        self.explicit_col_stretches = {}  # Track columns with explicit stretch factors
        self.set_layout_margins(0, 0, 0, 0)

    def set_layout_margins(self, top, right, bottom, left):
        self.layout.setContentsMargins(left, top, right, bottom)

    def add_widget_record(self, record: WSGridRecord):
        # Ensure the object is a widget; if it's a layout, convert it to a widget
        if isinstance(record.widget, QLayout):
            record.widget = layout_to_widget(record.widget)

        # Set widget minimum width if specified
        if record.min_width is not None:
            record.widget.setMinimumWidth(record.min_width)

        # Add the widget to the layout with specified alignment, or default alignment if none is specified
        if record.alignment is not None:
            self.layout.addWidget(record.widget, record.position.row, record.position.column, record.row_span,
                                  record.col_span, record.alignment)
        else:
            self.layout.addWidget(record.widget, record.position.row, record.position.column, record.row_span,
                                  record.col_span)

        # Apply row stretch if specified
        if record.row_stretch is not None:
            self.set_row_stretch(record.position.row, record.row_stretch)

        # Apply column stretch if specified
        if record.col_stretch is not None:
            self.set_column_stretch(record.position.column, record.col_stretch)

        # Keep track of the added widget
        self.widget_records.append(record)

    def add_widget_records(self, records):
        for record in records:
            self.add_widget_record(record)

    def set_row_stretch(self, row, stretch):
        self.layout.setRowStretch(row, stretch)

    def set_column_stretch(self, column, stretch):
        self.layout.setColumnStretch(column, stretch)
        self.explicit_col_stretches[column] = stretch

    def set_column_minimum_width(self, column, min_width):
        for record in self.widget_records:
            if record.position.column == column:  # Check column index
                record.widget.setMinimumWidth(min_width)

    def set_column_maximum_width(self, column, max_width):
        for record in self.widget_records:
            if record.position.column == column:  # Check column index
                record.widget.setMaximumWidth(max_width)

    def create_vertical_spacer(self, height):
        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(height)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        return spacer_widget

    def create_horizontal_spacer(self, width):
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(width)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        return spacer_widget

    def align_widgets_top_left(self):
        max_row = max(record.position.row for record in self.widget_records) + 1
        max_col = max(record.position.column for record in self.widget_records) + 1
        # Set default column stretch for columns without an explicit stretch
        for col in range(max_col):
            if col not in self.explicit_col_stretches:
                self.layout.setColumnStretch(col, 0)
        self.layout.setRowStretch(max_row, 1)
        # self.layout.setColumnStretch(max_col, 1)

    def align_widgets_top(self):
        max_row = max(record.position.row for record in self.widget_records)
        # Stretch the last row to push all widgets to the top
        self.layout.setRowStretch(max_row + 1, 1)

        # Ensure columns expand evenly across the width
        # If you have columns that should not expand, set their stretch factor explicitly to 0
        # Otherwise, you can remove or modify the loop below based on your needs
        max_col = max(record.position.column for record in self.widget_records) + 1
        for col in range(max_col):
            if col not in self.explicit_col_stretches:
                self.layout.setColumnStretch(col, 0)

    def get_current_column_count(self):
        # +1 because positions are 0-indexed
        return max(record.position.column for record in self.widget_records) + 1

    def get_current_row_count(self):
        # +1 because positions are 0-indexed
        return max(record.position.row for record in self.widget_records) + 1

    # def get_layout_widget(self):
    #     return self.container

    def get_layout_widget(self) -> QWidget:
        """Deprecated: Use as_widget() instead."""
        warnings.warn(
            "get_layout_widget() is deprecated and will be removed in a future version. Use as_widget() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.as_widget()

    def as_layout(self) -> QGridLayout:
        """Returns the layout as a QGridLayout instance."""
        return self.layout

    def as_widget(self) -> QWidget:
        """Returns the QWidget containing the layout."""
        return self.container

    def as_groupbox_widget(self, title: str = "", groupbox: QGroupBox = None) -> QGroupBox:
        """
        Returns a QGroupBox containing this layout.

        If a groupbox is passed in, it uses that. Otherwise, it creates one with the optional title.
        Your main program can then hold a reference to the returned QGroupBox for visibility control, etc.

        Args:
            title (str): Title for a new groupbox (only if groupbox is None).
            groupbox (QGroupBox, optional): An existing groupbox to use.

        Returns:
            QGroupBox: The group box containing the layout.
        """
        if groupbox is None:
            groupbox = QGroupBox(title)
        groupbox.setLayout(self.layout)
        return groupbox

    def hide_row(self, row):
        for record in self.widget_records:
            if record.position.row == row:
                record.widget.hide()

    def show_row(self, row):
        for record in self.widget_records:
            if record.position.row == row:
                record.widget.show()

    def toggle_row_visibility(self, row):
        is_hidden = self.is_row_hidden(row)
        if is_hidden:
            self.show_row(row)
        else:
            self.hide_row(row)

    def is_row_hidden(self, row):
        for record in self.widget_records:
            if record.position.row == row:
                return not record.widget.isVisible()
        return False

    def hide_column(self, column):
        for record in self.widget_records:
            if record.position.column == column:
                record.widget.hide()

    def show_column(self, column):
        for record in self.widget_records:
            if record.position.column == column:
                record.widget.show()

    def toggle_column_visibility(self, column):
        is_hidden = self.is_column_hidden(column)
        if is_hidden:
            self.show_column(column)
        else:
            self.hide_column(column)

    def is_column_hidden(self, column):
        for record in self.widget_records:
            if record.position.column == column:
                return not record.widget.isVisible()
        return False


def layout_to_widget(layout: QLayout) -> QWidget:
    """
    Converts a given QLayout to a QWidget containing that layout.

    Parameters:
    layout (QLayout): The layout to be converted to a QWidget. Must be an instance of QLayout or its subclasses.

    Returns:
    QWidget: A widget that contains the provided layout.

    Raises:
    TypeError: If the layout is not an instance of QLayout.
    ValueError: If the layout is already set on another widget.
    """
    if not isinstance(layout, QLayout):
        raise TypeError("The provided layout must be an instance of QLayout or its subclasses.")

    if layout.parentWidget() is not None:
        raise ValueError("The provided layout is already set on another widget.")

    # Create a new QWidget
    widget = QWidget()

    # Set the provided layout to the widget
    widget.setLayout(layout)

    return widget
