import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from views.mainui import Ui_MainWindow
from views.student_view import loadStudents
from views.program_view import loadPrograms
from views.college_view import loadColleges
from controllers.student_controller import AddStudentForm
from controllers.program_controller import AddProgramForm
from controllers.college_controller import AddCollegeForm

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

        #Add button for Student page
        self.ui.pushButton.clicked.connect(self.show_addStudent)

        #Add button for Program page
        self.ui.pushButton_11.clicked.connect(self.show_addProgram)

        #Add button for College page   
        self.ui.pushButton_12.clicked.connect(self.show_addCollege)

        # Load tables with MySQL data
        if hasattr(self.ui, 'tableWidget'):
            loadStudents(self.ui.tableWidget)  # Pass tableWidget to function

        if hasattr(self.ui, 'tableWidget_2'):  # Assuming tableWidget_2 is on page 2
            loadPrograms(self.ui.tableWidget_2) 

        if hasattr(self.ui, 'tableWidget_3'):  # Assuming tableWidget_2 is on page 2
            loadColleges(self.ui.tableWidget_3) 

    def show_addStudent(self):
        self.addStudentWindow = AddStudentForm(self)
        self.addStudentWindow.show()
        if self.addStudentWindow.exec():
            loadStudents(self.ui.tableWidget)

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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())