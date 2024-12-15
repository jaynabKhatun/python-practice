from fastapi import APIRouter

entry_root = APIRouter()


@entry_root.get("/")
def apiGet():
    res = {
        "status": "Running",
        "message": "API is running successfully."

    }
    return res
