from conn import *
from pymongo import MongoClient 
from app import app
from fastapi import Depends, Query, status
from fastapi.responses import JSONResponse

# ---------------------------------------------------
# перелік журналів успішності
@app.get("/api/journals") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_journals(idGroup: int = Query(default = None), db: MongoClient = Depends(get_db)): 
    """
    перелік журналів успішності
    """
    # якщо група не задана, повертаємо перелік всіх журналів;  
    condition = {}
    # якщо група задана, додатково фільтрація по групі
    if (idGroup != None):
        condition = { "group.$id": idGroup }

    pipeline = [    
        # умова
        { "$match": condition },
        # поєднання з колекцією groups         
        {
            "$lookup": {
                "from": "groups",           
                # Поле в колекції journals, за яким будемо поєднувати
                "localField": "group.$id",    
                # Поле в коллекції groups, за яким будемо поєднувати
                "foreignField": "_id",      
                # Назва нового масиву, у якому буде інформація із колекції groups
                "as": "groupInfo"            
            }
        },  
        # розгортаємо масив groupInfo
        { "$unwind": "$groupInfo" },                  
        # сортування: навчальний рік - за зменшенням, назва групи - за збільшенням
        { "$sort": { "year": -1, "groupInfo.name": 1} },
        # проекція даних для виведення результату
        { "$project": { 
             "_id": 0, "id": "$_id", "year": 1, "idGroup": "$groupInfo._id", "name": "$groupInfo.name"
            } 
        }       
    ]
    # повертаємо масив об'єктів 
    return [r for r in db.journals.aggregate(pipeline)] 

# ---------------------------------------------------
# журнал успішності за заданим id
@app.get("/api/journals/{id}") 
def get_journal(id: int, db: MongoClient = Depends(get_db)): 
    """
    журнал успішності за заданим id
    """
    pipeline = [    
         # умова
         { "$match": { "_id": id } },
        # поєднання з колекцією groups         
        {
            "$lookup": {
                "from": "groups",           
                # Поле в колекції journals, за яким будемо поєднувати
                "localField": "group.$id",    
                # Поле в коллекції groups, за яким будемо поєднувати
                "foreignField": "_id",      
                # Назва нового масиву, у якому буде інформація із колекції groups
                "as": "groupInfo"            
            }
        },  
        # розгортаємо масив groupInfo
        { "$unwind": "$groupInfo" },                  
        # проекція даних для виведення результату
        { "$project": { 
             "_id": 0, "id": "$_id", "year": 1, "idGroup": "$groupInfo._id", "name": "$groupInfo.name"
            } 
        }             
    ]
    journals = db.journals.aggregate(pipeline)
    # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
    if not journals.alive:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Журнал успішності не знайдений"}) 
    
    #якщо журналів успішності за заданим id знайдений, відправляємо його як об'єкт 
    return journals.next()
    