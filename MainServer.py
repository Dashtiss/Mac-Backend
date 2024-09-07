from fastapi import FastAPI, APIRouter, Request
from starlette.responses import RedirectResponse
import fastapi
from typing import Union
from pydantic import BaseModel
import dbManager as db

app = FastAPI()

# Define the API routes
app.title = "Laptop Server"
app.debug = True
app.openapi_url = "/openapi.json"
app.version = "1.1.0"
app.redoc_url = "/redoc"
app.docs_url = "/docs"
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
    if db.isAllowed(Username):
        return {"Success": True, "Ip": db.getUser(Username)["ip"]}
    else:
        return {"Success": False, "Reason": "Wrong Username"}


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
    if not db.isAllowed(Username):
        # Add the user to the database
        db.addUser(Username, Ip)
        return {"Success": True}
    else:
        # Return an error if the user already exists
        return {"Success": False, "Reason": "Username Already Exists"}
    

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