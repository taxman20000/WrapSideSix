# threading example

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QMessageBox, QProgressBar
import logging
import time

# === Configure Logging ===
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

from WrapSideSix.tasks.thread_runner import run_in_thread

class ThreadExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Threading Example")
        self.setMinimumSize(400, 300)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.button = QPushButton("Start Task")
        self.error_button = QPushButton("Start Task with Error")

        layout = QVBoxLayout(self)
        layout.addWidget(self.output)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.button)
        layout.addWidget(self.error_button)

        self.button.clicked.connect(self.start_task)
        self.error_button.clicked.connect(self.start_error_task)

    def long_running_task(self, input_text, progress_callback=None):
        """Task that reports progress"""
        for i in range(10):
            time.sleep(0.3)  # simulate work
            if progress_callback:
                progress_callback(i * 10)

        # Final step
        time.sleep(0.3)
        if progress_callback:
            progress_callback(100)

        return f"Completed task with input: {input_text}"

    def task_with_error(self, progress_callback=None):
        """Task that will raise an exception"""
        for i in range(5):
            time.sleep(0.3)
            if progress_callback:
                progress_callback(i * 10)

        # Simulate an error
        raise ValueError("This is a simulated error")

    def start_task(self):
        self.button.setEnabled(False)
        self.error_button.setEnabled(False)
        self.output.setPlainText("Working...")
        self.progress_bar.setValue(0)

        def on_finish(result):
            self.output.setPlainText(result)
            self.button.setEnabled(True)
            self.error_button.setEnabled(True)

        def on_error(error_info):
            exception, traceback_str = error_info
            self.output.setPlainText(f"Error occurred:\n{traceback_str}")
            QMessageBox.critical(self, "Error", str(exception))
            self.button.setEnabled(True)
            self.error_button.setEnabled(True)

        def on_progress(value):
            self.progress_bar.setValue(value)
            self.output.setPlainText(f"Working... {value}%")

        run_in_thread(
            self.long_running_task,
            "sample input",
            on_finish=on_finish,
            on_error=on_error,
            on_progress=on_progress,
            parent=self
        )

    def start_error_task(self):
        self.button.setEnabled(False)
        self.error_button.setEnabled(False)
        self.output.setPlainText("Working (will fail)...")
        self.progress_bar.setValue(0)

        def on_finish(result):
            # This won't be called due to the error
            self.output.setPlainText(result)
            self.button.setEnabled(True)
            self.error_button.setEnabled(True)

        def on_error(error_info):
            exception, traceback_str = error_info
            self.output.setPlainText(f"Error occurred:\n{traceback_str}")
            QMessageBox.critical(self, "Error", str(exception))
            self.button.setEnabled(True)
            self.error_button.setEnabled(True)

        def on_progress(value):
            self.progress_bar.setValue(value)
            self.output.setPlainText(f"Working (will fail)... {value}%")

        # Remove the "error input" argument that was causing the issue
        run_in_thread(
            self.task_with_error,
            on_finish=on_finish,
            on_error=on_error,
            on_progress=on_progress,
            parent=self
        )

if __name__ == "__main__":
    app = QApplication([])
    win = ThreadExample()
    win.show()
    app.exec()


