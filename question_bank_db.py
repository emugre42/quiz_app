import sqlite3

def create():

    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Modules(
        ID INTEGER PRIMARY KEY AutoIncrement,
        Module VARCHAR(50),
        ModuleCategory VARCHAR(50),
        ModuleType VARCHAR(50)
        )""")

    cur.execute("""

        CREATE TABLE IF NOT EXISTS Questions(
        ID INTEGER PRIMARY KEY AutoIncrement,
        Question VARCHAR(50),
        Category VARCHAR(50),
        Type VARCHAR(50)

    ) """)

    cur.execute("""

        CREATE TABLE IF NOT EXISTS Answers(
        ID INTEGER PRIMARY KEY,
        Description VARCHAR(50),
        IsCorrect INTEGER,
        QuestionID VARCHAR(50),
        FOREIGN KEY(QuestionID) REFERENCES Answers(ID)

    ) """)

    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS Results(
            ID INTEGER PRIMARY KEY AutoIncrement,
            Result VARCHAR(50),
            Date DATE
        )""")

    con.commit()
    con.close()

def get_module():
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()  
    cur.execute("""
    SELECT  Module,
            ModuleCategory,
            ModuleType
            FROM Modules""")
    con.commit()
    results = cur.fetchall()
    con.close()
    return results

def insert_module(text, module_category, module_type):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()
    query = """
            INSERT INTO Results(
                Module
                ModuleCategory,
                ModuleType
            ) VALUES (
                ?,
                ?,
                ?
            )"""
    cur.execute(query, [text, module_category, module_type])
    con.commit()
    con.close()

def delete_module(text, module_category, module_type):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Results WHERE Module = ? AND ModuleCategory = ? AND ModuleType = ?", [text, module_category, module_type])
    con.commit()
    con.close()

def get_result():
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()  
    cur.execute("""
    SELECT  Result,
            Date
            FROM Results""")
    con.commit()
    results = cur.fetchall()
    con.close()
    return results

def insert_result(rslt,  result_date):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()
    query = """
            INSERT INTO Results(
                Result,
                Date
            ) VALUES (
                ?,
                ?
            )"""
    cur.execute(query, [rslt,  result_date])
    con.commit()
    con.close()

def delete_result(rslt, result_date):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Results WHERE Result = ? AND Date = ?", [rslt,  result_date])
    con.commit()
    con.close()

def insert_question(text, question_category, question_type):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()
    query = """
            INSERT INTO Questions(
                Question,
                Category,
                Type
            ) VALUES (
                ?,
                ?,
                ?
            )"""
    cur.execute(query, [text, question_category, question_type])
    con.commit()
    con.close()

def get_question():
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()  
    cur.execute("""
    SELECT  Question,
            Category,
            Type
            FROM Questions""")
    con.commit()
    results = cur.fetchall()
    con.close()
    return results

def delete_question(text, question_category, question_type):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()
    query = "DELETE FROM Questions WHERE Question = ? AND Category = ? AND Type = ?"
    cur.execute(query, [text, question_category, question_type]) 
    con.commit()
    con.close()

def insert_answer(answer_description, answer_is_correct, question_id):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()
    cur.execute("""INSERT INTO Answers
                    (
                    Description,
                    IsCorrect,
                    QuestionID
                    ) VALUES(
                        ?,
                        ?,
                        ?
                    )""", [answer_description, answer_is_correct, question_id])
    con.commit()
    con.close()

def get_answer():
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()  
    cur.execute("""
    SELECT  Description,
            IsCorrect,
            QuestionID
            FROM Answers""")
    con.commit()
    results = cur.fetchall()
    con.close()
    return results

def delete_answer(answer_description, answer_is_correct):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()
    query = "DELETE FROM Answers WHERE Description = ? AND IsCorrect = ?"
    print(query, answer_description, answer_is_correct)
    cur.execute(query, [answer_description, answer_is_correct])
    con.commit()
    con.close()

def get_id(text, question_category, question_type):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()  
    cur.execute("SELECT ID FROM Questions WHERE Question = ? AND Category = ? AND Type = ?", [text, question_category, question_type])
    result = cur.fetchone()
    con.commit()
    con.close()
    return result[0]

def get_answers(id):
    con = sqlite3.connect("question_bank.db")
    cur = con.cursor()  
    cur.execute("SELECT Description, IsCorrect FROM Answers WHERE QuestionID = ?", [id])
    result = cur.fetchall()
    con.commit()
    con.close()
    return result