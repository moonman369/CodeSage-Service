"""Tools for analyzing historical code evolution.

Future implementations may integrate with VCS logs, issue trackers, and commit
metadata to surface trends or ownership insights.
"""
from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

__all__ = [
    "RecentChange",
    "ChangeHistoryResponse",
]


class RecentChange(BaseModel):
    """Represents a recent change artifact."""

    path: str = Field(..., description="File path changed.")
    author: str = Field(..., description="Author of the change.")
    timestamp: datetime = Field(..., description="UTC timestamp of the change.")
    message: str = Field(..., description="Commit or change message.")


class ChangeHistoryResponse(BaseModel):
    """Response containing placeholder recent changes."""

    changes: List[RecentChange] = Field(default_factory=list, description="List of recent changes.")


def get_recent_changes(limit: int = 5) -> ChangeHistoryResponse:
    """Return placeholder recent changes.

    Parameters
    ----------
    limit: int
        Max number of changes to include.
    """
    now = datetime.utcnow()
    changes = [
        RecentChange(
            path=f"src/module_{i}.py", author="placeholder", timestamp=now, message="Initial placeholder commit"
        )
        for i in range(limit)
    ]
    return ChangeHistoryResponse(changes=changes)
