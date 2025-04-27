from config.db_config import getConnection
from views.addCollege_view import Ui_CollegeForm
from PyQt6.QtWidgets import QDialog
from controllers.CustomDialog import CustomDialog
from utils.validators import uniqueCollege

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
        loadColleges(self.main_window.ui.tableWidget_3)

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