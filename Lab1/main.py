from app import app
from db import * 
from users import *
from groups import *
from subjects import *
from journals import *
from lessons import *
from rating import *
from fastapi.responses import FileResponse
    
@app.get("/") 
def main(): 
    """
    Метод завантажує дані стартової сторінки та надає клієнту.
    """
    return FileResponse("public/index.html") 
