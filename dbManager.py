from tinydb import TinyDB, Query
from dataclasses import dataclass
from pydantic import BaseModel



class status:
    """
    Enum for the status of a user.

    Attributes:
    - unknown (str): The status of an unknown user.
    - online (str): The status of an online user.
    - offline (str): The status of an offline user.
    """
    unknown: str = "unknown"
    online: str = "online"
    offline: str = "offline"
    
    
@dataclass
class User:
    """
    Represents a user in the database.

    Attributes:
    - username (str): The username of the user.
    - ip (str): The IP address of the user.
    - status (status): The status of the user.
    """
    username: str
    ip: str
    status: status | str


class Database:
    def __init__(self, dbName: str = "db", dbType: str = "json") -> None:
        self.db = TinyDB(f"{dbName}.{dbType}")

        self.users = self.db.table('users')
        
        self.query = Query()

        for user in self.users:
            self.users.update({"status": status.offline}, self.query.username == user["username"])
            
            
    def addUser(self, username: str, ip: str, status: status = status.unknown):
        self.users.insert({"username": username, "ip": ip, "status": status} )
        
    def getUser(self, username: str) -> User:
        user = self.users.search(self.query.username == username)
        try:
            if len(user) == 0:
                return None
            else:
                return User(user[0]["username"], user[0]["ip"], user[0]["status"] if "status" in user[0] else status.unknown)
        except IndexError:
            return None, IndexError

    def listUsers(self) -> list:
        return self.users.all()

    def resetIP(self, username: str, ip: str):
        self.users.update({"ip": ip}, self.query.username == username)
    
    def resetStatus(self, username: str, status: status):
        self.users.update({"status": status}, self.query.username == username)
