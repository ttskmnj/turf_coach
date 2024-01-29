from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from routes import router


load_dotenv()
MONGODB_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv('MONGO_INITDB_DATABASE')

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGODB_URL)
    app.database = app.mongodb_client[MONGO_DB]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(router, tags=["pitch"], prefix="/pitch")
