from config.db_config import getConnection
from views.addProgram_view import Ui_ProgramForm
from PyQt6.QtWidgets import QDialog
from controllers.CustomDialog import CustomDialog
from controllers.college_controller import getCollegeCodes
from utils.validators import uniqueProgram, uniqueEditProgram

#Create
class AddProgramForm(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.ui = Ui_ProgramForm()
        self.ui.setupUi(self)

        self.main_window = main_window
        self.populateColleges()

        # Connect Save button to save function
        self.ui.pushButton.clicked.connect(self.saveProgram)

    def populateColleges(self):
        collegeCode = getCollegeCodes()
        self.ui.comboBox.addItems(collegeCode)

    def saveProgram(self):
        collegeCode = self.ui.comboBox.currentText()
        programCode = self.ui.lineEdit_2.text()
        programName = self.ui.lineEdit_3.text()

        err = uniqueProgram(programCode)
        if err:
            CustomDialog("Validation Error", err).exec()
            return

        if not collegeCode or not programCode or not programName:
            dialog = CustomDialog("Input Error", "Please fill in all required fields.")
            dialog.exec()
            return
        
        try:
            addProgram((programCode, programName, collegeCode))
            dialog = CustomDialog("Success", "Program added successfully.")
            dialog.exec()
            self.close()
        except Exception as e:
            dialog = CustomDialog("Error", f"Failed to add program: {e}")
            dialog.exec()

        from views.program_view import loadPrograms
        loadPrograms(self.main_window.ui.tableWidget_2, self.main_window.showEditProgram, self.main_window.deleteProgram)

def addProgram(program):
    err = uniqueProgram(program[0])
    if err:
        raise ValueError(err)

    conn = getConnection()
    cursor = conn.cursor()

    sql = """ 
    INSERT INTO program (programCode, programName, collegeCode) VALUES (%s, %s, %s)
    """
    cursor.execute(sql, program)
    conn.commit()
    cursor.close()
    conn.close()

class EditProgramForm(QDialog):
    def __init__(self, main_window, originalCode):
        super().__init__(main_window)
        self.ui = Ui_ProgramForm()
        self.ui.setupUi(self)

        self.main_window = main_window
        self.originalCode = originalCode

        self.populateColleges()

        # Load existing program data
        data = getProgramByCode(originalCode)
        if not data:
            dialog = CustomDialog("Error", "Program not found.")
            dialog.exec()
            return
        
        self.ui.lineEdit_2.setText(data["programCode"])
        self.ui.lineEdit_3.setText(data["programName"])
        self.ui.comboBox.setCurrentText(data["collegeCode"])

        # Connect Save button to save function
        self.ui.pushButton.clicked.connect(self.saveProgram)

    def populateColleges(self):
        collegeCode = getCollegeCodes()
        self.ui.comboBox.addItems(collegeCode)

    def saveProgram(self):
        programCode = self.ui.lineEdit_2.text().strip()
        programName = self.ui.lineEdit_3.text().strip()
        collegeCode = self.ui.comboBox.currentText().strip()
        
        err = uniqueEditProgram(programCode, self.originalCode)
        if err:
            dialog = CustomDialog("Validation Error", err)
            dialog.exec()
            return

        if not collegeCode or not programCode or not programName:
            dialog = CustomDialog("Input Error", "Please fill in all required fields.")
            dialog.exec()
            return
        
        data = {
            "programCode": programCode,
            "programName": programName,
            "collegeCode": collegeCode
        }

        try:
            updateProgram(self.originalCode, data)
            dialog = CustomDialog("Success", "Program updated successfully.")
            dialog.exec()

            self.close()
        except Exception as e:
            dialog = CustomDialog("Error", f"Failed to update program: {e}")
            dialog.exec()

        from views.program_view import loadPrograms
        from views.student_view import loadStudents
        loadPrograms(self.main_window.ui.tableWidget_2, self.main_window.showEditProgram, self.main_window.deleteProgram)
        loadStudents(self.main_window.ui.tableWidget, self.main_window.showEditStudent, self.main_window.deleteStudent)
        
        
#Update
def updateProgram(ogprogramCode, updatedData):
    try:
        conn = getConnection()
        cursor = conn.cursor()

        sql = """
        UPDATE program
        SET programCode = %s, programName = %s, collegeCode = %s
        WHERE programCode = %s
        """
        values = (
            updatedData["programCode"],
            updatedData["programName"],
            updatedData["collegeCode"],
            ogprogramCode
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[updateProgramById] Error: {e}")
        return False
    
#Delete
def deleteProgrambyID(programCode):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "DELETE FROM program WHERE programCode = %s"
        cursor.execute(sql, (programCode,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[deleteProgramByID] Error: {e}")
        return False


#List
def getAllPrograms():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM program")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#For ComboBoxes
def getProgramCodes():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT programCode FROM program"
        cursor.execute(sql)
        programs = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return programs
    except Exception as e:
        print(f"[getProgramCodes] Error: {e}")
        return []
    
def getProgramByCode(program_code: str) -> dict | None:
    try:
        conn = getConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT programCode AS programCode,
                   programName AS programName,
                   collegeCode AS collegeCode
            FROM program
            WHERE programCode = %s
        """, (program_code,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        print(f"[getProgramByCode] Error: {e}")
        return None