from db import *
from app import app
from sqlalchemy import select
from sqlalchemy.orm import Session 
from fastapi import Depends, Query, Cookie, Form, status
from fastapi.responses import Response, JSONResponse

# ---------------------------------------------------
@app.get("/api/users") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_users(idGroup: int = Query(default = None), db: Session = Depends(get_db)): 
    """
    перелік користувачів
    """
    # якщо група не задана, повертаємо перелік всіх користувачів
    if (idGroup == None):
        # отримуємо  список  об'єктів User
        return db.query(User).order_by(User.firstName).all() 
    # якщо група задана, то тільки перелік користувачів (студентів) групи
    return db.query(User).filter(User.idGroup == idGroup).order_by(User.firstName).all() 

# ---------------------------------------------------
@app.get("/api/users/{id}") 
def get_user(response: Response, id, db: Session = Depends(get_db)): 
    """
    користувач за заданим id
    """
    # отримуємо користувача за id, поєднуючи дані таблиць користувачів та груп через OUTER JOIN
    stmt  = select(User.id,
                   User.firstName,
                   User.lastName,
                   User.login,
                   User.password,
                   User.role,
                   User.idGroup,
                   Group.name).join(Group, isouter=True).where(User.id == id)
    print (stmt)
    user = db.execute(stmt).mappings().first()
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if user == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач не знайдений"}) 
    
    response.set_cookie(key="user_id", value = user.id) 
    response.set_cookie(key="group_id", value = user.idGroup)    
    #якщо користувача знайдено, відправляємо його 
    return user 

# ---------------------------------------------------    
@app.post("/api/users") 
def create_user(response: Response,
                login: str  = Form(),
                password: str = Form(min_length = 4),
                last_name: str = Form(),
                first_name: str = Form(),
                role: bool = Form(),
                # значення за замовчуванням None, не передається для ролі викладача
                group: int = Form(default = None),
                db: Session = Depends(get_db)):
    """
    створення нового користувача
    """
    # отримуємо користувача за login 
    user = db.query(User).filter(User.login == login).first()
    if user != None:
         return JSONResponse(status_code = status.HTTP_409_CONFLICT, content={ "message": "Користувач " + login + " уже існує!"}) 
    user = User(
        login = login, 
        password = password,
        lastName = last_name,
        firstName = first_name,
        role = role,
        idGroup = group)
    db.add(user) 
    db.commit() 
    db.refresh(user)
    response.set_cookie(key="user_id", value = user.id) 
    response.set_cookie(key="group_id", value = user.idGroup) 
    return user 

# ---------------------------------------------------
@app.post("/api/users/hello") 
def get_user(response: Response, login: str  = Form(), password: str = Form(min_length = 4), db: Session = Depends(get_db)): 
    """
    користувач за заданим логіном та паролем
    """
    # отримуємо користувача за login 
    user = db.query(User).filter(User.login == login).first() 
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if user == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач " + login + " не знайдений"})  
    if user.password != password:
        return JSONResponse(status_code = status.HTTP_401_UNAUTHORIZED, content={ "message": "Неправильний пароль"}) 
    
    response.set_cookie(key="user_id", value = user.id) 
    response.set_cookie(key="group_id", value = user.idGroup)     
    # якщо користувача знайдено, відправляємо його
    return user 

# ---------------------------------------------------   
@app.put("/api/users") 
def edit_user(response: Response, 
            user_id: int | None = Cookie(default=None),
            login: str  = Form(),
            password: str = Form(min_length = 4),
            last_name: str = Form(),
            first_name: str = Form(),
            db: Session = Depends(get_db)): 
    """
    зміна даних користувача
    """
    # отримуємо користувача за id 
    user = db.query(User).filter(User.id == user_id).first() 
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if user == None:  
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач не знайдений"}) 
    # якщо користувач знайдений, змінюємо його дані і відправляємо назад клієнту 
    user.login = login
    user.password = password
    user.firstName = first_name
    user.lastName = last_name

    db.commit() # зберігаємо зміни  
    db.refresh(user) 
    response.set_cookie(key="user_id", value = user.id) 
    response.set_cookie(key="group_id", value = user.idGroup)        
    return user 
   
# ---------------------------------------------------
@app.delete("/api/users/{id}") 
def delete_user(id, db: Session = Depends(get_db)): 
    """
    видалення користувача
    """
    # отримуємо користувача за id 
    user = db.query(User).filter(User.id == id).first() 
    
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if user == None: 
        return JSONResponse( status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач не знайдений"}) 
    
    # якщо користувача знайдено, видаляємо його 
    db.delete(user)  # видаляємо об'єкт 
    db.commit()     # зберігаємо зміни 
    return user 