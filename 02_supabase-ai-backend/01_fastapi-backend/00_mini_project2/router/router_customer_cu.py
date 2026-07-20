from fastapi import APIRouter
# router/router_customer_cu.py
# router/router_customer_rd.py
from schema.model_customer import Customer
from schema.model_common import ApiResponse

router_cu = APIRouter()

# Request Body
# insert, update
@router_cu.post("/register")
async def register(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    response = None
    response = ApiResponse(
        success = True,
        message = f"{customer.name} 가입축하!",
    )
    return response

@router_cu.get("/health")
def health():
    response = ApiResponse(
        success=True,
        message="OK",
    )
    return response
