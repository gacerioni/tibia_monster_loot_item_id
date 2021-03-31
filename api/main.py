from typing import Optional
from fastapi import FastAPI

from mongodb_tibia_db import get_all_tibia_itemid_from_collection

app = FastAPI()


@app.get("/")
def read_root():
    return "Tibia Monster and Item API, by Gabs the Creator!"


@app.get("/tibiaitems")
def get_all_tibia_items_from_mongodb_collection():
    itemid_list = get_all_tibia_itemid_from_collection()

    return {"all_tibia_items": itemid_list}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

