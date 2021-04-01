from typing import Optional
from fastapi import FastAPI, Query

from mongodb_tibia_db import get_all_tibia_itemid_from_collection, get_tibia_item_by_id_from_collection, \
    get_tibia_item_by_name_from_collection

app = FastAPI()


@app.get("/")
def read_root():
    return "Tibia Monster and Item API, by Gabs the Creator!"


@app.get("/tibiaitems")
def get_all_tibia_items_from_mongodb_collection():
    itemid_list = get_all_tibia_itemid_from_collection()

    return {"all_tibia_items": itemid_list}


@app.get("/tibiaitems/id/{item_id}")
async def read_item(item_id: int, q: Optional[str] = Query("defaultquery", max_length=500)):
    result = get_tibia_item_by_id_from_collection(item_id)

    return result

    # if q:
    #    return {"item_id": item_id, "q": q}
    # return {"item_id": item_id}


@app.get("/tibiaitems/name/{item_name}")
async def read_item(item_name: str, q: Optional[str] = Query("defaultquery", max_length=500)):
    result = get_tibia_item_by_name_from_collection(item_name)

    return result
