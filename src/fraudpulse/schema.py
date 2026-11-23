"""Validated, immutable schema for incoming transaction events."""

from datetime import datetime, timedelta
from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator


class TransactionEvent(BaseModel):
    """A single fraud-detection transaction event."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: int = 1
    transaction_id: UUID
    account_id: str
    event_time: AwareDatetime
    amount_minor: int = Field(gt=0)
    currency: Literal["INR"]
    merchant_descriptor: str
    country: str = Field(pattern=r"^[A-Z]{2}$")
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    device_id: str

    @field_validator("event_time")
    @classmethod
    def event_time_must_be_utc(cls, value: datetime) -> datetime:
        """Reject offset-aware datetimes that are not UTC."""
        if value.utcoffset() != timedelta(0):
            raise ValueError("event_time must use UTC")
        return value
