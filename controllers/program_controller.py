from config.db_config import getConnection
from views.addProgram_view import Ui_ProgramForm
from PyQt6.QtWidgets import QDialog
from controllers.CustomDialog import CustomDialog
from controllers.college_controller import getCollegeCodes
from utils.validators import uniqueProgram

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
        loadPrograms(self.main_window.ui.tableWidget_2)


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

#Update
def updateProgram(programCode, updatedData):
    try:
        conn = getConnection()
        cursor = conn.cursor()

        sql = """
        UPDATE program
        SET name = %s, college_code = %s
        WHERE code = %s
        """
        values = (
            updatedData["Program Name"],
            updatedData["College Code"],
            programCode
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
def deleteProgram(programCode):
    try:
        conn, cursor = getConnection()
        sql = "DELETE FROM program WHERE code = %s"
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