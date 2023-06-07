"""Main Lambda function for the API."""
import json
from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_engine.engine import text_to_link
from amazon_scrapper.http_client import get_search_page_data

origins = [
    "*",
]


class Text(BaseModel):
    """Text to be converted to link"""
    text: str

class Link(BaseModel):
    """Link returned"""
    amazon_link: str

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
    """Root endpoint"""
    return {"message": "Welcome to my bookstore app!"}

@app.post("/amazon")
async def amazon(text: Text):
    """Get Amazon link from text"""

    text_dict = text.dict()

    amazon_link = text_to_link(text_dict['text'])

    return {"amazon_link": amazon_link}

@app.post("/get-amazon-page-data")
async def get_amazon_page_data(link: Link):
    """Get Amazon page data"""   
    link_dict = link.dict()

    amazon_link = link_dict['amazon_link']

    print(amazon_link)

    amazon_page_data = get_search_page_data(amazon_link)

    # return  amazon_page_data
    return jsonable_encoder(amazon_page_data)


    