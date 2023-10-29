from fastapi import FastAPI
import redis
import requests
from dotenv import load_dotenv
import os

load_dotenv()  

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

r = redis.Redis(host=REDIS_HOST, port=REDIS_HOST, decode_responses=True)

app = FastAPI()


@app.get("/rate")
async def getData():
  
  rate = r.get('rate')

  if not rate:
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url)
    data = response.json()
    rate = data["bpi"]["USD"]["rate"]
    r.setex('rate', 10, rate)

  return rate


