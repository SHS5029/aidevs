# Assignment 05 Practice - Product Inventory Functions (GPT gen)

상품 목록을 여러 함수로 나누어 처리하는 연습 문제입니다.

## 과제 파일

```text
submissions/assignment05_product_functions.py
```

## 요구사항

아래 함수를 모두 만듭니다.

```text
get_stock_status(quantity)
is_available(quantity)
calculate_average_price(prices)
filter_available_products(products)
print_product(product)
```

## 함수 설명

```text
get_stock_status(quantity): 재고 수량에 따라 "충분", "부족", "품절"을 반환합니다.
  - 10개 이상: "충분"
  - 1개 이상 10개 미만: "부족"
  - 0개: "품절"

is_available(quantity): 재고가 1개 이상이면 True를 반환합니다.

calculate_average_price(prices): 가격 list를 받아 평균 가격을 반환합니다.

filter_available_products(products): 재고가 있는 상품 dict만 모아 list로 반환합니다.

print_product(product): 상품 이름, 가격, 재고 수량, 재고 상태, 구매 가능 여부를 출력합니다.
```

## 데이터 예시

```python
products = [
    {"name": "키보드", "price": 45000, "quantity": 12},
    {"name": "마우스", "price": 27000, "quantity": 4},
    {"name": "모니터", "price": 230000, "quantity": 0},
    {"name": "웹캠", "price": 68000, "quantity": 7},
]
```

## 프로그램에서 할 일

```text
1. 모든 상품 정보를 print_product()로 출력합니다.
2. filter_available_products()를 사용해 구매 가능한 상품 목록을 출력합니다.
3. 모든 상품의 평균 가격을 소수점 둘째 자리까지 출력합니다.
```

## 실행 결과 예시

```text
이름: 키보드
가격: 45000원
재고: 12개
재고 상태: 충분
구매 가능: True
----------------------------------------
구매 가능한 상품: 키보드, 마우스, 웹캠
평균 가격: 92500.00원
```

출력 문구와 줄바꿈은 원하는 방식으로 바꾸어도 됩니다.

## 추가 과제

`filter_below_average_products(products)` 함수를 만들어 평균 가격보다 저렴한 상품만 반환합니다.

## 확인 기준

```text
각 함수가 한 가지 역할만 담당하는가?
계산하거나 판정하는 함수가 결과를 return하는가?
filter_available_products()에서 is_available()을 재사용했는가?
print_product()에서 get_stock_status()와 is_available()을 재사용했는가?
상품 데이터가 바뀌어도 같은 함수들을 다시 사용할 수 있는가?
```
