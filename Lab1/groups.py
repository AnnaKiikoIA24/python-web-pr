from db import *
from app import app
from sqlalchemy.orm import Session 
from fastapi import Depends, status
from fastapi.responses import JSONResponse

# ---------------------------------------------------
@app.get("/api/groups") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_groups(db: Session = Depends(get_db)):
    """
    перелік груп студентів
    \nотримуємо список об'єктів User
    """
    return db.query(Group).all() 

# ---------------------------------------------------
# група за заданим id
@app.get("/api/groups/{id}") 
def get_group(id, db: Session = Depends(get_db)): 
    """
    отримуємо групу за заданим id
    \nякщо не знайдена, відправляємо статусний код і повідомлення про помилку
    \nякщо групу за заданим id знайдено, відправляємо її як об'єкт
    """
    group = db.query(Group).filter(Group.id == id).first()  
    if group == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Група не знайдена"})  
    return group 