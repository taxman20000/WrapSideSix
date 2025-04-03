# widgets/list_widget_py

from PySide6.QtWidgets import QListWidget, QAbstractItemView, QMenu, QListWidgetItem
from PySide6.QtCore import Signal, Qt
import logging

# Logger Configuration
logger = logging.getLogger(__name__)


class WSListSelectionWidget(QListWidget):
    selection_changed = Signal()
    selected = Signal(int, str)
    doubleClicked = Signal(str, str)
    rightClicked = Signal(int, str)

    def __init__(self, multi_select=False, actions=None):
        super().__init__()

        # Set selection mode
        if multi_select:
            self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        else:
            self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.actions = actions if actions else {}
        self.connect_signals()

    def connect_signals(self):
        self.itemSelectionChanged.connect(self.get_data_to_emit)
        self.itemDoubleClicked.connect(self.handle_double_click)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.handle_right_click)

    def add_items(self, items):
        """Simplified method to add items to the list with unique IDs."""
        existing_ids = set(self.get_all_ids())
        next_id = max(existing_ids, default=0) + 1  # Ensure uniqueness

        for item in items:
            while next_id in existing_ids:  # Avoid ID collisions
                next_id += 1

            list_widget_item = QListWidgetItem(item)
            list_widget_item.setData(Qt.ItemDataRole.UserRole, next_id)
            self.addItem(list_widget_item)
            existing_ids.add(next_id)

    def populate_list(self, items, display_index=1, id_index=0, sort_mode=None):
        """Clears list and populates it with new items."""
        self.clear()

        if sort_mode == "asc":
            items = sorted(items, key=lambda x: x[display_index] if len(x) > display_index else '')
        elif sort_mode == "desc":
            items = sorted(items, key=lambda x: x[display_index] if len(x) > display_index else '', reverse=True)
        # else: leave unsorted

        for item in items:
            display_text = item[display_index] if len(item) > display_index else 'Unknown'
            item_id = item[id_index] if len(item) > id_index else None

            if item_id is None:
                logger.error(f"ERROR! Item has no ID -> {display_text}")
            elif item_id == 0:
                logger.error(f"ERROR! Item ID is 0 -> {display_text}")

            if item_id is not None:
                list_widget_item = QListWidgetItem(display_text)
                list_widget_item.setData(Qt.ItemDataRole.UserRole, item_id)  # ✅ Storing doc_id
                self.addItem(list_widget_item)

        if self.count() > 0:
            self.setCurrentRow(0)

    def get_data_to_emit(self):
        """Emit signals for selected item."""
        self.selection_changed.emit()
        selected_items = self.selectedItems()
        if selected_items:
            item = selected_items[0]
            item_id = item.data(Qt.ItemDataRole.UserRole)
            item_name = item.text()
            self.selected.emit(item_id, item_name)

    def get_selected_item(self):
        """Retrieve selected item's data."""
        selected_items = self.selectedItems()
        if selected_items:
            item = selected_items[0]
            return item.data(Qt.ItemDataRole.UserRole), item.text()
        return None, None

    def get_all_selected_items(self):
        """Retrieve data for all selected items (multi-select)."""
        return [(item.data(Qt.ItemDataRole.UserRole), item.text()) for item in self.selectedItems()]

    # def handle_double_click(self, item):
    #     """Handle double-click event."""
    #     self.doubleClicked.emit(item.data(Qt.UserRole), item.text())

    def handle_double_click(self, item):
        """Handle double-click event."""
        item_id = str(item.data(Qt.ItemDataRole.UserRole))  # 🔹 Force it to be a string
        item_name = item.text()

        logger.debug(f"Double Clicked Item -> ID: {item_id}, Name: {item_name} (type: {type(item_id)})")

        self.doubleClicked.emit(item_id, item_name)  # 🔹 Always emit as a string

    def handle_right_click(self, position):
        """Handle right-click event with custom menu actions."""
        item = self.itemAt(position)
        if not item:
            return  # No item under the cursor

        item_id = item.data(Qt.ItemDataRole.UserRole)
        item_name = item.text()

        menu = QMenu(self)
        for action_name, action_function in self.actions.items():
            action = menu.addAction(action_name)
            action.triggered.connect(lambda _, fn=action_function, id=item_id, name=item_name: fn(id, name))

        menu.exec(self.viewport().mapToGlobal(position))

    def select_by_id(self, record_id):
        """Select an item by ID."""
        for index in range(self.count()):
            item = self.item(index)
            if item.data(Qt.ItemDataRole.UserRole) == record_id:
                self.setCurrentRow(index)
                self.get_data_to_emit()
                return True
        return False

    def get_all_ids(self):
        """Retrieve all item IDs in the list."""
        return [self.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.count())]

    def get_all_ids_and_texts(self):
        """Retrieve all IDs and text values."""
        return [(self.item(i).data(Qt.ItemDataRole.UserRole), self.item(i).text()) for i in range(self.count())]

    # Navigation Methods
    def go_to_first_line(self):
        if self.count() > 0:
            self.setCurrentRow(0)

    def go_to_last_line(self):
        if self.count() > 0:
            self.setCurrentRow(self.count() - 1)

    def go_to_next_line(self):
        if self.currentRow() < self.count() - 1:
            self.setCurrentRow(self.currentRow() + 1)

    def go_to_previous_line(self):
        if self.currentRow() > 0:
            self.setCurrentRow(self.currentRow() - 1)

    def get_current_row_number(self):
        # return self.currentRow() + 1 if self.currentRow() >= 0 else 0
        return max(self.currentRow() + 1, 0)

    def get_total_rows(self):
        return self.count()

    def get_selected_count(self):
        """Return the number of selected rows."""
        return len(self.selectedItems())

