import psycopg2 
from conn import *
from app import app
from fastapi import Depends, status
from fastapi.responses import JSONResponse

# ---------------------------------------------------
# перелік навчальних предметів
@app.get("/api/subjects") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_subjects(conn: psycopg2.connect = Depends(get_db)): 
    """
    перелік навчальних предметів
    """
    # отримуємо список навчальних предметів
    cursor = conn.cursor()  
    sql = "SELECT subject_id, name_short, name_full FROM subjects ORDER BY name_short" 
    cursor.execute(sql)
    subjects = []
    for id, nameShort, nameFull in cursor.fetchall(): 
        subjects.append({ 
            "id": id, 
            "nameShort": nameShort,
            "nameFull": nameFull})
    cursor.close()

    return subjects


# ---------------------------------------------------
# навчальний предмет за заданим id
@app.get("/api/subjects/{id}") 
def get_subject(id, conn: psycopg2.connect = Depends(get_db)): 
    """
    навчальний предмет за заданим id
    """
    # отримуємо навчальний предмет за заданим id
    cursor = conn.cursor()  
    sql = f"SELECT subject_id, name_short, name_full FROM subjects WHERE subject_id={id}" 
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()    
    
    # якщо не знайдена, відправляємо статусний код і повідомлення про помилку 
    if row == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Навчальний предмет не знайдений"}) 
    
    #якщо навчальний предмет за заданим id знайдено, відправляємо його 
    id, nameShort, nameFull = row
    return { "id": id, 
             "nameShort": nameShort,
             "nameFull": nameFull } 