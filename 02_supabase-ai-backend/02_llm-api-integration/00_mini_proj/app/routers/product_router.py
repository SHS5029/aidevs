#product_router.py

from fastapi import APIRouter
from app.schemas.product_schema import ProductPublic
from app.services.product_service import product_create, product_get_all, product_get
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(".env"))

product_router = APIRouter()

@product_router.post("/product/create")
def create_product(product: ProductPublic) -> ProductPublic:
    """제품을 생성하는 엔드포인트입니다."""
    created_product = product_create(product)
    return created_product

@product_router.get("/product/get/{product_id}")
def get_product(product_id: int) -> ProductPublic:
    """특정 제품을 조회하는 엔드포인트입니다."""
    product = product_get(product_id)
    return product

@product_router.get("/product/get_all")
def get_all_products() -> list[ProductPublic]:
    """모든 제품을 조회하는 엔드포인트입니다."""
    products = product_get_all()
    return products