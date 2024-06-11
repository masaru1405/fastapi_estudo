from pydantic import BaseModel

class Car(BaseModel):
   id: int
   size: str
   fuel: str|None = 'eletric'  
   doors: int
   transmission: str|None = 'auto'