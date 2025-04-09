from conn import *
from pymongo import MongoClient 
from app import app
from fastapi import Depends, status
from fastapi.responses import JSONResponse

# ---------------------------------------------------
# перелік навчальних предметів
@app.get("/api/subjects") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_subjects(db: MongoClient = Depends(get_db)): 
    """
    перелік навчальних предметів
    """
    # отримуємо список навчальних предметів
    return find_documents(db["subjects"], {}, {}, {"nameFull": 1})


# ---------------------------------------------------
# навчальний предмет за заданим id
@app.get("/api/subjects/{id}") 
def get_subject(id: int, db: MongoClient = Depends(get_db)): 
    """
    навчальний предмет за заданим id
    """
    # отримуємо навчальний предмет за заданим id
    # отримуємо групу за заданим id
    subject = find_document(db["subjects"], {"_id": id})

    # якщо не знайдена, відправляємо статусний код і повідомлення про помилку 
    if subject == None:
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Навчальний предмет не знайдений"}) 
    
    #якщо навчальний предмет за заданим id знайдено, відправляємо його 
    return subject 