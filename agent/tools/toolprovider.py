from time import perf_counter
from typing import Any, Dict, List, Optional

from ..logger import Event, logger
from .calendar import calendar
from .tool import tool
from .weather import weather


class toolprovider:
    def __init__(self, run_logger: logger, model: Optional[str]) -> None:
        self.run_logger = run_logger
        self.run_logger.model = model
        self.tools: List[tool] = [calendar(), weather()]

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": registered_tool.name,
                    "description": registered_tool.description,
                    "parameters": registered_tool.parameters,
                },
            }
            for registered_tool in self.tools
        ]

    def run_tool(self, name: str, arguments_json: str) -> str:
        self.run_logger.log_event(
            Event.TOOL_CALL,
            tool=name,
            args=arguments_json,
        )
        started_at = perf_counter()
        result_args = None
        succeeded = False

        try:
            registered_tool = next(
                (item for item in self.tools if item.name == name),
                None,
            )
            if registered_tool is None:
                raise ValueError(f"Unsupported tool: {name}")

            result = registered_tool.run(arguments_json)
            result_args = {"result": result}
            succeeded = True
            return result

        except Exception as error:
            result_args = {
                "exception_type": type(error).__name__,
                "exception": str(error),
            }
            return f"An error occurred while running tool '{name}': {error}"

        finally:
            self.run_logger.log_event(
                Event.TOOL_RESULT,
                tool=name,
                args=result_args,
                ok=succeeded,
                duration_ms=(perf_counter() - started_at) * 1000,
            )
