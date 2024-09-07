from tinydb import TinyDB, Query
from dataclasses import dataclass
db = TinyDB('db.json')

users = db.table('users')

query = Query()

@dataclass
class User:
    username: str
    ip: str


def addUser(username: str, ip: str):
    users.insert({"username": username, "ip": ip})
    
def getUser(username: str) -> User:
    user = users.search(query.username == username)
    if len(user) == 0:
        return None
    else:
        return User(user[0]["username"], user[0]["ip"])

def listUsers() -> list:
    return users.all()

def resetIP(username: str, ip: str):
    users.update({"ip": ip}, query.username == username)
