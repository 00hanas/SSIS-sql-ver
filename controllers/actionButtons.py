from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QTableWidget, QMessageBox, QStyledItemDelegate
from PyQt6.QtGui import QIcon, QColor, QBrush, QPainter, QPen
from PyQt6.QtCore import Qt

def createEditAndDeleteButtons(row_idx, tableWidget, on_edit, on_delete):
    actions = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Edit Button
    editButton = QPushButton()
    editButton.setFixedSize(20, 20)
    editButton.setIcon(QIcon("C:/Users/ASUS/OneDrive/Documents/BSCS/Second Year/Second Sem/CCC151/SSIS V2/icon/edit icon.png"))

    editButton.setStyleSheet("""
        QPushButton{
            background-color: #043927;
            border: 0px;
            border-radius: 5px;              
        }
        QPushButton:hover{
            background-color: #065f46;     
        }
    """)
    editButton.clicked.connect(lambda _, idx=row_idx: on_edit(idx, tableWidget))
    layout.addWidget(editButton)

    # Delete Button
    deleteButton = QPushButton()
    deleteButton.setFixedSize(20, 20)
    deleteButton.setIcon(QIcon("C:/Users/ASUS/OneDrive/Documents/BSCS/Second Year/Second Sem/CCC151/SSIS V2/icon/delete icon.png"))
    deleteButton.setStyleSheet("""
        QPushButton{
            background-color: #8B0000;
            border: 0px;
            border-radius: 5px;             
        }
        QPushButton:hover{
            background-color: #B22222;           
        }
    """)
    deleteButton.clicked.connect(lambda _, idx=row_idx: showDeleteConfirmation(idx, tableWidget, on_delete))
    layout.addWidget(deleteButton)

    actions.setLayout(layout)
    tableWidget.setCellWidget(row_idx, tableWidget.columnCount() - 1, actions)
    tableWidget.setColumnWidth(tableWidget.columnCount() - 1, 120)

def showDeleteConfirmation(row_idx, tableWidget, on_delete):
    """Displays confirmation dialog before delete."""
    item = tableWidget.item(row_idx, 0)
    identifier = item.text() if item else "this item"
    confirm = QMessageBox.question(
        tableWidget,
        "Confirm Deletion",
        f"Are you sure you want to delete {identifier}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    if confirm == QMessageBox.StandardButton.Yes:
        on_delete(row_idx, tableWidget)

def saveEditedRow(row_idx, tableWidget, main_window=None, table_name=None):
    """Saves the edited row data back to the database."""

    try:
        # Collect data from the row
        data = []
        for col_idx in range(tableWidget.columnCount() - 1):  # Exclude Actions column
            item = tableWidget.item(row_idx, col_idx)
            data.append(item.text() if item else "")
        
        # Call the appropriate controller function based on table_name
        if table_name == "student":
            from controllers.student_controller import updateStudent
            updateStudent(data[0], data[1:])
        

        # Refresh the table after saving
        if main_window:
            if table_name == "student":
                from views.student_view import loadStudents
                loadStudents(main_window.ui.tableWidget_students)

        
            

    except Exception as e:
        print(f"[saveEditedRow] Error: {e}")


def deleteStudent(row_idx, tableWidget, main_window=None, table_name="student"):
    """Deletes the selected student from the database."""
    item = tableWidget.item(row_idx, 0)
    student_id = item.text() if item else None

    if student_id:
        from controllers.student_controller import deleteStudent
        deleteStudent(student_id)

        # Refresh the table after deletion
        if main_window:
            from views.student_view import loadStudents
            loadStudents(main_window.ui.tableWidget_students)

"""
def deleteProgram(row_idx, tableWidget, main_window=None, table_name="program"):
    
    item = tableWidget.item(row_idx, 0)
    program_code = item.text() if item else None

    if program_code:
        from controllers.program_controller import deleteProgram
        deleteProgram(program_code)

        # Refresh the table after deletion
        if main_window:
            from views.program_view import loadPrograms
            loadPrograms(main_window.ui.tableWidget_programs)

def deleteCollege(row_idx, tableWidget, main_window=None, table_name="college"):
    
    item = tableWidget.item(row_idx, 0)
    college_code = item.text() if item else None

    if college_code:
        from controllers.college_controller import deleteCollege
        deleteCollege(college_code)

        # Refresh the table after deletion
        if main_window:
            from views.college_view import loadColleges
            loadColleges(main_window.ui.tableWidget_colleges)

"""

class EditDelegate(QStyledItemDelegate):
    """Custom delegate to enforce font color during editing."""
    def paint(self, painter: QPainter, option, index):
        painter.save()
        painter.setPen(QPen(QColor("#043927")))  # Set font color to #043927
        super().paint(painter, option, index)
        painter.restore()

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        editor.setStyleSheet("color: #043927;")  # Ensure text color stays #043927
        return editor

def editMode(row_idx, tableWidget, main_window=None, table_name=None):
    columnCount = tableWidget.columnCount()
    delegate = EditDelegate(tableWidget)
    tableWidget.setItemDelegateForRow(row_idx, delegate)

    original_values = [tableWidget.item(row_idx, col_idx).text() if tableWidget.item(row_idx, col_idx) else "" 
                       for col_idx in range(columnCount - 1)]

    #Replace Edit/Delete buttons with Save button
    actions = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # Save Button

    saveButton = QPushButton()
    saveButton.setFixedSize(20, 20)
    saveButton.setIcon(QIcon("C:/Users/ASUS/OneDrive/Documents/BSCS/Second Year/Second Sem/CCC151/SSIS V2/icon/save icon.png"))
    saveButton.setStyleSheet("""
    QPushButton {
        background-color: #043927;
        border-radius: 5px;
        border: none;
        color: white;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #065f46;
    }
""")
    
    def saveOrCancel():
        """Ask user for confirmation before saving or canceling edits."""
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Confirm Edit")
        msgBox.setText("Do you want to save the changes?")
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msgBox.setDefaultButton(QMessageBox.StandardButton.Yes)
        
        result = msgBox.exec()

        if result == QMessageBox.StandardButton.Yes:
            saveEditedRow(row_idx, tableWidget, table_name)  # Save changes
        else:
            # Restore original values
            for col_idx in range(columnCount - 1):
                tableWidget.item(row_idx, col_idx).setText(original_values[col_idx])
            
            # Reset cell formatting
            for col_idx in range(columnCount - 1):
                item = tableWidget.item(row_idx, col_idx)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Disable editing
                    item.setBackground(QBrush(Qt.GlobalColor.white))  # Reset background
                    item.setForeground(QBrush(Qt.GlobalColor.black))  # Reset text color

            # Restore Edit/Delete buttons
            createEditAndDeleteButtons(row_idx, tableWidget, main_window)
        
    saveButton.clicked.connect(saveOrCancel)
    layout.addWidget(saveButton)

    actions.setLayout(layout)
    tableWidget.setCellWidget(row_idx, columnCount - 1, actions)





    '''
    """Enters edit mode for the selected row."""
    tableWidget.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
    tableWidget.setCurrentCell(row_idx, 0)  # Set focus on the first cell of the row

    # Save button
    saveButton = QPushButton("Save")
    saveButton.clicked.connect(lambda: saveEditedRow(row_idx, tableWidget, main_window, table_name))
    tableWidget.setCellWidget(row_idx, tableWidget.columnCount() - 1, saveButton)
    
    # Disable edit triggers
    tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)'
    '''
