import psycopg2 
from conn import *
from app import app
from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse

# ---------------------------------------------------
# перелік журналів успішності
@app.get("/api/journals") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_journals(idGroup: int = Query(default = None), conn: psycopg2.connect = Depends(get_db)): 
    """
    перелік журналів успішності
    """
    cursor = conn.cursor()  
    # якщо група не задана, повертаємо перелік всіх ;ehyfksd    
    strWhere = ""
    # якщо група задана, додатково фільтрація по групі
    if (idGroup != None):
        strWhere = f" AND g.group_id = {idGroup}"
    sql = f"""SELECT j.journal_id, j.year, j.id_group, g.name 
        FROM journals j, groups g 
        WHERE j.id_group = g.group_id {strWhere} 
        ORDER BY j.year DESC, g.name"""
    cursor.execute(sql)
    journals = []
    for id, year, idGroup, name in cursor.fetchall(): 
        journals.append({ 
            "id": id, 
            "year": year,
            "idGroup": idGroup,
            "name": name})
    cursor.close()

    return journals

# ---------------------------------------------------
# журнал успішності за заданим id
@app.get("/api/journals/{id}") 
def get_journal(id, conn: psycopg2.connect = Depends(get_db)): 
    """
    журнал успішності за заданим id
    """
    cursor = conn.cursor()  
    # отримуємо журнал успішності за заданим id
    sql = f"""SELECT j.journal_id, j.year, j.id_group 
        FROM journals j
        WHERE j.journal_id = {id}"""
    cursor.execute(sql)    
    row = cursor.fetchone()
    cursor.close()

    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if row == None:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Журнал успішності не знайдений"}) 
    
    #якщо журналів успішності за заданим id знайдений, відправляємо його як об'єкт 
    id, year, idGroup = row
    return { "id": id,
              "year": year,
              "idGroup": idGroup } 