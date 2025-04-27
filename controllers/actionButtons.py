from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

def createEditAndDeleteButtons(row_idx, tableWidget):
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
    #deleteButton.clicked.connect(lambda _, idx=row_idx: showDeleteConfirmation(idx, tableWidget, on_delete))
    layout.addWidget(deleteButton)

    actions.setLayout(layout)
    tableWidget.setCellWidget(row_idx, tableWidget.columnCount() - 1, actions)
    tableWidget.setColumnWidth(tableWidget.columnCount() - 1, 120)

    return editButton, deleteButton
