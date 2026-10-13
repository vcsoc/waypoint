from typing import Final, Literal, TypeAlias
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator

Locale: TypeAlias = Literal["en-US", "en-GB", "fr", "el", "af", "he", "de", "nl", "pt", "es", "it"]


def validate_timezone(value: str) -> str:
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError("Expected a valid IANA timezone") from None
    return value


class UserPreferences(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    locale: Locale = "en-US"
    timezone: str = Field(default="UTC", min_length=1, max_length=128)

    @field_validator("timezone")
    @classmethod
    def valid_timezone(cls, value: str) -> str:
        return validate_timezone(value)


class UserPreferencesUpdate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    locale: Locale | None = None
    timezone: str | None = Field(default=None, min_length=1, max_length=128)

    @field_validator("timezone")
    @classmethod
    def valid_timezone(cls, value: str | None) -> str | None:
        return None if value is None else validate_timezone(value)


DEFAULT_PREFERENCES: Final = UserPreferences()
