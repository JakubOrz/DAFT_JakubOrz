import base64
from hashlib import sha256
from fastapi import APIRouter, Cookie, HTTPException, status, Depends
from datetime import datetime
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

zadanie3ruter = APIRouter()
kluczeSesji: set = set()
secretKey = "Tajnekoddostarwarsilubieplackiivieratobyladobraadmin"
security = HTTPBasic()

# realpassowrd2 = "4dm1n:NotSoSecurePa$$"
realusername = "4dm1n"
realpassword = "NotSoSecurePa$$"

session_cookie_value = "None"
session_token_value = "None"
devlogoutredirection = "localhost:8000/logged_out"

@zadanie3ruter.get("/test")
def testrutera():
    return "Hehe ruter działa"


@zadanie3ruter.get("/hello")
def zadanie3_1():
    return HTMLResponse(content=f"<h1>Hello! Today date is {datetime.today()}</h1>", status_code=200)


@zadanie3ruter.post("/login_session")
def loginSession(response: Response, logintoken: HTTPBasicCredentials = Depends(security)):
    if str(logintoken.username) != realusername or str(logintoken.password) != realpassword:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    global session_cookie_value
    session_cookie_value = sha256(f"{secretKey}{datetime.now()}".encode()).hexdigest()
    response.set_cookie(key="session_token", value=session_cookie_value)
    response.status_code = status.HTTP_201_CREATED
    return response


@zadanie3ruter.post("/login_token", status_code=201)
def loginToken(logintoken: HTTPBasicCredentials = Depends(security)):
    if str(logintoken.username) != realusername or str(logintoken.password) != realpassword:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    global session_token_value
    session_token_value = sha256(f"{secretKey}token{datetime.now()}".encode()).hexdigest()
    return JSONResponse(status_code=201, content={"token": session_token_value})


def welcomemessage(format: str = None):
    if format == "json":
        return JSONResponse(status_code=200, content={"message": "Welcome!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")


@zadanie3ruter.get("/welcome_session", status_code=200)
def welcome_session(format: str = None, session_token: str = Cookie(None)):
    if session_token != session_cookie_value or session_cookie_value is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return welcomemessage(format)


@zadanie3ruter.get("/welcome_token", status_code=200)
def welcome_token(token: str = None, format: str = None):
    if token != session_token_value or session_token_value == "None":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return welcomemessage(format)


def handlelogout(format: str, cookies, token, devmode = False):
    if cookies:
        global session_cookie_value
        session_cookie_value = "None"
    if token:
        global session_token_value
        session_cookie_value = "None"
    if devmode:
        return RedirectResponse(status_code=status.HTTP_303_SEE_OTHER,
                                url=devlogoutredirection+f"?format={format}")
    return RedirectResponse(status_code=status.HTTP_303_SEE_OTHER,
                            url=f"https://daft-apka-jakubo.herokuapp.com/logged_out?format={format}")


@zadanie3ruter.delete("/logout_session", status_code=status.HTTP_303_SEE_OTHER)
def logout_session(format: str = None, session_token: str = Cookie(None)):
    if session_cookie_value == "None" is None or session_token != session_cookie_value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return handlelogout(format=format, cookies=True, token=False)


@zadanie3ruter.delete("/logout_token", status_code=status.HTTP_303_SEE_OTHER)
def logout_token(token: str = None, format: str = None):
    if token != session_token_value or session_token_value == "None":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return handlelogout(format=format, cookies=False, token=True)


@zadanie3ruter.get("/logged_out", status_code=200)
def loggedout(format: str = None):
    if format == "json":
        return JSONResponse(status_code=200, content={"message": "Logged out!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Logged out!</h1>")
    else:
        return PlainTextResponse(content="Logged out!")
