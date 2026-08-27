"""대상 여행지의 명소 정보를 조회하는 MCP 서버 예제입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "landmark",
    instructions="도시와 가격 조건으로 명소를 검색하고 명소별 정보를 제공합니다.",
)

LANDMARK = [
    {
        "landmark_id": "landmark-busan-001",
        "name": "해운대",
        "city": "부산",
        "price": 120_000,
    },
    {
        "landmark_id": "landmark-busan-002",
        "name": "광안리",
        "city": "부산",
        "price": 170_000,
    },
    {
        "landmark_id": "landmark-seoul-001",
        "name": "경복궁",
        "city": "서울",
        "price": 140_000,
    },
]

CANCELLATION_POLICIES = {
    "landmark-busan-001": "체크인 3일 전까지 취소하면 전액 환불합니다.",
    "landmark-busan-002": "체크인 7일 전까지 취소하면 전액 환불합니다.",
    "landmark-seoul-001": "체크인 2일 전까지 취소하면 전액 환불합니다.",
}


@mcp.tool()
def search_landmarks(
    city: Literal["부산", "서울"],
    max_price: int = 150_000,
) -> dict:
    """도시와 가격 조건으로 명소를 검색합니다."""
    if max_price < 1:
        raise ValueError("max_price는 1 이상이어야 합니다.")
    matches = [
        landmark for landmark in LANDMARK
        if landmark["city"] == city and landmark["price"] <= max_price
    ]
    return {"items": matches, "source": "lab-landmark-catalog"}


@mcp.tool()
def get_cancellation_policy(landmark_id: str) -> dict:
    """명소 검색 결과의 landmark_id로 해당 명소의 취소 규정을 조회합니다."""
    policy = CANCELLATION_POLICIES.get(landmark_id)
    if policy is None:
        raise ValueError(f"존재하지 않는 landmark_id입니다: {landmark_id}")
    landmark = next(landmark for landmark in LANDMARK if landmark["landmark_id"] == landmark_id)
    return {
        "landmark_id": landmark_id,
        "landmark_name": landmark["name"],
        "policy": policy,
        "source": "lab-landmark-policy-service",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
