from fastapi import FastAPI
from app.routers import chat_router, product_router
#from app.services import chat_service
from app.schemas import ChatSchema

app = FastAPI(title="Main App")

app.include_router(chat_router.chat_router)
app.include_router(product_router.product_router)