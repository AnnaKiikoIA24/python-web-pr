from conn import *
from pymongo import MongoClient 
from app import app
from fastapi import Depends, Query, Body, status 
from fastapi.responses import JSONResponse
from bson import ObjectId

# ---------------------------------------------------
@app.get("/api/rating") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_ratings(idLesson: str = Query(default = None), db: MongoClient = Depends(get_db)): 
    """
    рейтинг студентів (idLesson != None => на заданому занятті)
    \nякщо заняття не задане, повертаємо перелік всіх рейтингів по всіх заняттях
    """
    condition = {}
    if (idLesson != None):
        condition["lesson.$id"] = ObjectId(idLesson)
    
    pipeline = [                  
        # фільтруємо рейтинги за умовою condition
        { "$match": condition },
        # поєднання з колекцією users для вибору інформації про студента      
        {
            "$lookup": {
                "from": "users",           
                # Поле в колекції ratings, за яким будемо поєднувати
                "localField": "student.$id",    
                # Поле в коллекції users, за яким будемо поєднувати
                "foreignField": "_id",      
                # Назва нового масиву, у якому буде інформація із колекції users
                "as": "studentInfo"            
            }
        },
        # розгортаємо масив studentInfo
        { "$unwind": "$studentInfo" },
        # сортуємо за прізвищем студента
        { "$sort": { "studentInfo.lastName": 1 }},
        # створюємо проекцію загального масиву даних
        {
            "$project": {
                "_id": 0,
                "id": "$_id",   
                "idLesson": "$lesson.$id",            
                "idStudent": "$student.$id",
                "isPresence": 1,
                "grade": 1,               
                "firstName": "$studentInfo.firstName",
                "lastName": "$studentInfo.lastName"
            }
        }                       
    ]

    result = []
    for r in db.ratings.aggregate(pipeline):
        # конвертуємо ObjectId у строку
        r["id"] = str(r["id"])
        r["idLesson"] = str(r["idLesson"])        
        r["idStudent"] = str(r["idStudent"])
        result.append(r)
    # повертаємо масив об'єктів 
    return result 

# ---------------------------------------------------
@app.get("/api/rating/{id}") 
def get_rating(id: str, db: MongoClient = Depends(get_db)):
    """
    рядок рейтингу за заданим id
    """
    pipeline = [                  
        # фільтруємо рейтинги за ідентифікатором
        { "$match": { "_id": ObjectId(id)} },
        # поєднання з колекцією users для вибору інформації про студента      
        {
            "$lookup": {
                "from": "users",           
                # Поле в колекції ratings, за яким будемо поєднувати
                "localField": "student.$id",    
                # Поле в коллекції users, за яким будемо поєднувати
                "foreignField": "_id",      
                # Назва нового масиву, у якому буде інформація із колекції users
                "as": "studentInfo"            
            }
        },
        # розгортаємо масив studentInfo
        { "$unwind": "$studentInfo" },
        # сортуємо за прізвищем студента
        { "$sort": { "studentInfo.lastName": 1 }},
        # створюємо проекцію загального масиву даних
        {
            "$project": {
                "_id": 0,
                "id": "$_id",   
                "idLesson": "$lesson.$id",            
                "idStudent": "$student.$id",
                "isPresence": 1,
                "grade": 1,               
                "firstName": "$studentInfo.firstName",
                "lastName": "$studentInfo.lastName"
            }
        }                       
    ]   
    ratings = db.ratings.aggregate(pipeline)

    # якщо рядок рейтингу не знайдено, відправляємо статусний код і повідомлення про помилку 
    if not ratings.alive:   
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content={ "message": "Рядок рейтингу не знайдений"})     
    
    #якщо рядок рейтингу знайдено, відправляємо його 
    result = ratings.next()    
    # конвертуємо ObjectId у строку
    result["id"] = str(result["id"])
    result["idLesson"] = str(result["idLesson"])        
    result["idStudent"] = str(result["idStudent"])
    return result

# ---------------------------------------------------
@app.get("/api/rating/student/{idStudent}/{idJournal}/{idSubject}") 
# За допомогою класу Depends() у функцію передається результат функції get_db()
def get_ratings_student(idStudent: str, idJournal: int, idSubject: int, db: MongoClient = Depends(get_db)):
    """
    рейтинг студента за заданим id студента, журнала, навчального предмета
    """
    pipeline = [            
        # фільтрація за ідентифікатором студента
        { "$match": { "student.$id": ObjectId(idStudent) } },                  
        # поєднання з колекцією lessons         
        {
            "$lookup": {
                "from": "lessons",           
                # Поле в колекції groups, за яким будемо поєднувати
                "localField": "lesson.$id",    
                # Поле в коллекції lessons, за яким будемо поєднувати
                "foreignField": "_id",      
                # Назва нового масиву, у якому буде інформація із колекції lessons
                "as": "lessonInfo"            
            }
        },
        # розгортаємо масив lessonInfo
        { "$unwind": "$lessonInfo" },
        # фільтрація за ідентифікатором навчального предмета та журналу
        { "$match": { "lessonInfo.subject.$id": idSubject, "lessonInfo.journal.$id": idJournal } }, 
        # поєднання з колекцією users         
        {
            "$lookup": {
                "from": "users",           
                # Поле в колекції groups, за яким будемо поєднувати
                "localField": "lessonInfo.teacher.$id",    
                # Поле в коллекції users, за яким будемо поєднувати
                "foreignField": "_id",      
                # Назва нового масиву, у якому буде інформація із колекції users
                "as": "teacherInfo"            
            }
        },
        # розгортаємо масив teacherInfo
        { "$unwind": "$teacherInfo" },    

        # створюємо проекцію загального масиву даних
        {
            "$project": {
                "_id": 0,
                "id": "$_id",   
                "idLesson": "$lessonInfo._id",            
                "dateLesson": "$lessonInfo.dateLesson",
                "theme": "$lessonInfo.theme",
                "maxGrade": "$lessonInfo.maxGrade",
                "firstName": "$teacherInfo.firstName",
                "lastName": "$teacherInfo.lastName",                
                "isPresence": 1,
                "grade": 1
            }
        }                       
    ]

    result = []
    for r in db.ratings.aggregate(pipeline):
        # конвертуємо ObjectId у строку
        r["id"] = str(r["id"])
        r["idLesson"] = str(r["idLesson"])   
        # конвертуємо datetime у date 
        r["dateLesson"] = r["dateLesson"].date()     
        result.append(r)
    # повертаємо масив об'єктів 
    return result 

# ---------------------------------------------------    
@app.post("/api/rating") 
def create_rating(data = Body(), db: MongoClient = Depends(get_db)): 
    """
    створення нового рейтингу за списком рядків
    """
    newRatings = []
    for item in data:
        newRatings.append({
            "lesson": { "$ref": "lessons", "$id": ObjectId(item["idLesson"]) }, 
            "student": { "$ref": "users", "$id": ObjectId(item["idStudent"]) }, 
            "isPresence": item["isPresence"], 
            "grade": None if item["grade"] == "" else item["grade"]
        })

    # множинне додавання рядків
    db.ratings.insert_many(newRatings)
    return      
 
# ---------------------------------------------------   
@app.put("/api/rating") 
def edit_rating(data  = Body(), db: MongoClient = Depends(get_db)): 
    """
    зміна даних за списком рядків рейтингу
    """
    for item in data:
        updatedRating = {
            "lesson": { "$ref": "lessons", "$id": ObjectId(item["idLesson"]) }, 
            "student": { "$ref": "users", "$id": ObjectId(item["idStudent"]) }, 
            "isPresence": item["isPresence"], 
            "grade": None if item["grade"] == "" else item["grade"]
        }
        update_document(db.ratings, {"_id": ObjectId(item["id"]) }, updatedRating)
    return     
   
# ---------------------------------------------------   
@app.delete("/api/rating") 
def delete_rating(data = Body(), db: MongoClient = Depends(get_db)): 
    """
    видалення рядків рейтингу за списком
    """
    for item in data:
        delete_document(db.ratings, {"_id": ObjectId(item["id"]) })  
    return  
