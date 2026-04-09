from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}


@app.get("/date")
def get_current_date():
    return {"date": datetime.now().date().isoformat()}


@app.get("/date/{date_format}")
def get_date_with_format(date_format: str):
    """Возвращает текущую дату в указанном формате.

    Примеры форматов:
    - %Y-%m-%d → 2025-01-15
    - %d.%m.%Y → 15.01.2025
    - %d %B %Y → 15 January 2025
    - %A, %d %B %Y → Wednesday, 15 January 2025
    """
    try:
        formatted_date = datetime.now().strftime(date_format)
        return {"date": formatted_date, "format": date_format}
    except Exception as e:
        return {"error": f"Invalid date format: {str(e)}", "example": "Use formats like %Y-%m-%d, %d.%m.%Y"}


