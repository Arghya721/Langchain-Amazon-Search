"""Main Lambda function for the API."""
import json
from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from langchain_engine.engine import text_to_link
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*",
]


class Text(BaseModel):
    """Text to be converted to link"""
    text: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore app!"}

@app.post("/amazon")
async def amazon(text: Text):
    """Get Amazon link from text"""

    text_dict = text.dict()

    amazon_link = text_to_link(text_dict['text'])

    return {"amazon_link": amazon_link}


    