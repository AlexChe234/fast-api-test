from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


@app.get("/date")
def get_current_date():
    return {"date": datetime.now().date().isoformat()}


