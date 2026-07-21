from pydantic import BaseModel

class ProductPublic(BaseModel):
    id: int
    name: str
    price: int

