from fastapi import FastAPI
import uvicorn
import core.database as database
import os, logging
from chat.routers import router as chat_router
from auth.routers import router as auth_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")


app = FastAPI()
database.create_tables()


app.include_router(auth_router, tags=["auth"])
app.include_router(chat_router, tags=["chat"])  

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)