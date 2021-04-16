from fastapi import FastAPI, status

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/hello/{name}")
def hello_name(name: str):
    return f"Hello {name}"


@app.post("/method", status_code=status.HTTP_201_CREATED)
def hellopost():
    return ["mehod: POST"]


@app.get("/method")
def hellopost():
    return ["method: GET"]


@app.put("/method")
def hellopost():
    return ["method: PUT"]


@app.options("/method")
def hellopost():
    return ["method: OPTIONS"]


@app.delete("/method")
def hellopost():
    return ["method: DELETE"]


