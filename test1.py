from fastapi import FastAPI
import asyncio
import aioredis

app = FastAPI()

def anagramCheck(str1,str2):
    if sorted(str1) == sorted(str2):
        return True
    else:
        return False

async def inc():
    redis = aioredis.from_url("redis://192.168.0.102") #Place your ip
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