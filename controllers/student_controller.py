from config.db_config import getConnection
from views.addStudent_view import Ui_Form
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from controllers.program_controller import getProgramCodes
from controllers.CustomDialog import CustomDialog
from utils.validators import uniqueStudent


#Create
class AddStudentForm(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.main_window = main_window
        self.populatePrograms()

        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.lineEdit_3.setValidator(id_validator)  # Apply the validator to ID field
        
        # Connect Save button to save function
        self.ui.pushButton.clicked.connect(self.saveStudent)

    def populatePrograms(self):
        programCode = getProgramCodes()
        self.ui.comboBox_4.addItems(programCode)

    def saveStudent(self):
        """Collects student data and saves it to a CSV file."""
        # Get user inputs
        firstName = self.ui.lineEdit.text().strip()
        lastName = self.ui.lineEdit_2.text().strip()
        studentid = self.ui.lineEdit_3.text().strip()
        

        # Input validation
        if not studentid:
            dialog = CustomDialog("Input Error", "Student ID is required.")
            dialog.exec()
            return
        
        err = uniqueStudent(studentid)
        if err:
            CustomDialog("Validation Error", err).exec()
            return
        
        if not self.ui.lineEdit_3.hasAcceptableInput():
            dialog = CustomDialog("Input Error", "Invalid ID format! Use XXXX-XXXX.")
            dialog.exec()
            return
        
        yearLevel = self.ui.comboBox.currentText()
        gender = self.ui.comboBox_2.currentText()
        programCode = self.ui.comboBox_4.currentText()

        if not firstName or not lastName or not studentid or not yearLevel or not gender or not programCode:
            dialog = CustomDialog("Input Error", "Please fill in all required fields.")
            dialog.exec()
            return
        
        try:
            addStudent((studentid, firstName, lastName, yearLevel, gender, programCode))

            dialog = CustomDialog("Success", "Student added successfully!")
            dialog.exec()


            self.close()
        except Exception as e:
            dialog = CustomDialog("Error", f"An error occurred:\n{e}")
            dialog.exec()

        from views.student_view import loadStudents
        loadStudents(self.main_window.ui.tableWidget)

def addStudent(student):
    err = uniqueStudent(student[0])
    if err:
        raise ValueError(err)
    
    conn = getConnection()
    cursor = conn.cursor()

    sql = """ 
INSERT INTO student (studentID, firstName, lastName, yearLevel, gender, programCode) 
VALUES (%s, %s, %s, %s, %s, %s)
"""
    cursor.execute(sql, student)
    conn.commit()
    cursor.close()
    conn.close()


#Update
def updateStudent(studentID, updatedData):
    try:
        conn, cursor = getConnection()
        

        sql = """
        UPDATE student
        SET first_name = %s, last_name = %s, year_level = %s, gender = %s, program_code = %s
        WHERE id = %s
        """
        values = (
            updatedData["First Name"],
            updatedData["Last Name"],
            updatedData["Year Level"],
            updatedData["Gender"],
            updatedData["Program Code"],
            studentID
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[updateStudentById] Error: {e}")
        return False

#Delete
def deleteStudent(studentID):
    try:
        conn, cursor = getConnection()
        sql = "DELETE FROM student WHERE id = %s"
        cursor.execute(sql, (studentID,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[deleteStudentByID] Error: {e}")
        return False
    
#List
def getAllStudents():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows