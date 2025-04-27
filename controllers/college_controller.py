from config.db_config import getConnection
from views.addCollege_view import Ui_CollegeForm
from PyQt6.QtWidgets import QDialog
from controllers.CustomDialog import CustomDialog
from utils.validators import uniqueCollege, uniqueEditCollege

#Create
class AddCollegeForm(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.ui = Ui_CollegeForm()
        self.ui.setupUi(self)

        self.main_window = main_window

        # Connect Save button to save function
        self.ui.pushButton.clicked.connect(self.saveCollege)

    def saveCollege(self):
        collegeCode = self.ui.lineEdit.text()
        collegeName = self.ui.lineEdit_2.text()

        if not collegeCode or not collegeName:
            dialog = CustomDialog("Input Error", "Please fill in all required fields.")
            dialog.exec()
            return
        
        err = uniqueCollege(collegeCode)
        if err:

            CustomDialog("Validation Error", err).exec()
            return
        
        try:
            addCollege((collegeCode, collegeName))
            dialog = CustomDialog("Success", "College added successfully.")
            dialog.exec()
            self.close()
        except Exception as e:
            dialog = CustomDialog("Error", f"Failed to add college: {e}")
            dialog.exec()

        from views.college_view import loadColleges
        loadColleges(self.main_window.ui.tableWidget_3, self.main_window.showEditCollege, self.main_window.deleteCollege)

def addCollege(college):
    err = uniqueCollege(college[0])
    if err:
        raise ValueError(err)

    conn = getConnection()
    cursor = conn.cursor()

    sql = """ 
    INSERT INTO college (collegeCode, collegeName) VALUES (%s, %s)
    """
    cursor.execute(sql, college)
    conn.commit()
    cursor.close()
    conn.close()

class EditCollegeForm(QDialog):
    def __init__(self, main_window, originalCode):
        super().__init__(main_window)
        self.ui = Ui_CollegeForm()
        self.ui.setupUi(self)
        self.originalCode = originalCode
        self.main_window = main_window

        # Load existing college data
        data = getCollegeByCode(originalCode)
        if not data:
            dialog = CustomDialog("Error", "College not found.")
            dialog.exec()
            return
        
        self.ui.lineEdit.setText(data[0])
        self.ui.lineEdit_2.setText(data[1])

        # Connect Save button to save function
        self.ui.pushButton.clicked.connect(self.saveCollege)
        
    def saveCollege(self):
        collegeCode = self.ui.lineEdit.text()
        collegeName = self.ui.lineEdit_2.text()
            
        err = uniqueEditCollege(collegeCode, self.originalCode)
        if err:
            dialog = CustomDialog("Validation Error", err)
            dialog.exec()
            return
            
        if not collegeCode or not collegeName:
            dialog = CustomDialog("Input Error", "Please fill in all required fields.")
            dialog.exec()
            return
            
        data = {
            "collegeCode": collegeCode,
            "collegeName": collegeName
        }

        try:
            updateCollege(self.originalCode, data)
            dialog = CustomDialog("Success", "College updated successfully.")
            dialog.exec()
            self.close()

        except Exception as e:
            dialog = CustomDialog("Error", f"Failed to update college: {e}")
            dialog.exec()

        from views.college_view import loadColleges
        from views.program_view import loadPrograms
        loadColleges(self.main_window.ui.tableWidget_3, self.main_window.showEditCollege, self.main_window.deleteCollege)
        loadPrograms(self.main_window.ui.tableWidget_2, self.main_window.showEditProgram, self.main_window.deleteProgram)

#Update
def updateCollege(ogcollegeCode, updatedData):
    try:
        conn = getConnection()
        cursor = conn.cursor()

        sql = """
        UPDATE college
        SET collegeCode = %s, collegeName = %s
        WHERE collegeCode = %s
        """
        values = (
            updatedData["collegeCode"],
            updatedData["collegeName"],
            ogcollegeCode
        )

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[updateCollege] Error: {e}")
        return False

#Delete
def deleteCollegebyID(collegeCode):
    try:
        conn = getConnection()
        cursor = conn.cursor()

        sql = "DELETE FROM college WHERE collegeCode = %s"
        cursor.execute(sql, (collegeCode,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[deleteCollegebyID] Error: {e}")
        return False

#List
def getAllColleges():
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM college")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#Populate Combobox
def getCollegeCodes():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT collegeCode FROM college"
        cursor.execute(sql)
        colleges = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return colleges
    except Exception as e:
        print(f"[getCollegeCodes] Error: {e}")
        return []
    
def getCollegeByCode(college_code: str) -> dict | None:
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT collegeCode AS collegeCode,
                   collegeName AS collegeName
            FROM college
            WHERE collegeCode = %s
        """, (college_code,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Exception as e:
        print(f"[getCollegeByCode] Error: {e}")
        return None