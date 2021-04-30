from hashlib import sha256
from datetime import datetime


class SessionKeyHandler:
    def __init__(self):
        self.cookies = list()
        self.tokens = list()
        self._secretkey = "Tajnekoddostarwarsilubieplackiivieratobyladobraadmin"

    def generateCookie(self):
        newcookie = sha256(f"{self._secretkey}cookie{datetime.now()}".encode()).hexdigest()
        self.cookies.append(newcookie)
        if len(self.cookies) > 3:
            self.cookies.pop(0)
        return newcookie

    def generateToken(self):
        newtoken = sha256(f"{self._secretkey}token{datetime.now()}".encode()).hexdigest()
        self.tokens.append(newtoken)
        if len(self.tokens) > 3:
            self.tokens.pop(0)
        return newtoken

    def authorizeCookie(self, cookie: str):
        return cookie is not None and cookie in self.cookies

    def authorizeToken(self, token: str):
        return token is not None and token in self.tokens

    def logoutCookie(self, cookie: str):
        self.cookies.pop(self.cookies.index(cookie))

    def logoutToken(self, token: str):
        self.tokens.pop(self.tokens.index(token))
