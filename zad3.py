from fastapi import APIRouter
from datetime import date
from fastapi.responses import HTMLResponse

zadanie3ruter = APIRouter()


@zadanie3ruter.get("/test")
def testrutera():
    return "Hehe ruter działa"


@zadanie3ruter.get("/hello")
def zadanie3_1(response=HTMLResponse):
    return HTMLResponse(content=f"<h1>Hello! Today date is {date.today()} </h1>", status_code=200)
