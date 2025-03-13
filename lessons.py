from db import *
from app import app
from sqlalchemy import and_
from sqlalchemy.orm import Session 
from fastapi import Depends, Body, status 
from fastapi.responses import JSONResponse
from datetime import date

# ---------------------------------------------------
@app.get("/api/lessons") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_lessons(db: Session = Depends(get_db)): 
    """
    перелік занять
    """
    # отримуємо  список  об'єктів Lesson
    return db.query(Lesson).all() 

# ---------------------------------------------------
@app.get("/api/lessons/{id}") 
def get_lesson(id: int, db: Session = Depends(get_db)): 
    """
    заняття за заданим id
    """
    # отримуємо заняття за id 
    lesson = db.query(Lesson).filter(Lesson.id == id).first() 
    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if lesson == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    #якщо заняття знайдено, відправляємо його 
    return lesson

# ---------------------------------------------------    
@app.post("/api/lessons")
def create_lesson(idSubject: int = Body(embed=True),
                  idTeacher: int = Body(embed=True),
                  dateLesson: date = Body(embed=True),
                  idJournal: int = Body(embed=True),
                  theme: str = Body(embed=True),
                  maxGrade: int = Body(default = None, embed=True),
                  db: Session = Depends(get_db)):
    """
    створення нового заняття
    """
    lesson = Lesson(
        idSubject = idSubject, 
        idTeacher = idTeacher,
        dateLesson = dateLesson,
        idJournal = idJournal,
        theme = theme,
        maxGrade = maxGrade)
    db.add(lesson) 
    db.commit() 
    db.refresh(lesson) 
    return lesson 

# ---------------------------------------------------   
@app.post("/api/lessons/find") 
def find_lesson(data  = Body(), db: Session = Depends(get_db)):
    """
    пошук заняття за заданими параметрами
    """
    lesson = db.query(Lesson).filter(and_(Lesson.idJournal == data["idJournal"], Lesson.idSubject == data["idSubject"], Lesson.idTeacher == data["idTeacher"], Lesson.dateLesson == data["dateLesson"])).first()
    # якщо не заняття за обраними критеріями не знайдено, відправляємо статусний код і повідомлення про помилку 
    if lesson == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    #якщо заняття знайдено, відправляємо його 
    return lesson
   
# ---------------------------------------------------   
@app.put("/api/lessons") 
def edit_lesson(id: int = Body(embed=True),
                idSubject: int = Body(embed=True),
                idTeacher: int = Body(embed=True),
                dateLesson: date = Body(embed=True),
                idJournal: int = Body(embed=True),
                theme: str = Body(embed=True),
                maxGrade: int = Body(default = None, embed=True),
                db: Session = Depends(get_db)):
    """
    зміна даних про заняття
    """
    # отримуємо заняття за id 
    lesson = db.query(Lesson).filter(Lesson.id == id).first() 
    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if lesson == None:  
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    # якщо заняття знайдено, змінюємо його дані і відправляємо назад клієнту 
    lesson.idSubject = idSubject
    lesson.idTeacher = idTeacher
    lesson.dateLesson = dateLesson
    lesson.idJournal = idJournal
    lesson.theme = theme
    lesson.maxGrade = maxGrade

    db.commit() # зберігаємо зміни  
    db.refresh(lesson) 
    return lesson 
   
# ---------------------------------------------------   
@app.delete("/api/lessons/{id}") 
def delete_lesson(id, db: Session = Depends(get_db)):
    """
    видалення заняття
    """
    # отримуємо заняття за id 
    lesson = db.query(Lesson).filter(Lesson.id == id).first() 
    
    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if lesson == None: 
        return JSONResponse( status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    
    # якщо заняття знайдено, видаляємо його 
    db.delete(lesson)  # видаляємо об'єкт 
    db.commit()     # зберігаємо зміни 
    return lesson 