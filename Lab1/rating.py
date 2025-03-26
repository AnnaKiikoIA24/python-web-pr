from db import *
from app import app
from sqlalchemy import select, and_
from sqlalchemy.orm import Session 
from fastapi import Depends, Query, Body, status 
from fastapi.responses import JSONResponse

# ---------------------------------------------------
@app.get("/api/rating") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_ratings(idLesson: int = Query(default = None), db: Session = Depends(get_db)): 
    """
    рейтинг студентів (idLesson != None => на заданому занятті)
    \nякщо заняття не задане, повертаємо перелік всіх рейтингів по всіх заняттях
    """
    if (idLesson == None):
        # отримуємо список усіх об'єктів Raiting
        return db.query(Rating).all() 
    # якщо заняття задане, то тільки перелік рейтингу студентів на занятті
    # отримуємо список об'єктів Rating, поєднуючи дані таблиць рейтингу та користувачів
    stmt  = select(Rating.id,
                   Rating.idLesson,
                   Rating.idStudent,
                   User.firstName,
                   User.lastName,
                   Rating.isPresence,
                   Rating.grade).join_from(Rating, User).where(Rating.idLesson == idLesson).order_by(User.lastName)
    print (stmt)
    return db.execute(stmt).mappings().all()

# ---------------------------------------------------
@app.get("/api/rating/{id}") 
def get_rating(id: int, db: Session = Depends(get_db)):
    """
    рядок рейтингу за заданим id
    """
    # отримуємо заняття за id 
    rating = db.query(Rating).filter(Rating.id == id).first() 
    # якщо рядок рейтингу не знайдено, відправляємо статусний код і повідомлення про помилку 
    if rating == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Рядок рейтингу не знайдений"}) 
    #якщо рядок рейтингу знайдено, відправляємо його 
    return rating

# ---------------------------------------------------
@app.get("/api/rating/student/{idStudent}/{idJournal}/{idSubject}") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_ratings_student(idStudent: int, idJournal: int, idSubject: int, db: Session = Depends(get_db)):
    """
    рейтинг студента за заданим id студента, журнала, навчального предмета
    """

    # отримуємо список об'єктів Rating, поєднуючи дані таблиць рейтингу та користувачів
    stmt  = select(Lesson.dateLesson,
                   Lesson.theme,
                   Lesson.maxGrade,
                   User.firstName,
                   User.lastName,
                   Rating.id,
                   Rating.idLesson,
                   Rating.isPresence,
                   Rating.grade).join(Rating, Rating.idLesson == Lesson.id).join(User, Lesson.idTeacher == User.id).where(and_(Lesson.idSubject == idSubject,
                                                                                                                               Lesson.idJournal == idJournal,
                                                                                                                               Rating.idStudent == idStudent)).order_by(Lesson.dateLesson)
    print (stmt)
    return db.execute(stmt).mappings().all()

# ---------------------------------------------------    
@app.post("/api/rating") 
def create_rating(data= Body(), db: Session = Depends(get_db)): 
    """
    створення нового рейтингу за списком рядків
    """
    for item in data:
        rating = Rating(
            idLesson = item["idLesson"], 
            idStudent = item["idStudent"],
            isPresence = item["isPresence"],
            grade = item["grade"])
        db.add(rating) 
    db.commit() 
 
# ---------------------------------------------------   
@app.put("/api/rating") 
def edit_rating(data  = Body(), db: Session = Depends(get_db)): 
    """
    зміна даних за списком рядків рейтингу
    """
    for item in data:
        # отримуємо рядок рейтингу за id 
        rating = db.query(Rating).filter(Rating.id == item["id"]).first() 
        # якщо рядок не знайдений, відправляємо статусний код і повідомлення про помилку 
        if rating == None:  
            return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Рядок рейтингу з id=" + item["id"] + " не знайдений"}) 
        # якщо рядок знайдений, змінюємо його дані 
        rating.idLesson = item["idLesson"]
        rating.idStudent = item["idStudent"]
        rating.isPresence = item["isPresence"]
        rating.grade = item["grade"]

    db.commit() # зберігаємо зміни  
    # db.refresh(lesson) 
    # return lesson 
   
# ---------------------------------------------------   
@app.delete("/api/rating") 
def delete_rating(data = Body(), db: Session = Depends(get_db)): 
    """
    видалення рядків рейтингу за списком
    """
    for item in data:
        # отримуємо рядок рейтингу за id 
        rating = db.query(Rating).filter(Rating.id == item["id"]).first() 
        # якщо рядок не знайдений, відправляємо статусний код і повідомлення про помилку 
        if rating == None:  
            return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Рядок рейтингу з id=" + item["id"] + " не знайдений"}) 
        # якщо рядок знайдений, змінюємо його дані 
        db.delete(rating)  # видаляємо об'єкт 
        
    db.commit() # зберігаємо зміни  
