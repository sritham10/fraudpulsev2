from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from fraudpulse.schema import TransactionEvent


def valid_event_data() -> dict[str, object]:
    return {
        "transaction_id": "123e4567-e89b-12d3-a456-426614174000",
        "account_id": "acct_123",
        "event_time": datetime(2026, 11, 24, 12, 0, tzinfo=UTC),
        "amount_minor": 125_00,
        "currency": "INR",
        "merchant_descriptor": "Example Store",
        "country": "IN",
        "lat": 19.076,
        "lon": 72.8777,
        "device_id": "device_123",
    }


def test_valid_event_is_accepted():
    event = TransactionEvent(**valid_event_data())

    assert event.amount_minor == 125_00
    assert event.currency == "INR"


def test_zero_or_negative_amount_is_rejected():
    for amount_minor in (0, -1):
        data = valid_event_data()
        data["amount_minor"] = amount_minor

        with pytest.raises(ValidationError):
            TransactionEvent(**data)


def test_naive_datetime_is_rejected():
    data = valid_event_data()
    data["event_time"] = datetime(2026, 11, 24, 12, 0)

    with pytest.raises(ValidationError):
        TransactionEvent(**data)


def test_unknown_field_is_rejected():
    data = valid_event_data()
    data["unexpected"] = "value"

    with pytest.raises(ValidationError):
        TransactionEvent(**data)


def test_json_round_trip_returns_equal_event():
    event = TransactionEvent(**valid_event_data())

    restored = TransactionEvent.model_validate_json(event.model_dump_json())

    assert restored == event
