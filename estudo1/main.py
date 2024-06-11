from fastapi import FastAPI, HTTPException
from datetime import datetime
from schemas import load_db
import uvicorn

app = FastAPI()

db = load_db()

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