from controllers.student_controller import getAllStudents
from controllers.actionButtons import createEditAndDeleteButtons
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt

HEADERS = ["ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code"]  

def loadStudents(tableWidget, onEdit, onDelete):
    tableWidget.clearContents()
    tableWidget.setRowCount(0)
    students = getAllStudents()

    # Setup columns
    tableWidget.setColumnCount(len(HEADERS) + 1)  # +1 for Actions
    tableWidget.setHorizontalHeaderLabels(HEADERS + ["Actions"])
    tableWidget.horizontalHeader().setVisible(True)

    if students:
        tableWidget.setRowCount(len(students))
        for row_idx, row_data in enumerate(students):
            for col_idx, value in enumerate(row_data):

                if value is None:
                    value = "N/A"

                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tableWidget.setItem(row_idx, col_idx, item)

            # Add Action Buttons with callback
            editButton, deleteButton = createEditAndDeleteButtons(row_idx, tableWidget)

            editButton.clicked.connect(lambda _, row_idx=row_idx: onEdit(row_idx, tableWidget))
            deleteButton.clicked.connect(lambda _, row_idx=row_idx: onDelete(row_idx, tableWidget))
