from fastapi import FastAPI, Path, Query

from src.contacts.routers import router as contacts_router
from src.auth.routers import router as auth_router

app = FastAPI()

app.include_router(contacts_router, prefix="/contacts", tags=["contacts"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/ping")
async def ping():
    return {"message": "pong"}
