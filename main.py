from fastapi import FastAPI, status, Response
from Models import SimplePacjent, Pacjent
from zad3 import zadanie3ruter
from zad4 import zad4ruter
from zadanie5.ruter5 import router as zad5ruter

app = FastAPI()


app.include_router(
    zadanie3ruter,
    prefix="",
    tags=["PierwszyRuter"],
)

app.include_router(
    zad4ruter,
    prefix="",
    tags=["Zadanie4"]
)

app.include_router(
    zad5ruter,
    prefix="/orm",
    tags=["Zadanie5"]
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
