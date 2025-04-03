# examples/list_widget_example.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from WrapSideSix.widgets.list_widget import WSListSelectionWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WSListSelectionWidget Example")
        self.setGeometry(100, 100, 400, 300)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Sample actions for the context menu
        actions = {
            "Print Selection": lambda item_id, item_name: self.print_selection(item_id, item_name),
            "Clear List": lambda *_: self.clear_list()
        }

        # Create the WSListSelectionWidget
        self.list_widget = WSListSelectionWidget(multi_select=True, actions=actions)
        layout.addWidget(self.list_widget)

        # Connect signals
        self.list_widget.selected.connect(self.on_item_selected)
        self.list_widget.doubleClicked.connect(self.on_item_double_clicked)
        self.list_widget.rightClicked.connect(self.on_item_right_clicked)

        # Populate the list with sample data
        sample_data = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        self.list_widget.add_items(sample_data)

    def on_item_selected(self, item_id, item_name):
        print(f"Selected: ID={item_id}, Name={item_name}")

    def on_item_double_clicked(self, item_id, item_name):
        print(f"Double Clicked: ID={item_id}, Name={item_name}")

    def on_item_right_clicked(self, item_id, item_name):
        print(f"Right Clicked: ID={item_id}, Name={item_name}")

    def print_selection(self, item_id, item_name):
        print(f"Context Menu: Selected Item: ID={item_id}, Name={item_name}")

    def clear_list(self):
        self.list_widget.clear()
        print("List cleared.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

