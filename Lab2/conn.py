import psycopg2 
# визначаємо залежність 
# функція get_db(), через яку об'єкт підключення до бази даних буде передаватися у функцію обробки
def get_db(): 
    # створюємо об'єкт підключення до бази даних
    conn = psycopg2.connect(dbname="journal", user="postgres", password="12345", host="127.0.0.1") 
    try: 
        # yield  буде  виконуватися  при отриманні кожного нового запиту
        yield conn 
    finally: 
        conn.close() 
