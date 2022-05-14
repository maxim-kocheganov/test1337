from fastapi import FastAPI
import asyncio
import aioredis

from app import database as db
from sqlalchemy.orm import Session
from app.database import Item, engine
from sqlalchemy import null
from sqlalchemy import func
from app.settings import REDIS_URL

app = FastAPI()

def anagramCheck(str1,str2):
    if sorted(str1) == sorted(str2):
        return True
    else:
        return False

async def inc():
    redis = aioredis.from_url(REDIS_URL) #Place your ip
    #await redis.set("my-key", "value")
    #Evalue = await redis.get("my-key")
    res = await redis.incr("countOfAn")
    return res

@app.get("/anagram/")
async def read_item(str1: str = "", str2: str = ""):
    anagram = anagramCheck(str1,str2)
    if anagram:
        count = await inc()
        return {'anagram':'true', 'count':count}
    else:
        return {'anagram':'false'}

@app.get("/newmac/",status_code=201)
async def add_mac():
    for i in range(10):
        with Session(engine) as session:
            item = db.Item()
            item.setRandType()
            item.setRandId()            
            if i < 5:
                endpoint = db.Endpoint()
                session.add(endpoint)
                session.flush()               
                item.endpoint_id = endpoint.id
            session.add(item)
            session.commit()
    return {'mac':'success'}

@app.get("/endpoint/")
async def enpoint():
    countArr = []
    with Session(engine) as session:
        allTypes = session.query(Item).distinct(Item.dev_type).all()
        for _type in allTypes:
            typeStr = _type.dev_type
            count = session.query(Item).filter(Item.dev_type == typeStr).count()
            countArr.append({typeStr:count})
    return {'endpoints':countArr}