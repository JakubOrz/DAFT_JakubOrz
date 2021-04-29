import hashlib
from fastapi import FastAPI, status, Response
from Models import SimplePacjent, Pacjent
from zad3 import zadanie3ruter

app = FastAPI()

app.include_router(
    zadanie3ruter,
    prefix="",
    tags=["PierwszyRuter"],
)


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/hello/{name}")
def hello_name(name: str):
    return f"Hello {name}"


@app.post("/method", status_code=status.HTTP_201_CREATED)
def hellopost():
    return {"method": "POST"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(pacjent: SimplePacjent):
    global lista, counter
    pacjent = Pacjent(pacjent, numer=counter)
    lista[counter] = pacjent
    counter += 1
    return pacjent
