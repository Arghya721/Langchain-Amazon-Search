"""Main Lambda function for the API."""
import json
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore app!"}

@app.get("/amazon")
async def amazon():
    return {"message": "Welcome to my amazon smart search!"}