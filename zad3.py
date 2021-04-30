import base64
from hashlib import sha256
from fastapi import APIRouter, Cookie, HTTPException, status, Depends
from datetime import date
from fastapi.responses import HTMLResponse
from fastapi import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

zadanie3ruter = APIRouter()
kluczeSesji: set = set()
secretKey = "Tajnekoddostarwarsilubieplackiivieratobyladobraadmin"
security = HTTPBasic()
realpassowrd = "4dm1n:NotSoSecurePa$$"


@zadanie3ruter.get("/test")
def testrutera():
    return "Hehe ruter działa"


@zadanie3ruter.get("/hello")
def zadanie3_1():
    return HTMLResponse(content=f"<h1>Hello! Today date is {date.today()}</h1>", status_code=200)


@zadanie3ruter.post("/login_session")
def loginSession(response: Response, logintoken: HTTPBasicCredentials = Depends(security)):
    if base64.b64decode(logintoken).decode("Utf-8") != realpassowrd:
        raise HTTPException(status_code=401, detail="Unathorized")
    session_token = sha256(f"{secretKey}{realpassowrd}".encode()).hexdigest()
    kluczeSesji.add(session_token)
    response.set_cookie(key="token", value=session_token)
    return


@zadanie3ruter.post("/login_token")
def loginToken(*, logintoken: HTTPBasicCredentials = Depends(security), token=Cookie(None)):
    if base64.b64decode(logintoken).decode("Utf-8") != realpassowrd:
        raise HTTPException(status_code=401, detail="Unathorized")
    if token in kluczeSesji:
        return {"token": str(token)}
    raise HTTPException(status_code=401, detail="Unathorised")
