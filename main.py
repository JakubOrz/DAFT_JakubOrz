from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Helo World!"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return f"Hello {name}"
