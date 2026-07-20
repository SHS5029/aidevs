from pydantic import BaseModel, Field


class Cart(BaseModel):
    id: str = Field(min_length=3, examples=["cart01"])
    customer_id: str = Field(min_length=3, examples=["id01"])
    product_id: str = Field(min_length=3, examples=["prd01"])
    quantity: int = Field(ge=1, examples=[2])

class Product(BaseModel):
    id: str = Field(min_length=3, examples=["prd01"])
    category: str = Field(min_length=1, examples=["전자제품"])
    name: str = Field(min_length=1, examples=["무선 키보드"])
    price: int = Field(ge=0, examples=[30000])
    stock: int = Field(ge=0, examples=[10])