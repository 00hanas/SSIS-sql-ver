from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
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

class ConfirmDialog(QDialog):
    """
    Yes/No confirmation dialog. exec() returns True if user clicks Yes.
    """
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)

        self.setStyleSheet(
            """
            background-color: #043927;
            border-radius: 15px;
            """
        )
        self._result = False

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Message label
        label = QLabel(message)
        label.setStyleSheet(
            """
            color: white;
            font-size: 11px;
            font-weight: bold;
            """
        )
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Buttons layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yes_btn = QPushButton("Yes")
        yes_btn.setFixedSize(50, 20)
        yes_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #043927;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            """
        )
        yes_btn.clicked.connect(self._on_yes)
        btn_layout.addWidget(yes_btn)

        no_btn = QPushButton("No")
        no_btn.setFixedSize(50, 20)
        no_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #FFFFFF;
                color: #043927;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            """
        )
        no_btn.clicked.connect(self.reject)
        btn_layout.addWidget(no_btn)

        layout.addLayout(btn_layout)

    def _on_yes(self):
        self._result = True
        self.accept()

    def exec(self) -> bool:
        super().exec()
        return self._result
    