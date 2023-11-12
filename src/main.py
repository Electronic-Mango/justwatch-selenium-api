from os import getenv
from fastapi import FastAPI

from dotenv import load_dotenv
from justwatch import JustWatchApi

load_dotenv()
country = getenv("COUNTRY", "US")
just_watch = JustWatchApi(country)
app = FastAPI(docs_url="/")


@app.get("/search/{item_name}")
async def search(item_name: str):
    return just_watch.search(item_name)
