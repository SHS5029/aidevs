import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import types


MODULE_PATH = Path(__file__).with_name("01_create_learning_note.py")
supabase_client = types.ModuleType("supabase_client")
supabase_client.get_supabase = lambda: None
sys.modules.setdefault("supabase_client", supabase_client)
SPEC = importlib.util.spec_from_file_location("create_learning_note", MODULE_PATH)
create_learning_note = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(create_learning_note)


def test_format_created_at_as_kst_crosses_utc_date_boundary() -> None:
    assert create_learning_note.format_created_at_as_kst(
        "2026-07-20T15:30:45+00:00"
    ) == "2026-07-21 00:30:45 KST"


def test_create_time_id_uses_kst_timestamp_and_centiseconds() -> None:
    utc = timezone.utc
    created_at = datetime(2026, 7, 21, 3, 28, 1, 10_000, tzinfo=utc)

    assert create_learning_note.create_time_id(created_at) == "2026072112280101"
