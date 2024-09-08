from fastapi import FastAPI, APIRouter, Request, logger
from starlette.responses import RedirectResponse
import fastapi
from typing import Union
from pydantic import BaseModel

from dbManager import Database

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

@app.get("/OldDocs")
def OldDocs():
    return RedirectResponse("/docs")

@app.get("/openapi.json")
def get_open_api_endpoint():
    return RedirectResponse("/docs")

@app.get("/docs")
def get_docs():
    return RedirectResponse("/redoc")


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
        return {"Success": True, "Ip": user.ip}
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
        db.resetIP(Username, Status)
        return {"Success": True}
    else:
        return {"Success": False, "Reason": "Username Not Found"}