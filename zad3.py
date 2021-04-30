import base64
from hashlib import sha256
from fastapi import APIRouter, Cookie, HTTPException, status, Depends
from datetime import date
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

zadanie3ruter = APIRouter()
kluczeSesji: set = set()
secretKey = "Tajnekoddostarwarsilubieplackiivieratobyladobraadmin"
security = HTTPBasic()
realpassowrd2 = "4dm1n:NotSoSecurePa$$"
realusername = "4dm1n"
realpassword = "NotSoSecurePa$$"


@zadanie3ruter.get("/test")
def testrutera():
    return "Hehe ruter działa"


@zadanie3ruter.get("/hello")
def zadanie3_1():
    return HTMLResponse(content=f"<h1>Hello! Today date is {date.today()}</h1>", status_code=200)


@zadanie3ruter.post("/logintest")
def logintest(response: Response, logintoken: HTTPBasicCredentials = Depends(security)):
    print(logintoken)
    return logintoken


@zadanie3ruter.post("/login_session")
def loginSession(response: Response, logintoken: HTTPBasicCredentials = Depends(security),
                 status_code=status.HTTP_201_CREATED):
    if str(logintoken.username) != realusername or str(logintoken.password) != realpassword:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    session_token = sha256(f"{secretKey}{date.today()}".encode()).hexdigest()
    kluczeSesji.add(session_token)
    response.set_cookie(key="session_token", value=session_token)
    response.status_code = status.HTTP_201_CREATED
    return response


@zadanie3ruter.post("/login_token", status_code=201)
def loginToken(logintoken: HTTPBasicCredentials = Depends(security),
               session_token=Cookie(None)):
    if str(logintoken.username) != realusername or str(logintoken.password) != realpassword:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    session_token2 = sha256(f"{secretKey}placki".encode()).hexdigest()
    return JSONResponse(status_code=201, content={"token": session_token2})
