import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from views.mainui import Ui_MainWindow
from views.student_view import loadStudents
from views.program_view import loadPrograms
from views.college_view import loadColleges
from controllers.student_controller import AddStudentForm
from controllers.student_controller import EditStudentForm, deleteStudentbyID
from controllers.program_controller import AddProgramForm, EditProgramForm, deleteProgrambyID
from controllers.college_controller import AddCollegeForm, EditCollegeForm, deleteCollegebyID
from controllers.sortFunction import sortTable
from controllers.searchFunction import searchTable
from controllers.CustomDialog import CustomDialog, ConfirmDialog

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set default tab
        self.ui.tabWidget.setCurrentIndex(0)

        # Tab 1 navigation
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(1))  
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(2))

        # Tab 2 navigation
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(0))
        self.ui.pushButton_7.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(2))

        # Tab 3 navigation
        self.ui.pushButton_8.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(0))
        self.ui.pushButton_9.clicked.connect(lambda: self.ui.tabWidget.setCurrentIndex(1))

        #Add button for Student page
        self.ui.pushButton.clicked.connect(self.show_addStudent)

        #Add button for Program page
        self.ui.pushButton_11.clicked.connect(self.show_addProgram)

        #Add button for College page   
        self.ui.pushButton_12.clicked.connect(self.show_addCollege)

        #Sort Student table
        self.ui.comboBox_2.currentTextChanged.connect(self.studentSort)
        self.ui.comboBox_3.currentTextChanged.connect(self.studentSort)

        #Sort Program table
        self.ui.comboBox_4.currentTextChanged.connect(self.programSort)
        self.ui.comboBox_5.currentTextChanged.connect(self.programSort)

        #Sort College table
        self.ui.comboBox_7.currentTextChanged.connect(self.collegeSort)
        self.ui.comboBox_8.currentTextChanged.connect(self.collegeSort)

        # Connect search for Students page
        self.ui.lineEdit.textChanged.connect(lambda: searchTable(self.ui.tableWidget, self.ui.lineEdit, self.ui.comboBox))  
        self.ui.comboBox.currentTextChanged.connect(lambda: searchTable(self.ui.tableWidget, self.ui.lineEdit, self.ui.comboBox))  

        # Connect search for Programs page
        self.ui.lineEdit_2.textChanged.connect(lambda: searchTable(self.ui.tableWidget_2, self.ui.lineEdit_2, self.ui.comboBox_6))  
        self.ui.comboBox_6.currentTextChanged.connect(lambda: searchTable(self.ui.tableWidget_2, self.ui.lineEdit_2, self.ui.comboBox_6))  

        # Connect search for Colleges page
        self.ui.lineEdit_3.textChanged.connect(lambda: searchTable(self.ui.tableWidget_3, self.ui.lineEdit_3, self.ui.comboBox_9))  
        self.ui.comboBox_9.currentTextChanged.connect(lambda: searchTable(self.ui.tableWidget_3, self.ui.lineEdit_3, self.ui.comboBox_9))


        # Load tables with MySQL data
        if hasattr(self.ui, 'tableWidget'):
            loadStudents(self.ui.tableWidget, self.showEditStudent, self.deleteStudent)  # Pass tableWidget to function

        if hasattr(self.ui, 'tableWidget_2'):  # Assuming tableWidget_2 is on page 2
            loadPrograms(self.ui.tableWidget_2, self.showEditProgram, self.deleteProgram)  # Pass tableWidget_2 to function

        if hasattr(self.ui, 'tableWidget_3'):  # Assuming tableWidget_2 is on page 2
            loadColleges(self.ui.tableWidget_3, self.showEditCollege, self.deleteCollege)  # Pass tableWidget_2 to function

    def show_addStudent(self):
        self.addStudentWindow = AddStudentForm(self)
        self.addStudentWindow.show()
        if self.addStudentWindow.exec():
            loadStudents(self, self.ui.tableWidget, self, self)

    def show_addProgram(self):
        self.addProgramWindow = AddProgramForm(self)
        self.addProgramWindow.show()
        if self.addProgramWindow.exec():
            loadPrograms(self.ui.tableWidget_2)

    def show_addCollege(self):
        self.addCollegeWindow = AddCollegeForm(self)
        self.addCollegeWindow.show()
        if self.addCollegeWindow.exec():
            loadColleges(self.ui.tableWidget_3)

    def showEditStudent(self, row_idx=None, tableWidget=None):
        if tableWidget is None:
            tableWidget = None  

        if row_idx is None:
            row_idx = tableWidget.currentRow()

        if row_idx < 0:
            from controllers.CustomDialog import CustomDialog  
            dialog = CustomDialog("Error", "Please select a student to edit.")
            dialog.exec()
            return

        student_id = tableWidget.item(row_idx, 0).text()

        # 3) Open the EditStudentForm
        dlg = EditStudentForm(self, originalID=student_id)  
        if dlg.exec():  
            from views.student_view import loadStudents
            loadStudents(self.ui.tableWidget, self.showEditStudent, self.deleteStudent)

    def showEditProgram(self, row_idx=None, tableWidget=None):
        if tableWidget is None:
            tableWidget = None  

        if row_idx is None:
            row_idx = tableWidget.currentRow()

        if row_idx < 0:
            from controllers.CustomDialog import CustomDialog  
            dialog = CustomDialog("Error", "Please select a program to edit.")
            dialog.exec()
            return

        program_code = tableWidget.item(row_idx, 0).text()

        dlg = EditProgramForm(self, originalCode=program_code)  
        if dlg.exec():  
            from views.program_view import loadPrograms
            loadPrograms(self.ui.tableWidget_2, self, self.showEditProgram, self.deleteProgram)

    def showEditCollege(self, row_idx=None, tableWidget=None):
        if tableWidget is None:
            tableWidget = None  

        if row_idx is None:
            row_idx = tableWidget.currentRow()

        if row_idx < 0:
            from controllers.CustomDialog import CustomDialog  
            dialog = CustomDialog("Error", "Please select a college to edit.")
            dialog.exec()
            return

        college_code = tableWidget.item(row_idx, 0).text()

        dlg = EditCollegeForm(self, originalCode=college_code)  
        if dlg.exec():  
            from views.college_view import loadColleges
            loadColleges(self.ui.tableWidget_3, self, self.showEditCollege, self.deleteCollege)

    def deleteStudent(self, row_idx, tableWidget):
        student_id = tableWidget.item(row_idx, 0).text()

        confirm = ConfirmDialog(
            title="Confirm Delete",
            message=f"Are you sure you want to delete student '{student_id}'?",
            parent=self
            ).exec()  

        if not confirm:
            return

        if deleteStudentbyID(student_id):
         
            CustomDialog("Deleted", f"Student '{student_id}' successfully removed.", parent=self).exec()
            
            loadStudents(self.ui.tableWidget, self.showEditStudent, self.deleteStudent)
        else:
            CustomDialog("Error", f"Could not delete student '{student_id}'. Please try again.", parent=self).exec()

    def deleteProgram(self, row_idx, tableWidget):
        program_code = tableWidget.item(row_idx, 0).text()

        confirm = ConfirmDialog(
            title="Confirm Delete",
            message=f"Are you sure you want to delete program '{program_code}'?",
            parent=self
            ).exec()
        
        if not confirm:
            return
        
        if deleteProgrambyID(program_code):
            CustomDialog("Deleted", f"Program '{program_code}' successfully removed.", parent=self).exec()
            loadPrograms(self.ui.tableWidget_2, self.showEditProgram, self.deleteProgram)
            loadStudents(self.ui.tableWidget, self.showEditStudent, self.deleteStudent)
        else:
            CustomDialog("Error", f"Could not delete program '{program_code}'. Please try again.", parent=self).exec()

    def deleteCollege(self, row_idx, tableWidget):
        college_code = tableWidget.item(row_idx, 0).text()

        confirm = ConfirmDialog(
            title="Confirm Delete",
            message=f"Are you sure you want to delete college '{college_code}'?",
            parent=self
            ).exec()
        
        if not confirm:
            return
        
        if deleteCollegebyID(college_code):
            CustomDialog("Deleted", f"College '{college_code}' successfully removed.", parent=self).exec()
            loadColleges(self.ui.tableWidget_3, self.showEditCollege, self.deleteCollege)
            loadPrograms(self.ui.tableWidget_2, self.showEditProgram, self.deleteProgram)
        else:
            CustomDialog("Error", f"Could not delete college '{college_code}'. Please try again.", parent=self).exec()
    
    def studentSort(self):
        columnName = self.ui.comboBox_2.currentText()
        ascending = self.ui.comboBox_3.currentText() == "Ascending"

        sortTable(self.ui.tableWidget, columnName, ascending)

    def programSort(self):
        
        columnName = self.ui.comboBox_4.currentText()  # Get selected column
        ascending = self.ui.comboBox_5.currentText() == "Ascending"  # Check sort order

        sortTable(self.ui.tableWidget_2, columnName, ascending)
    
    def collegeSort(self):
        
        columnName = self.ui.comboBox_7.currentText()  # Get selected column
        ascending = self.ui.comboBox_8.currentText() == "Ascending"  # Check sort order

        sortTable(self.ui.tableWidget_3, columnName, ascending)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())