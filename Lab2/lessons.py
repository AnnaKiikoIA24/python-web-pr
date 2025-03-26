import psycopg2 
from conn import *
from app import app
from fastapi import Depends, Body, status 
from fastapi.responses import JSONResponse
from datetime import date

# ---------------------------------------------------
# перелік занять
@app.get("/api/lessons") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_lessons(conn: psycopg2.connect = Depends(get_db)): 
    """
    перелік занять
    """
    cursor = conn.cursor()  
    # Отримуємо список всіх занять
    sql = """SELECT l.lesson_id, l.id_subject, l.id_teacher, l.date_lesson, l.id_journal, l.theme, l.max_grade 
            FROM lessons l"""
    cursor.execute(sql)
    lessons = []
    for id, idSubject, idTeacher, dateLesson, idJournal, theme, maxGrade in cursor.fetchall(): 
        lessons.append({ 
            "id": id, 
            "idSubject": idSubject,
            "idTeacher": idTeacher,
            "dateLesson": dateLesson,
            "idJournal": idJournal,
            "theme": theme,
            "maxGrade": maxGrade})
    cursor.close()
    return lessons

# ---------------------------------------------------
# заняття за заданим id
@app.get("/api/lessons/{id}") 
def get_lesson(id: int, conn: psycopg2.connect = Depends(get_db)):
    """
    заняття за заданим id
    """
    cursor = conn.cursor()
    # отримуємо заняття за id 
    sql = f"""SELECT l.lesson_id, l.id_subject, l.id_teacher, l.date_lesson, l.id_journal, l.theme, l.max_grade 
        FROM lessons l
        WHERE l.lesson_id = {id}"""
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()

    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if row == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    
    #якщо заняття знайдено, відправляємо його 
    id, idSubject, idTeacher, dateLesson, idJournal, theme, maxGrade = row
    return { "id": id,
            "idSubject": idSubject,
            "idTeacher": idTeacher,
            "dateLesson": dateLesson,
            "idJournal": idJournal,
            "theme": theme,
            "maxGrade": maxGrade }

# ---------------------------------------------------   
# створення нового заняття 
@app.post("/api/lessons") 
def create_lesson(idSubject: int = Body(embed=True),
                idTeacher: int = Body(embed=True),
                dateLesson: date = Body(embed=True),
                idJournal: int = Body(embed=True),
                theme: str = Body(embed=True),
                maxGrade = Body(default = None, embed=True),
                conn: psycopg2.connect = Depends(get_db)): 
    """
    створення нового заняття
    """    
    cursor = conn.cursor()
    sql = """INSERT INTO lessons(
	        id_subject, id_teacher, date_lesson, id_journal, theme, max_grade)
            VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (idSubject, idTeacher, dateLesson, idJournal, theme, None if maxGrade == "" else maxGrade))
    conn.commit()

    # отримуємо поточне значення user_id з відповідної послідовності
    sql = """SELECT currval('lessons_lesson_id_seq')"""
    cursor.execute(sql)
    id, = cursor.fetchone()  
    cursor.close()

    return { "id": id, 
            "idSubject": idSubject,
            "idTeacher": idTeacher,
            "dateLesson": dateLesson,
            "idJournal": idJournal,
            "theme":  theme,
            "maxGrade": maxGrade }

# ---------------------------------------------------   
# пошук заняття за заданими параметрами
@app.post("/api/lessons/find") 
def find_lesson(data  = Body(), conn: psycopg2.connect = Depends(get_db)): 
    """
    пошук заняття за заданими параметрами
    """
    cursor = conn.cursor() 
    sql = """SELECT lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade
            FROM lessons
            WHERE id_journal = %s AND id_subject = %s AND id_teacher = %s AND date_lesson = %s"""
    cursor.execute(sql, (data["idJournal"], data["idSubject"], data["idTeacher"], data["dateLesson"]))
    row = cursor.fetchone()
    cursor.close()

    # якщо не заняття за обраними критеріями не знайдено, відправляємо статусний код і повідомлення про помилку 
    if row == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    id, idSubject, idTeacher, dateLesson, idJournal, theme, maxGrade = row
    #якщо заняття знайдено, відправляємо його 
    return { "id": id, 
            "idSubject": idSubject, 
            "idTeacher": idTeacher, 
            "dateLesson": dateLesson, 
            "idJournal": idJournal, 
            "theme": theme, 
            "maxGrade": maxGrade }
   
# ---------------------------------------------------   
# зміна даних про заняття
@app.put("/api/lessons") 
def edit_lesson(id: int = Body(embed=True),
                idSubject: int = Body(embed=True),
                idTeacher: int = Body(embed=True),
                dateLesson: date = Body(embed=True),
                idJournal: int = Body(embed=True),
                theme: str = Body(embed=True),
                maxGrade = Body(default = None, embed=True),
                conn: psycopg2.connect = Depends(get_db)):
    """
    зміна даних про заняття
    """    
    cursor = conn.cursor()
    # отримуємо заняття за id 
    sql = f"SELECT lesson_id FROM lessons WHERE lesson_id = {id}"
    cursor.execute(sql)
    row = cursor.fetchone()
   
    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if row == None:  
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    # якщо заняття знайдено, змінюємо його дані і відправляємо назад клієнту 
    sql = """UPDATE lessons
	SET id_subject = %s, id_teacher = %s, date_lesson = %s, id_journal = %s, theme = %s, max_grade = %s
	WHERE lesson_id = %s"""

    cursor.execute(sql, (idSubject, idTeacher, dateLesson, idJournal, theme, None if maxGrade == "" else maxGrade, id))
    conn.commit()
    cursor.close()

    return { "id": id, 
            "idSubject": idSubject, 
            "idTeacher": idTeacher, 
            "dateLesson": dateLesson, 
            "idJournal": idJournal, 
            "theme": theme, 
            "maxGrade": maxGrade }
   
# ---------------------------------------------------   
# видалення заняття
@app.delete("/api/lessons/{id}") 
def delete_lesson(id: int, conn: psycopg2.connect = Depends(get_db)): 
    """
    видалення заняття
    """
    cursor = conn.cursor()
    # отримуємо заняття за id 
    sql = f"SELECT lesson_id FROM lessons WHERE lesson_id = {id}"
    cursor.execute(sql)
    row = cursor.fetchone()
   
    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if row == None:  
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    
    # якщо заняття знайдено, видаляємо його 
    sql = f"DELETE FROM public.lessons WHERE lesson_id = {id}"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    return