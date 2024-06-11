from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn

app = FastAPI()

db = [
    {"id": 1, "size": "s", "fuel": "gasoline", "doors": 3, "transmission": "auto"},
    {"id": 2, "size": "s", "fuel": "electric", "doors": 3, "transmission": "auto"},
    {"id": 3, "size": "s", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
    {"id": 4, "size": "m", "fuel": "electric", "doors": 3, "transmission": "auto"},
    {"id": 5, "size": "m", "fuel": "hybrid", "doors": 5, "transmission": "auto"},
    {"id": 6, "size": "m", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
    {"id": 7, "size": "l", "fuel": "diesel", "doors": 5, "transmission": "manual"},
    {"id": 8, "size": "l", "fuel": "electric", "doors": 5, "transmission": "auto"},
    {"id": 9, "size": "l", "fuel": "hybrid", "doors": 5, "transmission": "auto"}
]

@app.get('/date')
def date():
   return{'date': datetime.now()}

@app.get('/')
def hello(name):
   return {'hello': f'Hello, {name}'}

@app.get('/api/cars')
def get_cars(size: str|None = None, doors: int|None = None) -> list: 
   result = db
   if size and doors:
      result = [car for car in db if car['size'] == size and car['doors'] >= doors]
   return result

@app.get('/api/cars/{id}')
def  car_by_id(id: int) -> dict:
   result = [car for car in db if car['id'] == id]
   if result:
      return result[0] #retorna o primeiro elemento da lista, obs que todos os elementos da lista são dict
   else:
      raise HTTPException(status_code=404, detail=f"No car with id={id}")

if __name__ == "__main__":
   uvicorn.run("main:app", reload=True) 