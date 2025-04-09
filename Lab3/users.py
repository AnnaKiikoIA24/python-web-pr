from conn import *
from pymongo import MongoClient 
from app import app
from fastapi import Depends, Query, Cookie, Form, status
from fastapi.responses import Response, JSONResponse
from bson import ObjectId, DBRef

# ---------------------------------------------------
# перелік користувачів
@app.get("/api/users") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_users(idGroup: int = Query(default = None), db: MongoClient = Depends(get_db)):
    """
    перелік користувачів
    """
    # якщо група не задана, повертаємо перелік всіх користувачів    
    condition = {}
    if (idGroup != None):
        # якщо група задана, то тільки перелік користувачів (студентів) групи
        condition = { "idGroup": idGroup }     
    
    result = []
    for r in find_documents(db.users, condition, {}, {"lastName": 1}):
        # конвертуємо ObjectId у строку
        r["id"] = str(r["id"])
        result.append(r)
    # повертаємо масив об'єктів 
    return result    

# ---------------------------------------------------
# користувач за заданим id
@app.get("/api/users/{id}") 
def get_user(response: Response, id: str, db: MongoClient = Depends(get_db)): 
    """
    користувач за заданим id 
    \n("плюс" назва групи для студента)
    """
    pipeline = [    
        # умова
        { "$match": { "_id": ObjectId(id) } },
        {
            "$lookup": {
                "from": "groups",           # Колекция, з якою поєднуємо: groups
                "localField": "idGroup",    # Поле в колекції users, за яким будемо поєднувати
                "foreignField": "_id",      # Поле в колекції groups, за яким будемо поєднувати
                "as": "groupInfo"           # Назва нового масиву, у якому буде інформацяя із колекції groups
            }
        },
        {
            # Розгортаємо масив groupInfo
            "$unwind": {
                "path": "$groupInfo", 
                # якщо в groupInfo відсутні дані (користувач є викладачем, немає прив'язки до групи), зберігаємо пустий масив (аналог SQL LEFT JOIN)    
                "preserveNullAndEmptyArrays": True     
            }
        },
        {
            "$project": {
                "_id": 0,
                "id": "$_id",
                "login": 1,                
                "password": 1,             
                "firstName": 1,
                "lastName": 1,
                "role": 1,
                "idGroup": 1,            
                "name":  {            
                    # якщо groupInfo не пусте, то беремо з нього nameGroup, інакше - ставимо None
                    "$ifNull": ["$groupInfo.name", None]
                }
            }
        }         
    ]
    users = db.users.aggregate(pipeline)

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if not users.alive:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач не знайдений"}) 
    
    #якщо користувач за заданим id знайдений, відправляємо його як об'єкт 
    user = users.next() 
    # конвертуємо атрибут типу ObjectId у строку
    user["id"] = str(user["id"])   

    response.set_cookie(key="user_id", value = user["id"]) 
    response.set_cookie(key="group_id", value = user["idGroup"])  
    return user

# ---------------------------------------------------   
# створення нового користувача 
@app.post("/api/users") 
def create_user(response: Response,
                login: str  = Form(),
                password: str = Form(min_length = 4),
                last_name: str = Form(),
                first_name: str = Form(),
                role: bool = Form(),
                # значення за замовчуванням None, не передається для ролі викладача
                group: int = Form(default = None),
                db: MongoClient = Depends(get_db)): 
    """
    створення нового користувача
    """    
    # отримуємо користувача за login 
    user = find_document(db["users"], {'login': login})  

    if user != None:
        return JSONResponse(status_code = status.HTTP_409_CONFLICT, content={ "message": "Користувач " + login + " уже існує!"}) 
    
    newUser = {
        "login": login,
        "password": password,
        "firstName": first_name,
        "lastName": last_name,
        "role": role,
        "idGroup": group
    }

    newId = str(insert_document(db["users"], newUser))

    response.set_cookie(key="user_id", value = newId) 
    response.set_cookie(key="group_id", value = group) 
    return {
        "id": newId,
        "login": login,
        "password": password,
        "firstName": first_name,
        "lastName": last_name,
        "role": role,
        "idGroup": group        
    }

# ---------------------------------------------------
# користувач за заданим логіном та паролем
@app.post("/api/users/hello") 
def get_user(response: Response, login: str  = Form(), password: str = Form(min_length = 4), db: MongoClient = Depends(get_db)): 
    """
    користувач за заданим логіном та паролем
    """    
    user = find_document(db["users"], {'login': login})  

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if user == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач " + login + " не знайдений"}) 
    
    if user["password"] != password:
        return JSONResponse(status_code = status.HTTP_401_UNAUTHORIZED, content={ "message": "Неправильний пароль"}) 
    
    # конвертуємо ObjectId у строку
    user["id"] = str(user["id"])   

    response.set_cookie(key="user_id", value = user["id"]) 
    response.set_cookie(key="group_id", value = user["idGroup"])     
    # якщо користувача знайдено, відправляємо його
    return user 

# ---------------------------------------------------   
# зміна даних користувача
@app.put("/api/users") 
def edit_user(response: Response, 
            user_id: str | None = Cookie(default=None),
            login: str  = Form(),
            password: str = Form(min_length = 4),
            last_name: str = Form(),
            first_name: str = Form(), 
            db: MongoClient = Depends(get_db)): 
    """
    зміна даних користувача
    """    
    # отримуємо користувача за id 
    user = find_document(db["users"], {'_id': ObjectId(user_id)})  

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if user == None:  
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач не знайдений"}) 
    
    # якщо користувач знайдений, змінюємо його дані і відправляємо назад клієнту 
    updatedUser = {
        "login": login,
        "password": password,
        "firstName": first_name,
        "lastName": last_name
    }
    update_document(db["users"],  { '_id': ObjectId(user_id) }, updatedUser)

    # перечитуємо, щоб отримати інформацію про роль та групу
    updatedUser = find_document(db["users"], {'_id': ObjectId(user_id)})  
    updatedUser["id"] = user_id;
    return updatedUser
   
# ---------------------------------------------------   
# видалення користувача
@app.delete("/api/users/{id}") 
def delete_user(id: str,  db: MongoClient = Depends(get_db)): 
    """
    видалення користувача
    """
    # отримуємо користувача за id 
    user = find_document(db["users"], {'_id': ObjectId(id)})  

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if user == None:  
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач не знайдений"}) 

    delete_document(db["users"], {'_id': ObjectId(id)})    
    return  