from config.db_config import getConnection
from views.addStudent_view import Ui_Form
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from controllers.program_controller import getProgramCodes
from controllers.CustomDialog import CustomDialog
from utils.validators import uniqueStudent, uniqueEditStudent


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
        loadStudents(self.main_window.ui.tableWidget, self, self)  

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

class EditStudentForm(QDialog):
    def __init__(self, main_window, originalID):
        super().__init__(main_window)
        self.originalID = originalID
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.main_window = main_window
        self.populatePrograms()

        id_validator = QRegularExpressionValidator(QRegularExpression(r"^\d{4}-\d{4}$"))
        self.ui.lineEdit_3.setValidator(id_validator)

        # Load existing student data
        data = getStudentById(originalID)
        if not data:
            # show error and close
            dialog = CustomDialog("Input Error", "No student found with ID {originalID}.")
            dialog.exec()
            return

        # 2) populate the fields
        self.ui.lineEdit_3.setText(data["studentID"])
        self.ui.lineEdit.setText(data["firstName"])
        self.ui.lineEdit_2.setText(data["lastName"])
        self.ui.comboBox.setCurrentText(str(data["yearLevel"]))
        self.ui.comboBox_2.setCurrentText(data["gender"])
        self.ui.comboBox_4.setCurrentText(data["programCode"])

        # Connect Save button to save function
        self.ui.pushButton.clicked.connect(self.saveStudent)

    def populatePrograms(self):
        programCode = getProgramCodes()
        self.ui.comboBox_4.addItems(programCode)

    def saveStudent(self):
        firstName = self.ui.lineEdit.text().strip()
        lastName = self.ui.lineEdit_2.text().strip()
        studentid = self.ui.lineEdit_3.text().strip()

        if not studentid:
            dialog = CustomDialog("Input Error", "Student ID is required.")
            dialog.exec()
            return
        
        err = uniqueEditStudent(studentid, self.originalID)
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
        
        data = {
            "studentID": studentid,
            "firstName": firstName,
            "lastName": lastName,
            "yearLevel": yearLevel,
            "gender": gender,
            "programCode": programCode
        }

        try:
            updateStudent(self.originalID, data)

            dialog = CustomDialog("Success", "Student updated successfully!")
            dialog.exec()

            self.close()
        except Exception as e:
            dialog = CustomDialog("Error", f"An error occurred:\n{e}")
            dialog.exec()
        
        from views.student_view import loadStudents
        loadStudents(self.main_window.ui.tableWidget, self.main_window.showEditStudent, self.main_window.deleteStudent)

#Update
def updateStudent(ogstudentID, updatedData):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        

        sql = """
        UPDATE student
        SET studentID = %s, firstName = %s, lastName = %s, yearLevel = %s, gender = %s, programCode = %s
        WHERE studentID = %s
        """
        values = (
            updatedData["studentID"],
            updatedData["firstName"],
            updatedData["lastName"],
            updatedData["yearLevel"],
            updatedData["gender"],
            updatedData["programCode"],
            ogstudentID
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
def deleteStudentbyID(studentID):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "DELETE FROM student WHERE studentID = %s"
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

def getStudentById(student_id: str) -> dict | None:
    try:
        conn = getConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT studentID    AS studentID,
                   firstName  AS firstName,
                   lastName   AS lastName,
                   yearLevel  AS yearLevel,
                   gender      AS gender,
                   programCode AS programCode
              FROM student
             WHERE studentID = %s
        """, (student_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row  # dict or None
    except Exception as e:
        print(f"[getStudentById] Error: {e}")
        return None
