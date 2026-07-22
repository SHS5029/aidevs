r"""learning_notes 생성 예제입니다.

실행:
    cd C:\aidev\02_supabase-ai-backend
    .\.venv\Scripts\Activate.ps1
    python .\03_supabase-db-and-auth\02_supabase-table-and-crud\01_create_learning_note.py
"""

from datetime import datetime, timedelta, timezone

from supabase_client import get_supabase


KST = timezone(timedelta(hours=9))


def create_time_id(created_at: datetime | None = None) -> str:
    """KST 생성 시각을 YYYYMMDDHHMMSSff 형식의 ID로 만듭니다."""

    created_at_kst = (created_at or datetime.now(KST)).astimezone(KST)
    centiseconds = created_at_kst.microsecond // 10_000
    return f"{created_at_kst:%Y%m%d%H%M%S}{centiseconds:02d}"


def format_created_at_as_kst(created_at: str) -> str:
    """타임존이 포함된 생성 시각을 KST 날짜와 시간으로 변환합니다."""

    return datetime.fromisoformat(created_at).astimezone(KST).strftime("%Y-%m-%d %H:%M:%S KST")


def main() -> None:
    """learning_notes 테이블에 메모 1개를 생성합니다."""

    supabase = get_supabase()

    # insert는 SQL의 INSERT INTO와 비슷합니다.
    # 딕셔너리의 key는 테이블 컬럼명과 같아야 합니다.
    result = (
        supabase.table("learning_notes")
        .insert(
            {
                "id": create_time_id(),
                "title": "제목",
                "content": "내용",
            }
        )
        .execute()
    )

    if not result.data:
        raise RuntimeError("insert 결과가 비어 있습니다. learning_notes 테이블과 권한을 확인하세요.")

    created = result.data[0]
    print("[created note]")
    print(f"id: {created.get('id')}")
    print(f"title: {created.get('title')}")
    print(f"content: {created.get('content')}")
    print(f"created_at: {format_created_at_as_kst(created['created_at'])}")


if __name__ == "__main__":
    main()
