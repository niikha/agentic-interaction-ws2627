from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        }

    @abstractmethod
    def run(self, arguments_json: str) -> str:
        raise NotImplementedError
