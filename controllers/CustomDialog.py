from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class CustomDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.setStyleSheet("""
            background-color: #043927;
            border-radius: 15px;
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Message Label
        label = QLabel(message)
        label.setStyleSheet("""
            color: white;
            font-size: 11px;
            font-weight: bold;
        """)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # OK Button
        button = QPushButton("OK")
        button.setFixedSize(50, 20)
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #043927;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        button.clicked.connect(self.accept)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
