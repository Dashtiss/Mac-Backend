from fastapi import FastAPI, APIRouter, Request, logger
from starlette.responses import RedirectResponse
import fastapi
from typing import Union
from pydantic import BaseModel

from dbManager import Database, status
import requests
db = Database()

app = FastAPI(
    log_level=None,
)


# Define the API routes
app.title = "Laptop Server"
app.debug = True
app.openapi_url = "/openapi.json"
app.version = "1.1.0"
app.redoc_url = "/docs"
app.docs_url = "/Olddocs"
app.description = "Laptop Server API"


@app.get("/")
def read_root():
    """
    Simple endpoint to test the server is up.

    Returns:
    - dict: A dictionary containing a simple "Hello World" message.
    """
    return {"Hello": "World"}

@app.get("/ping")
def ping(request: Request):
    """
    Return the IP address of the client that made the request.

    Returns:
    - dict: A dictionary containing a boolean success status and the IP address of the client.
    """
    client_ip = request.client.host
    return {"Success": True, "Ip": client_ip}

@app.get("/Login")
def Login(Username:str, Ip: str) -> dict:
    """
    Check if a user is in the database and retrieve their IP address if they are.

    Args:
    - Username (str): The username to check.
    - Ip (str): The IP address to store for the user if they are not in the database already.

    Returns:
    - dict: A dictionary containing the success status of the operation and the IP address for the user if they were found.
    """
    user = db.getUser(Username)
    if user is not None:
        if user.ip == Ip:
            return {"Success": True, "Ip": Ip}
        else:
            db.resetIP(Username, Ip)
            return {"Success": True, "Ip": Ip, "Reason": "IP Changed"}
    else:
        return {"Success": False, "Reason": "User Not Found"}


@app.get("/AddUser")
def AddUser(
    Username: str, 
    Ip: str
) -> dict:
    """
    Adds a new user to the database.

    Args:
    - Username (str): The username of the user to add.
    - Ip (str): The IP address of the user to add.

    Returns:
    - dict: A dictionary containing the success status of the operation.
    """
    users = db.listUsers()
    if users is not None:
        for user in users:
            if user["username"] == Username:
                return {"Success": False, "Reason": "Username Already Exists"}
    db.addUser(Username, Ip)
    return {"Success": True}
    

@app.get("/ResetIP")
def ResetIP(Username:str, NewIp: str) -> dict:
    """
    Resets the IP address of a user in the database.

    Args:
    - Username (str): The username of the user to reset the IP address for.
    - NewIp (str): The new IP address to store for the user.

    Returns:
    - dict: A dictionary containing the success status of the operation.
    """
    user = db.getUser(Username)
    if user is not None:
        db.resetIP(Username, NewIp)
        return {"Success": True}
    else:
        return {"Success": False, "Reason": "Username Not Found"}
    
@app.get("/SetStatus")
def SetStatus(Username:str, Status: str) -> dict:
    """
    Sets the status of a user in the database.

    Args:
    - Username (str): The username of the user to set the status for.
    - Status (str): The new status to store for the user.

    Returns:
    - dict: A dictionary containing the success status of the operation.
    """
    user = db.getUser(Username)
    if user is not None:
        if Status.lower() in ["online", "offline", "unknown"]:
            db.resetStatus(Username, Status)
            return {"Success": True}
        else:
            return {"Success": False, "Reason": "Invalid Status"}
    else:
        return {"Success": False, "Reason": "Username Not Found"}
    
@app.get("/Panel")
def Panel() -> dict:
    """
    Returns a list of all users in the database.

    Returns:    
    - dict: A dictionary containing the success status of the operation and a list of all users in the database.
    """
    users = db.listUsers()
    if users is not None:
        return {"Success": True, "Users": users}
    else:
        return {"Success": False, "Reason": "No Users Found"}
    
@app.get("/sendCommand")
def sendCommand(Username: str, Command: str) -> dict:
    """
    Sends a command to a user in the database.

    Args:
    - Username (str): The username of the user to send the command to.
    - Command (str): The command to send to the user.

    Returns:
    - dict: A dictionary containing the success status of the operation.
    """
    user = db.getUser(Username)
    if user is not None:
        if user.status == status.online:
            r = requests.get(f"http://{user.ip}/{Command}")
            return {"Success": True, "Response": r.status_code}
        else:
            return {"Success": False, "Reason": "User is offline"}
    else:
        return {"Success": False, "Reason": "Username Not Found"}