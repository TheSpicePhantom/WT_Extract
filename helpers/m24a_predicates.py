"""Referenz-Predicates für M24a — delegiert an game_core.worker_fast_path."""

from game_core.worker_fast_path import (
    can_apply_worker_complete_fast_path,
    has_user_decorations_in_chunk,
    is_worker_complete_result,
)

__all__ = [
    "can_apply_worker_complete_fast_path",
    "has_user_decorations_in_chunk",
    "is_worker_complete_result",
]
