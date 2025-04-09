from pymongo import MongoClient 
# визначаємо залежність 
# функція get_db(), через яку об'єкт підключення до бази даних буде передаватися у функцію обробки
def get_db(): 
    # Створюємо клієнт 
    client = MongoClient('localhost', 27017)
    # Підключаємося до нашої бази даних 
    db = client['journal'] 
    # yield  буде  виконуватися  при отриманні кожного нового запиту
    yield db 

def find_documents(collection, condition, projection={}, sort={}): 
    """ Function to retrieve multiple documents from a provided 
    Collection using a dictionary containing a document's elements. 
    """ 
    results = []
    # модифікація колекції
    for r in collection.find(condition, projection).sort(sort):
        # додаємо до словнику елемент з ключем "id"
        r["id"] = r["_id"]
        # видаляємо зі словника елемент з ключем "_id"
        r.pop("_id") 
        print(r)
        results.append(r)
    return results
    
def find_document(collection, condition, projection={}): 
    """ Function to retrieve single document from a provided 
    Collection using a dictionary containing a document's elements. 
    """ 
    r = collection.find_one(condition, projection)
    if r != None:
        # додаємо до словнику елемент з ключем "id"
        r["id"] = r["_id"]
        # видаляємо зі словника елемент з ключем "_id"
        r.pop("_id") 
    return r    
    
def insert_document(collection, data): 
    """ Function to insert a document into a collection and 
    return the document's id. 
    """ 
    return collection.insert_one(data).inserted_id    

def update_document(collection, query_elements, new_values): 
    "Function to update a single document in a collection." 
    collection.update_one(query_elements, {'$set': new_values})

def delete_document(collection, query): 
    "Function to delete a single document from a collection." 
    collection.delete_one(query) 
    