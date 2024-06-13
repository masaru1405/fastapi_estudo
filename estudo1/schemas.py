import json
from pydantic import BaseModel

#Para add um novo carro (put)
class CarInput(BaseModel):
   size: str
   fuel: str|None = 'eletric'  
   doors: int
   transmission: str|None = 'auto'

#Para retornar um carro (get)
class CarOutput(CarInput):
   id: int


def load_db() -> list[CarOutput]:
   """Load a list of Car objects from a JSON file"""
   with open("cars.json") as f:
      return [CarOutput.model_validate(obj) for obj in json.load(f)]

def save_db(cars: list[CarInput]):
   with open("cars.json", 'w') as f:
      json.dump([car.model_dump() for car in cars], f, indent=4) #para add um car, reescreve todos os outros?