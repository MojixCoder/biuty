from fastapi import HTTPException


PERMISSION_DENIED = HTTPException(status_code=403, detail="Permission denied.")
NOT_FOUND = HTTPException(status_code=404, detail="Not found.")
CONFLICT = HTTPException(status_code=409, detail="Conflict.")
BAD_REQUEST = HTTPException(status_code=400, detail="Bad request.")
UNAUTHORIZED = HTTPException(
    status_code=401,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)
