from conn import *
from pymongo import MongoClient 
from app import app
from fastapi import Depends, Body, status 
from fastapi.responses import JSONResponse
from datetime import date, datetime
from bson import ObjectId

# ---------------------------------------------------
# перелік занять
@app.get("/api/lessons") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_lessons(db: MongoClient = Depends(get_db)): 
    """
    перелік занять
    """
    # # Отримуємо список всіх занять
    lessons = find_documents(db["lessons"], 
                             # умова: відсутня
                             {}, 
                             # проекція
                             {          
                                "dateLesson": 1,
                                "idJournal": "$journal.$id",
                                "idSubject": "$subject.$id",
                                "idTeacher": "$teacher.$id",
                                "theme": 1,
                                "maxGrade": 1                                  
                             }, 
                             # cортування
                             {"dateLesson": 1})

    result = []
    for r in lessons: 
        # конвертуємо ObjectId у строку
        r["id"] = str(r["id"])
        r["idTeacher"] = str(r["idTeacher"])
        result.append(r)
    # повертаємо масив об'єктів 
    return result

# ---------------------------------------------------
# заняття за заданим id
@app.get("/api/lessons/{id}") 
def get_lesson(id: str, db: MongoClient = Depends(get_db)):
    """
    заняття за заданим id
    """
    lesson = find_document(db["lessons"], 
                             # умова
                             { "_id": ObjectId(id) }, 
                             # проекція
                             {          
                                "dateLesson": 1,
                                "idJournal": "$journal.$id",
                                "idSubject": "$subject.$id",
                                "idTeacher": "$teacher.$id",
                                "theme": 1,
                                "maxGrade": 1                                  
                             })    

    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if lesson == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    
    #якщо заняття знайдено, відправляємо його 
    # конвертуємо ObjectId у строку
    lesson["id"] = str(lesson["id"])
    lesson["idTeacher"] = str(lesson["idTeacher"])
    return lesson

# ---------------------------------------------------   
# створення нового заняття 
@app.post("/api/lessons") 
def create_lesson(idSubject: int = Body(embed=True),
                idTeacher: str = Body(embed=True),
                dateLesson: date = Body(embed=True),
                idJournal: int = Body(embed=True),
                theme: str = Body(embed=True),
                maxGrade = Body(default = None, embed=True),
                db: MongoClient = Depends(get_db)): 
    """
    створення нового заняття
    """    
    newLesson = {
        "subject": { "$ref": "subjects", "$id": idSubject },
        "teacher": { "$ref": "users", "$id": ObjectId(idTeacher) },
        "journal": { "$ref": "journals", "$id": idJournal },
        "dateLesson": datetime.combine(dateLesson, datetime.min.time()),
        "theme": theme,
        "maxGrade":  None if maxGrade == "" else maxGrade
    }
    newId = str(insert_document(db["lessons"], newLesson))

    return {
        "id": newId,
        "idSubject": idSubject,
        "idTeacher": idTeacher,
        "dateLesson": dateLesson,
        "theme": theme,
        "maxGrade":  maxGrade
    }

# ---------------------------------------------------   
# пошук заняття за заданими параметрами
@app.post("/api/lessons/find") 
def find_lesson(idSubject: int = Body(embed=True),
                idTeacher: str = Body(embed=True),
                dateLesson: date = Body(embed=True),
                db: MongoClient = Depends(get_db)): 
    """
    пошук заняття за заданими параметрами
    """
    lesson = find_document(db["lessons"], 
                             # умова
                             { 
                                "subject.$id": idSubject, 
                                "teacher.$id": ObjectId(idTeacher), 
                                "dateLesson": datetime.combine(dateLesson, datetime.min.time()) 
                             }, 
                             # проекція
                             {          
                                "dateLesson": 1,
                                "idJournal": "$journal.$id",
                                "idSubject": "$subject.$id",
                                "idTeacher": "$teacher.$id",
                                "theme": 1,
                                "maxGrade": 1                                  
                             })    

    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if lesson == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"}) 
    
    #якщо заняття знайдено, відправляємо його 
    # конвертуємо ObjectId у строку
    lesson["id"] = str(lesson["id"])
    lesson["idTeacher"] = str(lesson["idTeacher"])
    return lesson
   
# ---------------------------------------------------   
# зміна даних про заняття
@app.put("/api/lessons") 
def edit_lesson(id: str = Body(embed=True),
                idSubject: int = Body(embed=True),
                idTeacher: str = Body(embed=True),
                dateLesson: date = Body(embed=True),
                idJournal: int = Body(embed=True),
                theme: str = Body(embed=True),
                maxGrade = Body(default = None, embed=True),
                db: MongoClient = Depends(get_db)):
    """
    зміна даних про заняття
    """    
    lesson = find_document(db["lessons"], {'_id': ObjectId(id)})  
 
    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if lesson == None:  
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"})  
    
    # якщо заняття знайдено, змінюємо його дані і відправляємо назад клієнту 
    updatedLesson = {
        "subject": { "$ref": "subjects", "$id": idSubject },
        "teacher": { "$ref": "users", "$id": ObjectId(idTeacher) },
        "journal": { "$ref": "journals", "$id": idJournal },
        "dateLesson": datetime.combine(dateLesson, datetime.min.time()),
        "theme": theme,
        "maxGrade":  None if maxGrade == "" else maxGrade
    }
    update_document(db["lessons"],  { '_id': ObjectId(id) }, updatedLesson)

    return {
        "id": id,
        "idSubject": idSubject,
        "idTeacher": idTeacher,
        "dateLesson": dateLesson,
        "theme": theme,
        "maxGrade": maxGrade        
    }       
   
# ---------------------------------------------------   
# видалення заняття
@app.delete("/api/lessons/{id}") 
def delete_lesson(id: str, db: MongoClient = Depends(get_db)): 
    """
    видалення заняття
    """
    lesson = find_document(db["lessons"], {'_id': ObjectId(id)})  
 
    # якщо не знайдено, відправляємо статусний код і повідомлення про помилку 
    if lesson == None:  
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Заняття не знайдено"})     
    
    delete_document(db["lessons"], {'_id': ObjectId(id)})    
    return