"""
uvicorn main:app --reload
"""

from fastapi import FastAPI
# main.py
from router.router_customer_cu import router_cu
from router.router_customer_rd import router_rd


app = FastAPI(
    title = "Request Test",
    description = "request test",
)

app.include_router(router_cu)
app.include_router(router_rd)