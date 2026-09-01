from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ErrorInfo:
    code: str
    message: str
    location: str | None = None


class ThesisBenchError(Exception):
    exit_code = 1

    def __init__(self, code: str, message: str, *, location: str | None = None) -> None:
        self.info = ErrorInfo(code=code, message=message, location=location)
        super().__init__(message)

    @property
    def code(self) -> str:
        return self.info.code

    def as_json_object(self) -> dict[str, Any]:
        error: dict[str, Any] = {"code": self.info.code, "message": self.info.message}
        if self.info.location is not None:
            error["location"] = self.info.location
        return {"error": error}

    def __str__(self) -> str:
        if self.info.location is None:
            return self.info.message
        return f"{self.info.message} ({self.info.location})"


class ConfigurationError(ThesisBenchError):
    exit_code = 2


class PreparationError(ThesisBenchError):
    exit_code = 3


class CollisionError(ThesisBenchError):
    exit_code = 4


class IntegrityError(ThesisBenchError):
    exit_code = 4
