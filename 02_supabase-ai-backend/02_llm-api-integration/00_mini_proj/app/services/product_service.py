#product service.py 
# 입력, 전체 조회, 한 개 조회

from app.schemas.product_schema import ProductPublic

def product_create(product: ProductPublic) -> ProductPublic:
    print("DB에 입력이처리됩니다")
    return product

def product_get_all() -> list[ProductPublic]:
    result = []
    result.append(ProductPublic(id=1, name="Sample Product", price=100))
    result.append(ProductPublic(id=2, name="Sample Product 2", price=200))
    result.append(ProductPublic(id=3, name="Sample Product 3", price=300))
    return result

def product_get(product_id: int) -> ProductPublic:
    get_product = ProductPublic(
        id = product_id, name="Sample Product", price=30000
    )
    return get_product