from db import *
from app import app
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse

# ---------------------------------------------------
@app.get("/api/journals") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_journals(idGroup: int = Query(default = None), db: Session = Depends(get_db)): 
    """
    перелік журналів успішності
    """
    # отримуємо  список  об'єктів Journal, поєднуючи дані таблиць журналів та груп
    # сортування за роком у зворотному порядку + назва групи
    
    # якщо група не задана, повертаємо перелік всіх користувачів
    if (idGroup == None):
        stmt  = select(Journal.id, Journal.year, Group.name, Journal.idGroup).join_from(Journal, Group).order_by(Journal.year.desc(), Group.name)
    # якщо група задана, додатково фільтрація по групі
    else:
        stmt  = select(Journal.id, Journal.year, Group.name, Journal.idGroup).join_from(Journal, Group).where(Journal.idGroup == idGroup).order_by(Journal.year.desc(), Group.name)
    #.select_from(Journal).join(Group, Group.id == Journal.idGroup)
    print (stmt)
    return db.execute(stmt).mappings().all()

# ---------------------------------------------------
@app.get("/api/journals/{id}") 
def get_journal(id, db: Session = Depends(get_db)): 
    """
    журнал успішності за заданим id
    """
    # отримуємо журнал успішності за заданим id
    journal = db.query(Journal).filter(Journal.id == id).first() 
    # якщо не знайдена, відправляємо статусний код і повідомлення про помилку 
    if journal == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Журнал успішності не знайдений"}) 
    
    #якщо журналів успішності за заданим id знайдений, відправляємо його як об'єкт 
    return journal 