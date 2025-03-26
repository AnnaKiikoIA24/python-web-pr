import psycopg2 
from conn import *
from app import app
from fastapi import Depends, status
from fastapi.responses import JSONResponse

# ---------------------------------------------------
# перелік груп студентів
@app.get("/api/groups") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_groups(conn: psycopg2.connect = Depends(get_db)): 
    """
    перелік груп студентів
    \nотримуємо список об'єктів User
    """
    cursor = conn.cursor()  
    sql = "SELECT group_id, name FROM groups ORDER BY name" 
    cursor.execute(sql)
    groups = []
    for id, name in cursor.fetchall(): 
        groups.append({ 
            "id": id, 
            "name": name})
    cursor.close()

    return groups

# ---------------------------------------------------
# група за заданим id
@app.get("/api/groups/{id}") 
def get_group(id, conn: psycopg2.connect = Depends(get_db)): 
    """
    отримуємо групу за заданим id
    \nякщо не знайдена, відправляємо статусний код і повідомлення про помилку
    \nякщо групу за заданим id знайдено, відправляємо її як об'єкт
    """
    # отримуємо групу за заданим id
    cursor = conn.cursor()  
    sql = f"SELECT group_id, name FROM groups WHERE group_id={id}" 
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()  

    # якщо не знайдена, відправляємо статусний код і повідомлення про помилку 
    if row == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Група не знайдена"}) 
    
    #якщо групу за заданим id знайдено, відправляємо її як об'єкт 
    id, name = row  
    return { "id": id, 
             "name": name } 