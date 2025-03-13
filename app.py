from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles 

app = FastAPI(openapi_url="/custom-openapi.json")
app.mount("/static", StaticFiles(directory="public"))