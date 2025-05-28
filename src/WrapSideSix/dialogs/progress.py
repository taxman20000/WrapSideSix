# progress.py

from PySide6.QtWidgets import QProgressDialog, QProgressBar
from PySide6.QtCore import Qt

import logging

# Logger Configuration
logger = logging.getLogger(__name__)


class WSProgressHandler:
    def __init__(self, parent, use_dialog=True, title="Working...", modal=True, indeterminate=False):
        self.use_dialog = use_dialog
        self.progress = None
        self.indeterminate = indeterminate

        if use_dialog:
            min_val = 0
            max_val = 0 if indeterminate else 100
            self.progress = QProgressDialog(title, "", min_val, max_val, parent)
            self.progress.setWindowTitle(title)
            self.progress.setMinimumDuration(0)
            self.progress.setAutoClose(False)
            self.progress.setAutoReset(False)
            self.progress.setCancelButtonText("")
            if modal:
                self.progress.setWindowModality(Qt.WindowModality.WindowModal)
        else:
            self.progress = QProgressBar(parent)
            if indeterminate:
                self.progress.setRange(0, 0)
            else:
                self.progress.setRange(0, 100)
                self.progress.setValue(0)

    def show(self):
        if isinstance(self.progress, QProgressDialog):
            if not self.indeterminate:
                self.progress.setValue(0)
            self.progress.show()

    def set_value(self, value):
        # Only update if determinate
        if not self.indeterminate:
            self.progress.setValue(int(value))

    def close(self):
        self.progress.close()

