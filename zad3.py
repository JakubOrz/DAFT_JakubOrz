import base64
from hashlib import sha256
from fastapi import APIRouter, Cookie, HTTPException, status, Depends
from datetime import date
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

zadanie3ruter = APIRouter()
kluczeSesji: set = set()
secretKey = "Tajnekoddostarwarsilubieplackiivieratobyladobraadmin"
security = HTTPBasic()

# realpassowrd2 = "4dm1n:NotSoSecurePa$$"
realusername = "4dm1n"
realpassword = "NotSoSecurePa$$"

session_cookie_value = sha256(f"{secretKey}{date.today()}".encode()).hexdigest()
session_token_value = sha256(f"{secretKey}placki".encode()).hexdigest()


@zadanie3ruter.get("/test")
def testrutera():
    return "Hehe ruter działa"


@zadanie3ruter.get("/hello")
def zadanie3_1():
    return HTMLResponse(content=f"<h1>Hello! Today date is {date.today()}</h1>", status_code=200)


@zadanie3ruter.post("/login_session")
def loginSession(response: Response, logintoken: HTTPBasicCredentials = Depends(security)):
    if str(logintoken.username) != realusername or str(logintoken.password) != realpassword:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    response.set_cookie(key="session_token", value=session_cookie_value)
    response.status_code = status.HTTP_201_CREATED
    return response


@zadanie3ruter.post("/login_token", status_code=201)
def loginToken(logintoken: HTTPBasicCredentials = Depends(security)):
    if str(logintoken.username) != realusername or str(logintoken.password) != realpassword:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return JSONResponse(status_code=201, content={"token": session_token_value})


@zadanie3ruter.get("/welcome_session", status_code=200)
def welcome_session(format: str = None, session_token: str = Cookie(None)):
    if session_token != session_cookie_value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if format == "json":
        return JSONResponse(status_code=200, content={"message": "Welcome!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")


@zadanie3ruter.get("/welcome_token", status_code=200)
def welcome_token(token: str = None, format: str = None):
    if token != session_token_value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if format == "json":
        return JSONResponse(status_code=200, content={"message": "Welcome!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")

