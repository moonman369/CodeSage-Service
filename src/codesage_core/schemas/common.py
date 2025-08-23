"""Common Pydantic schema utilities shared across the CodeSage Core server."""
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field

__all__ = ["Timestamped"]


class Timestamped(BaseModel):
    """Mixin providing a created timestamp."""

    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp (UTC).")
