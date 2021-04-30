import base64
from hashlib import sha256
from fastapi import APIRouter, Cookie, HTTPException, status, Depends
from datetime import datetime
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi import Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sessionkeyhandler import SessionKeyHandler

zadanie3ruter = APIRouter()
security = HTTPBasic()
sessionHandler = SessionKeyHandler()

# realpassowrd2 = "4dm1n:NotSoSecurePa$$"
realusername = "4dm1n"
realpassword = "NotSoSecurePa$$"


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
    global sessionHandler
    response.set_cookie(key="session_token", value=sessionHandler.generateCookie())
    response.status_code = status.HTTP_201_CREATED
    return response


@zadanie3ruter.post("/login_token", status_code=201)
def loginToken(logintoken: HTTPBasicCredentials = Depends(security)):
    if str(logintoken.username) != realusername or str(logintoken.password) != realpassword:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    global sessionHandler
    return JSONResponse(status_code=201, content={"token": sessionHandler.generateToken()})


def welcomemessage(format: str = None):
    if format == "json":
        return JSONResponse(status_code=200, content={"message": "Welcome!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>")
    else:
        return PlainTextResponse(content="Welcome!")


@zadanie3ruter.get("/welcome_session", status_code=200)
def welcome_session(format: str = None, session_token: str = Cookie(None)):
    global sessionHandler
    if not sessionHandler.authorizeCookie(session_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return welcomemessage(format)


@zadanie3ruter.get("/welcome_token", status_code=200)
def welcome_token(token: str = None, format: str = None):
    global sessionHandler
    if not sessionHandler.authorizeToken(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return welcomemessage(format)


@zadanie3ruter.delete("/logout_session2", status_code=status.HTTP_303_SEE_OTHER)
def logout_session_withRedirect(format: str = None, session_token: str = Cookie(None)):
    global sessionHandler
    if not sessionHandler.authorizeCookie(session_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    sessionHandler.logoutCookie(session_token)
    return RedirectResponse(status_code=403,
                            url=f"https://daft-apka-jakubo.herokuapp.com/logged_out?format={format}")


@zadanie3ruter.delete("/logout_token2", status_code=status.HTTP_303_SEE_OTHER)
def logout_token_withRedirect(token: str = None, format: str = None):
    global sessionHandler
    if not sessionHandler.authorizeToken(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    sessionHandler.logoutToken(token)
    return RedirectResponse(status_code=403,
                            url=f"https://daft-apka-jakubo.herokuapp.com/logged_out?format={format}")


@zadanie3ruter.delete("/logout_session", status_code=200)
def logout_session(session_token: str = Cookie(None)):
    global sessionHandler
    if not sessionHandler.authorizeCookie(session_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    sessionHandler.logoutCookie(session_token)
    return


@zadanie3ruter.delete("/logout_token", status_code=200)
def logout_tokent(token: str = None):
    global sessionHandler
    if not sessionHandler.authorizeToken(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    sessionHandler.logoutToken(token)
    return


@zadanie3ruter.get("/logged_out", status_code=200)
def loggedout(format: str = None):
    if format == "json":
        return JSONResponse(status_code=200, content={"message": "Logged out!"})
    elif format == "html":
        return HTMLResponse(content="<h1>Logged out!</h1>")
    else:
        return PlainTextResponse(content="Logged out!")
