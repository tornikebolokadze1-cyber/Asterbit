#!/usr/bin/env python3
"""Read a transcript's token usage the way the advisor tool documents it (engine assessment A4).

On a turn with an advisor call, one API response holds several sampling rounds:
usage.iterations lists them (type "message" = the main model, "advisor_message" =
the advisor), and every top-level field is the SUM over the main model's rounds.
So the top-level input + cache figure is about twice the real context (seen live
2026-10-07: 1,175,330 reported, 588,432 real). The main model's context is the
last "message" round. Advisor tokens never count toward the main context.
"""

from __future__ import annotations

CONTEXT_FIELDS = (
    "input_tokens",
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
)


def context_size(usage: dict) -> int:
    """Tokens in the main model's prompt for this response."""
    iterations = usage.get("iterations")
    if isinstance(iterations, list):
        rounds = [
            item
            for item in iterations
            if isinstance(item, dict) and item.get("type") == "message"
        ]
        if rounds:
            usage = rounds[-1]
    return sum(int(usage.get(field) or 0) for field in CONTEXT_FIELDS)
