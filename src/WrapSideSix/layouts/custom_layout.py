# layouts/custom_layout.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout)
import logging

# Logger Configuration
logger = logging.getLogger(__name__)


def create_custom_layout(widgets, layout_type='V', return_type='widget', align='top', spacing=0, stretch_factors=None, margins=(0, 0, 0, 0)):
    """
    Create a QVBoxLayout or QHBoxLayout containing the specified widgets.

    Args:
        widgets (list): A list of QWidget objects to be added to the layout.
        layout_type (str): Specify 'V' for QVBoxLayout or 'H' for QHBoxLayout.
        return_type (str): Specify 'widget' to return a QWidget containing the layout, or 'layout' to return the layout itself.
        align (str): Alignment of widgets within the layout. Options: 'left', 'bottom_right', 'center'.
        spacing (int): Space between widgets.
        stretch_factors (list): List of stretch factors for each widget.

    Returns:
        QWidget or QLayout: A QWidget containing the specified layout, or the layout itself, containing the specified widgets.
    """

    assert layout_type.upper() in ["V", "H"], f"Invalid layout type: {layout_type}"
    # self.value = value
    assert return_type.lower() in ['widget', 'layout'], f"Invalid return_type: {return_type}"
    assert align.lower() in ['top', 'bottom', 'left', 'right', 'center'], f"Invalid align: {align}"

    wl = len(widgets)
    if stretch_factors:
        ws = len(stretch_factors)
        assert wl == ws, f"Widgets and Stretch Factors must have the same number of list items: {wl} != {ws}"

    if layout_type.upper() == 'V':
        layout = QVBoxLayout()
    elif layout_type.upper() == 'H':
        layout = QHBoxLayout()
    else:
        raise ValueError("Invalid layout_type. Use 'V' for QVBoxLayout or 'H' for QHBoxLayout.")

    layout.setSpacing(spacing)
    layout.setContentsMargins(*margins)  # Set layout margins

    if align.lower() == 'bottom' or align.lower() == 'right' or align.lower() == 'center':
        layout.addStretch()  # This will push widgets to the top

    for i, widget in enumerate(widgets):
        layout.addWidget(widget)
        if stretch_factors is not None:
            layout.setStretchFactor(widget, stretch_factors[i])
        # spacer = QSpacerItem(0, spacing, QSizePolicy.Fixed, QSizePolicy.Fixed)
        # layout.addItem(spacer)

    if align.lower() == 'top' or align.lower() == 'left' or align.lower() == 'center':  # or align.lower() == 'left'
        layout.addStretch()  # This will push widgets to the top

    if return_type.lower() == 'widget':
        container = QWidget()
        container.setLayout(layout)
        return container
    elif return_type.lower() == 'layout':
        return layout
    else:
        raise ValueError(
            "Invalid return_type. Use 'widget' to return a QWidget, or 'layout' to return the layout itself.")

