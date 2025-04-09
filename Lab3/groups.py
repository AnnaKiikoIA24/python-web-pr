from conn import *
from pymongo import MongoClient 
from app import app
from fastapi import Depends, status
from fastapi.responses import JSONResponse

# ---------------------------------------------------
# перелік груп студентів
@app.get("/api/groups") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_groups(db: MongoClient = Depends(get_db)): 
    """
    перелік груп студентів
    \nотримуємо список об'єктів груп
    """
    return find_documents(db["groups"], {}, {}, {"name": 1})

# ---------------------------------------------------
# група за заданим id
@app.get("/api/groups/{id}") 
def get_group(id: int, db: MongoClient = Depends(get_db)): 
    """
    отримуємо групу за заданим id
    \nякщо не знайдена, відправляємо статусний код і повідомлення про помилку
    \nякщо групу за заданим id знайдено, відправляємо її як об'єкт
    """
    # отримуємо групу за заданим id
    group = find_document(db["groups"], {"_id": id}, {})

    # якщо не знайдена, відправляємо статусний код і повідомлення про помилку 
    if group == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Група не знайдена"}) 
    
    #якщо групу за заданим id знайдено, відправляємо її як об'єкт 
    return group 