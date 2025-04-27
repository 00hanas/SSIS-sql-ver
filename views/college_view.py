from controllers.college_controller import getAllColleges
from controllers.actionButtons import createEditAndDeleteButtons, editMode, deleteStudent
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt

HEADERS = ["College Code", "College Name"]

def loadColleges(tableWidget):
    tableWidget.clearContents()
    tableWidget.setRowCount(0)
    colleges = getAllColleges()

    # Setup columns
    tableWidget.setColumnCount(len(HEADERS) + 1)  # +1 for Actions
    tableWidget.setHorizontalHeaderLabels(HEADERS + ["Actions"])
    tableWidget.horizontalHeader().setVisible(True)

    if colleges:
        tableWidget.setRowCount(len(colleges))
        for row_idx, row_data in enumerate(colleges):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tableWidget.setItem(row_idx, col_idx, item)

            # Add Action Buttons with callbacks
            createEditAndDeleteButtons(row_idx, tableWidget, on_edit=editMode, on_delete=deleteStudent)