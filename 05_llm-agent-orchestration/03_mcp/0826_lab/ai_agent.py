
import asyncio
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import AsyncOpenAI

from _stdio_client import connect_to_travel_server


ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
INSTRUCTIONS = (
    "당신은 냉장고 재료 기반 레시피 추천 AI입니다.\n"
    "목표: 사용자가 가진 재료로 만들 수 있는 최적의 레시피를 찾습니다.\n"
    "규칙:\n"
    "1) 레시피 추천 시 mcp_server.py 도구가 제공하는 레시피를 최우선으로 사용합니다. "
    "도구에서 제공되지 않는 레시피 정보를 부득이하게 사용할 경우, 해당 레시피명 옆에 반드시 '(인터넷참조)'라고 표시합니다.\n"
    "2) 사실을 꾸며내지 말고, 도구 결과에 근거해 답변합니다. 조리법은 생략합니다.\n"
)


def to_openai_tool(tool) -> dict[str, Any]:
    """MCP Tool Schema를 OpenAI Responses API의 Function Tool로 변환합니다."""
    raw = tool.model_dump(by_alias=True)
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": raw["inputSchema"],
        "strict": False,
    }


def text_result(result) -> str:
    return "\n".join(
        content.text for content in result.content if hasattr(content, "text")
    )


async def answer(question: str) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 필요합니다.")

    trace: list[dict[str, Any]] = []

    async with AsyncOpenAI() as client, connect_to_travel_server() as session:
        discovered = (await session.list_tools()).tools
        available = {tool.name for tool in discovered}
        openai_tools = [to_openai_tool(tool) for tool in discovered]
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            input=question,
            tools=openai_tools,
            parallel_tool_calls=True,
        )

        tool_calls = [item for item in response.output if item.type == "function_call"]
        if not tool_calls:
            return {
                "question": question,
                "model": OPENAI_MODEL,
                "discovered_tools": sorted(available),
                "llm_calls": 1,
                "trace": trace,
                "answer": response.output_text,
            }

        tool_outputs = []
        for call in tool_calls:
            if call.name not in available:
                raise ValueError(f"MCP Server가 제공하지 않는 Tool입니다: {call.name}")
            arguments = json.loads(call.arguments)
            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments는 JSON Object여야 합니다.")

            result = await session.call_tool(call.name, arguments)
            result_text = text_result(result)
            trace.append({
                "tool": call.name,
                "arguments": arguments,
                "is_error": bool(result.isError),
                "result": result_text,
            })
            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result_text,
            })

        final_response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
        )
        return {
            "question": question,
            "model": OPENAI_MODEL,
            "discovered_tools": sorted(available),
            "llm_calls": 2,
            "trace": trace,
            "answer": final_response.output_text,
        }


async def main() -> None:
#    result = await answer("부산 오늘 날씨 알려줘")
    result = await answer("한식 먹을래, 칼로리가 적었으면 좋겠어, 요리는 못하는 편이야.")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
