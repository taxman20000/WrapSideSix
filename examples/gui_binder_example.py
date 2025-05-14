# gui_binder_example.py (extended)

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
                                 QComboBox, QDateEdit, QDateTimeEdit, QTextEdit, QPushButton)
from PySide6.QtCore import QDate, QDateTime
from dataclasses import dataclass
from WrapSideSix.io.gui_binder import WSGuiBinder, JsonIO  # adjust import if needed
from WrapSideSix.widgets.line_edit_widget import WSLineButtonFile
import sys

@dataclass
class Person:
    name: str = ""
    age: int = 0
    salary: float = 0.0
    role: str = ""
    birthday: str = ""
    last_updated: str = ""
    notes: str = ""
    resume_path: str = ""

class PersonForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Person Form")

        # Create widgets
        self.name_input = QLineEdit()
        self.age_input = QSpinBox()
        self.age_input.setRange(0, 150)
        self.salary_input = QDoubleSpinBox()
        self.salary_input.setRange(0.0, 1_000_000.0)
        self.role_input = QComboBox()
        self.role_input.addItems(["", "Engineer", "Designer", "Manager"])
        self.birthday_input = QDateEdit()
        self.birthday_input.setCalendarPopup(True)
        self.birthday_input.setDate(QDate.currentDate())
        self.last_updated_input = QDateTimeEdit()
        self.last_updated_input.setCalendarPopup(True)
        self.last_updated_input.setDateTime(QDateTime.currentDateTime())
        self.notes_input = QTextEdit()
        self.resume_input = WSLineButtonFile()

        self.save_btn = QPushButton("Save")
        self.load_btn = QPushButton("Load")
        self.clear_btn = QPushButton("Clear")
        self.check_btn = QPushButton("Check Required Fields")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Age:"))
        layout.addWidget(self.age_input)
        layout.addWidget(QLabel("Salary:"))
        layout.addWidget(self.salary_input)
        layout.addWidget(QLabel("Role:"))
        layout.addWidget(self.role_input)
        layout.addWidget(QLabel("Birthday:"))
        layout.addWidget(self.birthday_input)
        layout.addWidget(QLabel("Last Updated:"))
        layout.addWidget(self.last_updated_input)
        layout.addWidget(QLabel("Notes:"))
        layout.addWidget(self.notes_input)
        layout.addWidget(QLabel("Resume File Path:"))
        layout.addWidget(self.resume_input)

        layout.addWidget(self.save_btn)
        layout.addWidget(self.load_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.check_btn)
        self.setLayout(layout)

        # Wire up binder
        self.widgets = {
            "name": self.name_input,
            "age": self.age_input,
            "salary": self.salary_input,
            "role": self.role_input,
            "birthday": self.birthday_input,
            "last_updated": self.last_updated_input,
            "notes": self.notes_input,
            "resume_path": self.resume_input,
        }
        self.binder = WSGuiBinder(Person, self.widgets)
        self.io = JsonIO()
        self.json_path = "person.json"

        # Required fields (subset)
        self.required_fields = ["name", "age", "role", "resume_path"]

        # Connect buttons
        self.save_btn.clicked.connect(self.save_person)
        self.load_btn.clicked.connect(self.load_person)
        self.clear_btn.clicked.connect(self.clear_form)
        self.check_btn.clicked.connect(self.check_fields)

    def save_person(self):
        self.binder.from_gui()
        self.io.save(self.binder.instance, self.json_path)
        print("✅ Saved:", self.binder.instance)

    def load_person(self):
        person = self.io.load(self.json_path, Person)
        self.binder.instance = person
        self.binder.to_gui()
        print("📥 Loaded:", person)

    def clear_form(self):
        self.binder.clear_gui()
        print("🧹 Cleared form")

    def check_fields(self):
        filled = self.binder.all_fields_filled(self.required_fields)
        print("✅ Required fields filled" if filled else "❌ Some required fields are missing")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonForm()
    window.show()
    sys.exit(app.exec())

