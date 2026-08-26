"""stdio로 실행되는 스마트냉장고 MCP Server입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "travel-tools",
    instructions="stdio로 실행되는 스마트냉장고 MCP Server입니다.",
)


@mcp.tool()
def get_foods() -> dict:
    foods = [
        {"name": "배추", "calories": 20, "expiration_days": "2026-08-31"},
        {"name": "무", "calories": 15, "expiration_days": "2026-09-10"},
        {"name": "당근", "calories": 25, "expiration_days": "2026-09-05"},
        {"name": "양배추", "calories": 30, "expiration_days": "2026-09-07"},
        {"name": "상추", "calories": 18, "expiration_days": "2026-08-30"},
        {"name": "깻잎", "calories": 22, "expiration_days": "2026-08-29"},
        {"name": "시금치", "calories": 19, "expiration_days": "2026-08-28"},
        {"name": "대파", "calories": 14, "expiration_days": "2026-09-02"},
        {"name": "쪽파", "calories": 12, "expiration_days": "2026-08-27"},
        {"name": "양파", "calories": 40, "expiration_days": "2026-09-15"},
        {"name": "마늘", "calories": 15, "expiration_days": "2026-09-18"},
        {"name": "생강", "calories": 20, "expiration_days": "2026-09-20"},
        {"name": "고추", "calories": 30, "expiration_days": "2026-09-04"},
        {"name": "청양고추", "calories": 35, "expiration_days": "2026-09-03"},
        {"name": "토마토", "calories": 18, "expiration_days": "2026-08-30"},
        {"name": "오이", "calories": 16, "expiration_days": "2026-08-29"},
        {"name": "콩나물", "calories": 20, "expiration_days": "2026-08-27"},
        {"name": "버섯", "calories": 22, "expiration_days": "2026-09-08"},
        {"name": "표고버섯", "calories": 28, "expiration_days": "2026-09-12"},
        {"name": "새송이버섯", "calories": 26, "expiration_days": "2026-09-09"},
        {"name": "감자", "calories": 77, "expiration_days": "2026-09-25"},
        {"name": "고구마", "calories": 86, "expiration_days": "2026-09-30"},
        {"name": "브로콜리", "calories": 34, "expiration_days": "2026-09-01"},
        {"name": "애호박", "calories": 20, "expiration_days": "2026-08-31"},
        {"name": "호박", "calories": 26, "expiration_days": "2026-09-06"},
        {"name": "피망", "calories": 31, "expiration_days": "2026-09-02"},
        {"name": "파프리카", "calories": 32, "expiration_days": "2026-09-05"},
        {"name": "아스파라거스", "calories": 24, "expiration_days": "2026-08-30"},
        {"name": "콩", "calories": 130, "expiration_days": "2026-09-28"},
        {"name": "두부", "calories": 76, "expiration_days": "2026-08-28"},
        {"name": "계란", "calories": 155, "expiration_days": "2026-09-15"},
        {"name": "우유", "calories": 62, "expiration_days": "2026-08-30"},
        {"name": "요거트", "calories": 70, "expiration_days": "2026-08-29"},
        {"name": "치즈", "calories": 114, "expiration_days": "2026-09-13"},
        {"name": "김치", "calories": 20, "expiration_days": "2026-10-05"},
        {"name": "된장", "calories": 40, "expiration_days": "2026-10-20"},
        {"name": "고추장", "calories": 50, "expiration_days": "2026-10-18"},
        {"name": "참기름", "calories": 120, "expiration_days": "2026-11-10"},
        {"name": "들기름", "calories": 120, "expiration_days": "2026-11-07"},
        {"name": "돼지고기", "calories": 242, "expiration_days": "2026-08-27"},
        {"name": "소고기", "calories": 250, "expiration_days": "2026-08-28"},
        {"name": "닭고기", "calories": 165, "expiration_days": "2026-08-30"},
        {"name": "오리고기", "calories": 337, "expiration_days": "2026-08-29"},
        {"name": "양고기", "calories": 294, "expiration_days": "2026-08-31"},
        {"name": "베이컨", "calories": 541, "expiration_days": "2026-09-03"},
        {"name": "햄", "calories": 145, "expiration_days": "2026-09-05"},
        {"name": "소시지", "calories": 301, "expiration_days": "2026-09-04"},
        {"name": "훈제오리", "calories": 318, "expiration_days": "2026-09-06"},
        {"name": "닭가슴살", "calories": 109, "expiration_days": "2026-09-02"},
        {"name": "참치캔", "calories": 198, "expiration_days": "2027-08-20"},
        {"name": "어묵", "calories": 110, "expiration_days": "2026-09-01"},
        {"name": "만두", "calories": 220, "expiration_days": "2026-10-15"},
        {"name": "냉동피자", "calories": 266, "expiration_days": "2026-11-01"},
        {"name": "라면", "calories": 500, "expiration_days": "2027-02-28"},
        {"name": "우유", "calories": 62, "expiration_days": "2026-08-24"},
        {"name": "두부", "calories": 76, "expiration_days": "2026-08-25"},
        {"name": "딸기", "calories": 32, "expiration_days": "2026-08-23"},
        {"name": "바나나", "calories": 89, "expiration_days": "2026-08-22"},
        {"name": "아보카도", "calories": 160, "expiration_days": "2026-08-26"},
        {"name": "망고", "calories": 60, "expiration_days": "2026-08-24"},
        {"name": "파파야", "calories": 43, "expiration_days": "2026-08-25"},
        {"name": "패션프루트", "calories": 97, "expiration_days": "2026-08-24"},
        {"name": "용과", "calories": 57, "expiration_days": "2026-08-25"},
        {"name": "코코넛", "calories": 354, "expiration_days": "2026-08-30"},
        {"name": "라임", "calories": 30, "expiration_days": "2026-08-27"},
        {"name": "레몬그라스", "calories": 99, "expiration_days": "2026-09-01"},
        {"name": "고수", "calories": 23, "expiration_days": "2026-08-26"},
        {"name": "바질", "calories": 23, "expiration_days": "2026-08-27"},
        {"name": "민트", "calories": 44, "expiration_days": "2026-08-28"},
        {"name": "할라피뇨", "calories": 29, "expiration_days": "2026-08-29"},
        {"name": "타마린드", "calories": 239, "expiration_days": "2026-09-05"},
        {"name": "병아리콩", "calories": 164, "expiration_days": "2026-09-10"},
        {"name": "퀴노아", "calories": 120, "expiration_days": "2027-01-15"},
        {"name": "렌틸콩", "calories": 116, "expiration_days": "2027-02-01"},
        {"name": "쿠스쿠스", "calories": 112, "expiration_days": "2027-01-20"},
        {"name": "사프란", "calories": 310, "expiration_days": "2027-03-15"},
        {"name": "카다멈", "calories": 311, "expiration_days": "2027-03-20"},
    ]
    return {"items": foods, "source": "smart-fridge-food-catalog"}

## 툴
## 재료목록, 레시피, 칼로리, 유통기한 ) 조회 툴



@mcp.tool()
def get_recipes(
    ingredients: list[str],
    max_calories: int = 500,
) -> dict:
    """재료와 최대 칼로리로 레시피를 검색합니다."""
    if not ingredients:
        raise ValueError("ingredients는 빈 리스트일 수 없습니다.")
    if max_calories < 1:
        raise ValueError("max_calories는 1 이상이어야 합니다.")
    recipes = [
        {"name": "김치찌개", "ingredients": ["배추", "무", "당근"], "calories": 400, "difficulty": "쉬움", "cooking_time_minutes": 30},
        {"name": "된장찌개", "ingredients": ["배추", "무"], "calories": 300, "difficulty": "쉬움", "cooking_time_minutes": 25},
        {"name": "계란말이", "ingredients": ["계란", "대파", "당근"], "calories": 280, "difficulty": "보통", "cooking_time_minutes": 20},
        {"name": "토마토 달걀볶음", "ingredients": ["토마토", "계란", "양파"], "calories": 320, "difficulty": "쉬움", "cooking_time_minutes": 15},
        {"name": "두부조림", "ingredients": ["두부", "대파", "마늘", "고추장"], "calories": 360, "difficulty": "보통", "cooking_time_minutes": 30},
        {"name": "감자조림", "ingredients": ["감자", "양파", "마늘"], "calories": 290, "difficulty": "쉬움", "cooking_time_minutes": 35},
        {"name": "닭가슴살 샐러드", "ingredients": ["닭가슴살", "상추", "토마토", "오이"], "calories": 260, "difficulty": "쉬움", "cooking_time_minutes": 15},
        {"name": "돼지고기 김치볶음", "ingredients": ["돼지고기", "김치", "양파", "대파"], "calories": 470, "difficulty": "보통", "cooking_time_minutes": 25},
        {"name": "소고기 버섯볶음", "ingredients": ["소고기", "버섯", "양파", "마늘"], "calories": 450, "difficulty": "보통", "cooking_time_minutes": 20},
        {"name": "브로콜리 두부무침", "ingredients": ["브로콜리", "두부", "참기름"], "calories": 240, "difficulty": "쉬움", "cooking_time_minutes": 15},
        {"name": "콩나물국", "ingredients": ["콩나물", "대파", "마늘"], "calories": 180, "difficulty": "쉬움", "cooking_time_minutes": 20},
        {"name": "오이무침", "ingredients": ["오이", "고추", "마늘", "참기름"], "calories": 170, "difficulty": "쉬움", "cooking_time_minutes": 10},
        {"name": "버섯계란국", "ingredients": ["버섯", "계란", "대파"], "calories": 210, "difficulty": "쉬움", "cooking_time_minutes": 20},
        {"name": "고구마 샐러드", "ingredients": ["고구마", "요거트", "상추"], "calories": 340, "difficulty": "쉬움", "cooking_time_minutes": 20},
        {"name": "참치김치볶음밥", "ingredients": ["참치캔", "김치", "양파", "계란"], "calories": 490, "difficulty": "보통", "cooking_time_minutes": 25},
        {"name": "애호박전", "ingredients": ["애호박", "계란", "부침가루"], "calories": 350, "difficulty": "보통", "cooking_time_minutes": 25},
        {"name": "코코넛 닭가슴살 카레", "ingredients": ["닭가슴살", "코코넛", "감자", "양파", "고추"], "calories": 420, "difficulty": "보통", "cooking_time_minutes": 40},
        {"name": "망고 아보카도 살사", "ingredients": ["망고", "아보카도", "토마토", "라임", "고수"], "calories": 230, "difficulty": "쉬움", "cooking_time_minutes": 15},
        {"name": "타마린드 돼지고기 볶음", "ingredients": ["돼지고기", "타마린드", "양파", "할라피뇨", "고수"], "calories": 460, "difficulty": "보통", "cooking_time_minutes": 30},
        {"name": "사프란 해산물풍 버섯 리소토", "ingredients": ["사프란", "버섯", "표고버섯", "양파", "치즈"], "calories": 480, "difficulty": "어려움", "cooking_time_minutes": 45},
        {"name": "파파야 오리 가슴살 샐러드", "ingredients": ["오리고기", "파파야", "상추", "라임", "민트"], "calories": 390, "difficulty": "보통", "cooking_time_minutes": 25},
        {"name": "깻잎 페스토 퀴노아 볼", "ingredients": ["퀴노아", "깻잎", "바질", "마늘", "파프리카"], "calories": 360, "difficulty": "보통", "cooking_time_minutes": 30},
        {"name": "용과 요거트 카르파초", "ingredients": ["용과", "요거트", "민트", "라임"], "calories": 190, "difficulty": "쉬움", "cooking_time_minutes": 10},
        {"name": "카다멈 고구마 수프", "ingredients": ["고구마", "우유", "카다멈", "양파"], "calories": 310, "difficulty": "보통", "cooking_time_minutes": 35},
    ]
    matches = [
        recipe for recipe in recipes
        if all(item in ingredients for item in recipe["ingredients"]) and recipe["calories"] <= max_calories
    ]
    return {"items": matches, "source": "smart-fridge-recipe-catalog"}


@mcp.resource("smart-fridge://knowledge/professional-cooking")
def professional_cooking_knowledge() -> str:
    """전문 요리 지식과 기본 조리 원칙을 제공합니다."""
    return """# 전문 요리 지식

## 기본 조리 원칙
- 재료는 조리 전 충분히 세척하고, 육류·채소용 도마와 칼을 구분합니다.
- 육류와 가금류는 중심부까지 완전히 익히고, 조리 후에는 즉시 냉장 보관합니다.
- 소금은 조리 초반에 재료의 간을 맞추고, 산미(레몬·식초)는 마무리에 더해 풍미를 살립니다.

## 채소 조리
- 잎채소는 센 불에 짧게 조리해 색과 식감을 유지합니다.
- 뿌리채소는 크기를 균일하게 썰어 익는 시간을 맞춥니다.
- 버섯은 팬을 과도하게 채우지 않고 수분이 증발할 때까지 볶습니다.

## 국물과 볶음
- 볶음 요리는 팬을 충분히 예열한 뒤 재료를 나누어 넣어 수분이 생기지 않게 합니다.
- 찌개와 국은 단단한 재료부터 넣고, 향채는 마무리 단계에 넣어 향을 보존합니다.
- 참기름과 들기름은 향이 날아가기 쉬우므로 불을 끈 뒤 넣는 것이 좋습니다.
"""


if __name__ == "__main__":
    print("MCP Server를 stdio로 실행합니다. Ctrl+C로 종료합니다.")
    mcp.run(transport="stdio")
