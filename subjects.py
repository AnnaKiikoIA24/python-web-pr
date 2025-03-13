from db import *
from app import app
from sqlalchemy.orm import Session 
from fastapi import Depends, status
from fastapi.responses import JSONResponse

# ---------------------------------------------------
@app.get("/api/subjects") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_subjects(db: Session = Depends(get_db)):
    """
    перелік навчальних предметів
    """
    # отримуємо  список  об'єктів User
    return db.query(Subject).all() 

# ---------------------------------------------------
@app.get("/api/subjects/{id}") 
def get_subject(id, db: Session = Depends(get_db)): 
    """
    навчальний предмет за заданим id
    """
    # отримуємо навчальний предмет за заданим id
    subject = db.query(Subject).filter(Subject.id == id).first() 
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if subject == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Навчальний предмет не знайдений"}) 
    
    #якщо навчальний предмет за заданим id знайдено, відправляємо його 
    return subject 