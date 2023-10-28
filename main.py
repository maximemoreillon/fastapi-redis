from fastapi import FastAPI
import redis
import requests

r = redis.Redis(host='localhost', port=30379, decode_responses=True)

app = FastAPI()


@app.get("/rate")
async def getData():
  
  rate = r.get('rate')

  if not rate:
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    rate = data["bpi"]["USD"]["rate"]
    r.setex('rate', 10, rate)

  return rate


