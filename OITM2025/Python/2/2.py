from pydantic import BaseModel

class Car(BaseModel):
    id: int
    manufacturer: str = "Anonymous"

u = Car(id="123")
print(u.model_dump())
