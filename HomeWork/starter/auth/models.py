from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Account:
    id: int
    email: str


@dataclass(slots=True)
class AuditEvent:
    account_id: int
    event_type: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: datetime | None = None


@dataclass(slots=True)
class AccountCard:
    account: Account
    has_active_code: bool
    events: list[AuditEvent]
