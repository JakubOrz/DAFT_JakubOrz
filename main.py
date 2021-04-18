import hashlib
from fastapi import FastAPI, status, Response
from Models import SimplePacjent, Pacjent

app = FastAPI()
counter: int = 1
lista = dict()


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/hello/{name}")
def hello_name(name: str):
    return f"Hello {name}"


@app.post("/method", status_code=status.HTTP_201_CREATED)
def hellopost():
    return {"method": "POST"}


@app.get("/method")
def hellopost():
    return {"method": "GET"}


@app.put("/method")
def hellopost():
    return {"method": "PUT"}


@app.options("/method")
def hellopost():
    return {"method": "OPTIONS"}


@app.delete("/method")
def hellopost():
    return {"method": "DELETE"}


@app.get("/auth")
def authorize(password: str = None, password_hash: str = None, response: Response = 200):
    if password is None or password_hash is None or password == "" or password_hash == "":
        response.status_code = 401
        return
    h = hashlib.sha512(password.encode())
    # print(f"pass>:{password}")
    # print(f"passhash:>{password_hash}")
    # print(h.hexdigest())
    if h.hexdigest() != password_hash:
        response.status_code = 401
        return
    response.status_code = 204
    return


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(pacjent: SimplePacjent):
    global lista, counter
    pacjent = Pacjent(pacjent, numer=counter)
    lista[counter] = pacjent
    counter += 1
    return pacjent


@app.get("/patient/{numer}", status_code=200)
def getpatient(numer: int, response: Response = 200):
    if numer < 1:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return
    global lista
    pacjent: Pacjent = lista.get(numer)
    if pacjent is None:
        response.status_code = status.HTTP_404_NOT_FOUND
    return pacjent

