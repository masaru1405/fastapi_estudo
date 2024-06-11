import json
from pydantic import BaseModel

class Car(BaseModel):
   id: int
   size: str
   fuel: str|None = 'eletric'  
   doors: int
   transmission: str|None = 'auto'


def load_db() -> list[Car]:
   """Load a list of Car objects from a JSON file"""
   with open("cars.json") as f:
      return [Car.model_validate(obj) for obj in json.load(f)]