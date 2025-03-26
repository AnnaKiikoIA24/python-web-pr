import psycopg2 
from conn import *
from app import app
from fastapi import Depends, Query, Body, status 
from fastapi.responses import JSONResponse

# ---------------------------------------------------
@app.get("/api/rating") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_ratings(idLesson: int = Query(default = None), conn: psycopg2.connect = Depends(get_db)): 
    """
    рейтинг студентів (idLesson != None => на заданому занятті)
    \nякщо заняття не задане, повертаємо перелік всіх рейтингів по всіх заняттях
    """
    cursor = conn.cursor()  
    ratings = []
    if (idLesson == None):
        # отримуємо список усіх об'єктів Raiting
        sql = "SELECT rating_id, id_lesson, id_student, is_presence, grade FROM ratings"
        cursor.execute(sql)
        
        for id, idLesson_, idStudent, isPresence, grade in cursor.fetchall(): 
            ratings.append({ 
                "id": id, 
                "idLesson": idLesson_,
                "idStudent": idStudent,
                "isPresence": isPresence,
                "grade": grade })
        cursor.close()  
        return ratings          
    
    # якщо заняття задане, то тільки перелік рейтингу студентів на занятті
    # отримуємо список об'єктів Rating, поєднуючи дані таблиць рейтингу та користувачів
    sql = f"""SELECT r.rating_id, r.id_lesson, r.id_student, u.first_name, u.last_name, r.is_presence, r.grade 
        FROM ratings r, users u
        WHERE r.id_student = u.user_id
        AND r.id_lesson = {idLesson}
        ORDER BY u.last_name"""
    cursor.execute(sql)
    
    for id, idLesson_, idStudent, firstName, lastName, isPresence, grade in cursor.fetchall(): 
        ratings.append({ 
            "id": id, 
            "idLesson": idLesson_,
            "idStudent": idStudent,
            "firstName": firstName,
            "lastName": lastName,
            "isPresence": isPresence,
            "grade": grade })
    cursor.close()  
    return ratings          

# ---------------------------------------------------
@app.get("/api/rating/{id}") 
def get_rating(id: int, conn: psycopg2.connect = Depends(get_db)):
    """
    рядок рейтингу за заданим id
    """
    cursor = conn.cursor()  
    # отримуємо заняття за id 
    sql = f"SELECT rating_id, id_lesson, id_student, is_presence, grade FROM ratings WHERE rating_id={id}"
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()

    # якщо рядок рейтингу не знайдено, відправляємо статусний код і повідомлення про помилку 
    if row == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Рядок рейтингу не знайдений"}) 
    
    #якщо рядок рейтингу знайдено, відправляємо його 
    id, idLesson, idStudent, isPresence, grade = row
    return { 
        "id": id, 
        "idLesson": idLesson,
        "idStudent": idStudent,
        "isPresence": isPresence,
        "grade": grade }

# ---------------------------------------------------
@app.get("/api/rating/student/{idStudent}/{idJournal}/{idSubject}") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_ratings_student(idStudent: int, idJournal: int, idSubject: int, conn: psycopg2.connect = Depends(get_db)):
    """
    рейтинг студента за заданим id студента, журнала, навчального предмета
    """
    cursor = conn.cursor()  
    # отримуємо список об'єктів Rating, поєднуючи дані таблиць рейтингу та користувачів
    sql = f"""SELECT l.date_lesson, l.theme, l.max_grade, u.first_name, u.last_name, r.rating_id, r.id_lesson, r.is_presence, r.grade 
        FROM lessons l, ratings r, users u 
        WHERE l.lesson_id = r.id_lesson
            AND u.user_id = l.id_teacher
            AND l.id_subject = {idSubject}
            AND l.id_journal = {idJournal}
            AND r.id_student = {idStudent}
        ORDER BY l.date_lesson"""
    cursor.execute(sql)
    
    ratings = []
    for dateLesson, theme, maxGrade, firstName, lastName, id, idLesson, isPresence, grade in cursor.fetchall(): 
        ratings.append({ 
            "dateLesson": dateLesson, 
            "theme": theme,
            "maxGrade": maxGrade,
            "firstName": firstName,
            "lastName": lastName,            
            "id": id,
            "idLesson": idLesson,
            "isPresence": isPresence,
            "grade": grade })
    cursor.close()  
    return ratings 

# ---------------------------------------------------    
@app.post("/api/rating") 
def create_rating(data = Body(), conn: psycopg2.connect = Depends(get_db)): 
    """
    створення нового рейтингу за списком рядків
    """
    cursor = conn.cursor()  
    ratings = []
    # створюємо масив кортежів
    for item in data:
        ratings.append((item["idLesson"], item["idStudent"], item["isPresence"], item["grade"]))
    
    sql = """INSERT INTO ratings(
        id_lesson, id_student, is_presence, grade)
        VALUES (%s, %s, %s, %s)"""
    # множинне додавання рядків
    cursor.executemany(sql, ratings)
    conn.commit() 
    cursor.close()  
    return      
 
# ---------------------------------------------------   
@app.put("/api/rating") 
def edit_rating(data  = Body(), conn: psycopg2.connect = Depends(get_db)): 
    """
    зміна даних за списком рядків рейтингу
    """
    cursor = conn.cursor()  
    ratings = []
    for item in data:
        ratings.append((item["idLesson"], item["idStudent"], item["isPresence"], item["grade"], item["id"]))
    
    sql = """UPDATE public.ratings
        SET id_lesson = %s, id_student = %s, is_presence = %s, grade = %s
        WHERE rating_id = %s"""
    # множинне оновлення рядків
    cursor.executemany(sql, ratings)
    conn.commit() 
    cursor.close()  
    return     
   
# ---------------------------------------------------   
@app.delete("/api/rating") 
def delete_rating(data = Body(), conn: psycopg2.connect = Depends(get_db)): 
    """
    видалення рядків рейтингу за списком
    """
    cursor = conn.cursor()  
    ratings = []
    for item in data:
        ratings.append((item["id"], ))
    
    sql = "DELETE FROM public.ratings WHERE rating_id = %s"
    # множинне видалення рядків
    cursor.executemany(sql, ratings)
    conn.commit() 
    cursor.close()  
    return  
