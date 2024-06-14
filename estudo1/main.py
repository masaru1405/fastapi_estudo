from fastapi import FastAPI, HTTPException
from datetime import datetime
from schemas import load_db, save_db, CarInput, CarOutput
import uvicorn

app = FastAPI()

db = load_db()

@app.get('/date')
def date():
   return{'date': datetime.now()}

@app.get('/')
def hello(name):
   return {'hello': f'Hello, {name}'}

#/api/cars?size=m&doors=3
@app.get('/api/cars')
def get_cars(size: str|None = None, doors: int|None = None) -> list: 
   result = db
   print(size, doors)
   if size and doors:
      result = [car for car in db if car.size == size and car.doors >= doors]
   return result

@app.get('/api/cars/{id}')
def  car_by_id(id: int) -> dict:
   result = [car for car in db if car['id'] == id]
   if result:
      return result[0] #retorna o primeiro elemento da lista, obs que todos os elementos da lista são dict
   else:
      raise HTTPException(status_code=404, detail=f"No car with id={id}")

#response_model é um argumento do decorator e não da função. FastAPI irá fazer a validação da saída e fará a conversão quando necessário.
#OBS: def nomeFuncao(argumentos) -> tipoDeSaida; o FastAPI não utiliza o type hint de saída da função (neste caso especificado como 'tipoDeSaida')
@app.post('/api/cars/', response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
   new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, transmission=car.transmission, id=len(db)+1)
   
   db.append(new_car) 
   save_db(db)
   return new_car

@app.put('/api/cars/{id}', response_model=CarOutput)
def change_car(id: int, new_data: CarInput) -> CarOutput:
   matches = [car for car in db if car.id == id]
   if matches:
      car = matches[0]
      car.fuel = new_data.fuel
      car.transmission = new_data.transmission
      car.size = new_data.size
      car.doors = new_data.doors
      save_db(db)
      return car
   else:
      return HTTPException(status_code=404, detail=f"No car with id={id}")

@app.delete('/api/cars/{id}', status_code=204)
def remove_car(id: int) -> None:
   matches = [car for car in db if car.id == id]
   if matches:
      car = matches[0]
      db.remove(car)
      save_db(db)
   else:
      return HTTPException(status_code=404, detail=f"No car with id={id}")

if __name__ == "__main__":
   uvicorn.run("main:app", reload=True) 