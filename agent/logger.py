import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4


class Event(str, Enum):
    USER_TASK = "user_task"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    FINAL = "final"
    ERROR = "error"


class logger:
    def __init__(self) -> None:
        self.run_id = str(uuid4())
        log_directory = Path(__file__).resolve().parent.parent / "log"
        log_directory.mkdir(parents=True, exist_ok=True)
        log_date = datetime.now(timezone.utc).date().isoformat()
        self.log_file = log_directory / f"{log_date}.jsonl"
        self.log_file.touch()

    def log_event(
        self,
        event: Event,
        tool: Optional[str] = None,
        args: Optional[Any] = None,
        ok: bool = True,
        model: Optional[str] = None,
        duration_ms: Optional[float] = None,
    ) -> None:

        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "run_id": self.run_id,
            "event": event.value,
            "tool": tool,
            "args": args,
            "ok": ok,
            "model": model,
            "duration_ms": duration_ms,
        }
        with self.log_file.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(entry) + "\n")
