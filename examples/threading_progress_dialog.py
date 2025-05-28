from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
)
import time
import logging

from WrapSideSix import run_in_thread
from WrapSideSix import WSProgressHandler

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProgressExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WSProgressHandler Example")
        self.setMinimumSize(400, 250)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.button = QPushButton("Start Task")

        layout = QVBoxLayout(self)
        layout.addWidget(self.output)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.start_task)

    def long_task(self, progress_callback=None):
        for i in range(11):
            time.sleep(0.3)  # Simulate work
            if progress_callback:
                progress_callback(i * 10)  # Send progress (0 to 100)
        return "Task complete!"

    def start_task(self):
        self.button.setEnabled(False)
        self.output.setPlainText("Running task...")

        self.progress = WSProgressHandler(self, use_dialog=True, title="Processing...", indeterminate=False)
        self.progress.show()

        def on_progress(value):
            self.progress.set_value(value)
            self.output.setPlainText(f"Progress: {value}%")

        def on_finish(result):
            self.progress.close()
            self.output.setPlainText(result)
            self.button.setEnabled(True)

        def on_error(err):
            self.progress.close()
            exception, tb = err
            logger.error(tb)
            QMessageBox.critical(self, "Error", str(exception))
            self.button.setEnabled(True)

        run_in_thread(
            self.long_task,
            on_start=lambda: logger.info("Thread started"),
            on_progress=on_progress,
            on_finish=on_finish,
            on_error=on_error,
            parent=self
        )

if __name__ == "__main__":
    app = QApplication([])
    window = ProgressExample()
    window.show()
    app.exec()
