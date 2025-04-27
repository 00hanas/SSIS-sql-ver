from config.db_config import getConnection

def _exists(table: str, column: str, value) -> bool:
    """
    Returns True if a row exists in `table` where `column` = value.
    """
    conn = getConnection()
    cursor = conn.cursor()
    sql = f"SELECT COUNT(*) FROM `{table}` WHERE `{column}` = %s"
    cursor.execute(sql, (value,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def is_unique_student_id(studentid):
    return not _exists("student", "studentID", studentid)

def is_unique_program_code(programCode):
    return not _exists("program", "programCode", programCode)

def is_unique_college_code(collegeCode):
    return not _exists("college", "collegeCode", collegeCode)

def uniqueStudent(studentid):
    """
    :param data: {"id": str, "first_name": str, ...}
    :returns: error message if invalid, otherwise None
    """
    if not is_unique_student_id(studentid):
        return f"Student ID {studentid} already exists."
    return None

def uniqueProgram(programCode):
    if not is_unique_program_code(programCode):
        return f"Program Code {programCode} already exists."
    # e.g. check that college_code exists, etc.
    return None

def uniqueCollege(collegeCode):
    if not is_unique_college_code(collegeCode):
        return f"College Code {collegeCode} already exists."
    return None
