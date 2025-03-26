from conn import *
import psycopg2 
from app import app
from fastapi import Depends, Query, Cookie, Form, status
from fastapi.responses import Response, JSONResponse

# ---------------------------------------------------
# перелік користувачів
@app.get("/api/users") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_users(idGroup: int = Query(default = None), conn: psycopg2.connect = Depends(get_db)):
    """
    перелік користувачів
    """
    cursor = conn.cursor()  
    # якщо група не задана, повертаємо перелік всіх користувачів    
    strWhere = ""
    if (idGroup != None):
        # якщо група задана, то тільки перелік користувачів (студентів) групи
        strWhere = f"WHERE id_group={idGroup}"
    sql = f"SELECT user_id, login, password, first_name, last_name, role, id_group FROM users {strWhere} ORDER BY last_name" 
    cursor.execute(sql)
    users = []
    for id, login, password, firstName, lastName, role, idGroup in cursor.fetchall(): 
        users.append({ 
            "id": id, 
            "login": login, 
            "password": password, 
            "firstName": firstName, 
            "lastName": lastName, 
            "role": role,
            "idGroup": idGroup})
    cursor.close()

    return users

# ---------------------------------------------------
# користувач за заданим id
@app.get("/api/users/{id}") 
def get_user(response: Response, id, conn: psycopg2.connect = Depends(get_db)): 
    """
    користувач за заданим id
    """
    cursor = conn.cursor()
    # отримуємо користувача за id, поєднуючи дані таблиць користувачів та груп через OUTER JOIN
    sql = f"""SELECT u.user_id, u.login, u.password, u.first_name, u.last_name, u.role, u.id_group, g.name  
        FROM users u LEFT OUTER JOIN groups g 
        ON u.id_group = g.group_id 
        WHERE user_id={id}"""
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if row == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач не знайдений"}) 
    
    id, login, password, firstName, lastName, role, idGroup, name = row
    response.set_cookie(key="user_id", value = id) 
    response.set_cookie(key="group_id", value = idGroup)    
    #якщо користувача знайдено, відправляємо його 
    return { "id": id, 
            "login": login, 
            "password": password, 
            "firstName": firstName, 
            "lastName": lastName, 
            "role": role,
            "idGroup": idGroup,
            "name": name} 

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
                conn: psycopg2.connect = Depends(get_db)): 
    """
    створення нового користувача
    """    
    # отримуємо користувача за login 
    sql = """SELECT user_id  
            FROM users  
            WHERE login = %s"""  
    cursor = conn.cursor()
    cursor.execute(sql, (login,))
    row = cursor.fetchone()   

    if row != None:
        return JSONResponse(status_code = status.HTTP_409_CONFLICT, content={ "message": "Користувач " + login + " уже існує!"}) 
    
    sql = """INSERT INTO users(
	        login, password, first_name, last_name, role, id_group)
            VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (login, password, first_name, last_name, role, group))
    conn.commit() 

    # отримуємо поточне значення user_id з відповідної послідовності
    sql = """SELECT currval('users_user_id_seq')"""
    cursor.execute(sql)
    id, = cursor.fetchone()  
    cursor.close()

    response.set_cookie(key="user_id", value = id) 
    response.set_cookie(key="group_id", value = group) 
    return { "id": id, 
            "login": login, 
            "password": password, 
            "firstName": first_name, 
            "lastName": last_name, 
            "role": role,
            "idGroup": group }  

# ---------------------------------------------------
# користувач за заданим логіном та паролем
@app.post("/api/users/hello") 
def get_user(response: Response, login: str  = Form(), password: str = Form(min_length = 4), conn: psycopg2.connect = Depends(get_db)): 
    """
    користувач за заданим логіном та паролем
    """    
    cursor = conn.cursor()
    # отримуємо користувача за login 
    sql = """SELECT user_id, password, first_name, last_name, role, id_group 
        FROM users WHERE login = %s """
    cursor.execute(sql, (login,))
    row = cursor.fetchone() 
    cursor.close()   

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if row == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач " + login + " не знайдений"}) 
    
    id, dbPassword, firstName, lastName, role, idGroup = row 
    if dbPassword != password:
        return JSONResponse(status_code = status.HTTP_401_UNAUTHORIZED, content={ "message": "Неправильний пароль"}) 
    
    response.set_cookie(key="user_id", value = id) 
    response.set_cookie(key="group_id", value = idGroup)     
    # якщо користувача знайдено, відправляємо його
    return { "id": id, 
            "login": login, 
            "firstName": firstName, 
            "lastName": lastName, 
            "role": role,
            "idGroup": idGroup } 

# ---------------------------------------------------   
# зміна даних користувача
@app.put("/api/users") 
def edit_user(response: Response, 
            user_id: int | None = Cookie(default=None),
            login: str  = Form(),
            password: str = Form(min_length = 4),
            last_name: str = Form(),
            first_name: str = Form(), 
            conn: psycopg2.connect = Depends(get_db)): 
    """
    зміна даних користувача
    """    
    cursor = conn.cursor()
    # отримуємо користувача за id 
    sql = f"SELECT user_id, role, id_group FROM users WHERE user_id = {user_id}" 
    cursor.execute(sql)
    row = cursor.fetchone()   

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if row == None:  
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач не знайдений"}) 
    
    # якщо користувач знайдений, змінюємо його дані і відправляємо назад клієнту 
    id, role, idGroup = row
    sql = """UPDATE users 
    SET login = %s, 
        password = %s,
        first_name = %s,
        last_name = %s
    WHERE user_id = %s"""
    cursor.execute(sql, (login, password, first_name, last_name, user_id))
    conn.commit()
    cursor.close()

    response.set_cookie(key="user_id", value = id) 
    response.set_cookie(key="group_id", value = idGroup)        
    return { "id": id,
            "login": login, 
            "firstName": first_name, 
            "lastName": last_name, 
            "role": role,
            "idGroup": idGroup } 
   
# ---------------------------------------------------   
# видалення користувача
@app.delete("/api/users/{id}") 
def delete_user(id, conn: psycopg2.connect = Depends(get_db)): 
    """
    видалення користувача
    """
    cursor = conn.cursor()
    # отримуємо користувача за id 
    sql = f"SELECT user_id FROM users WHERE user_id = {id}" 
    cursor.execute(sql)
    row = cursor.fetchone()   

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if row == None:  
        return JSONResponse( status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Користувач не знайдений"}) 
    
    # якщо користувача знайдено, видаляємо його 
    sql = f"DELETE FROM users WHERE user_id = {id}"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    return  