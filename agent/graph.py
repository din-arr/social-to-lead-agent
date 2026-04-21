"""Advanced lead-flow message processor for AutoStream assistant.

This module keeps a backward-compatible ``process_message`` function while
improving validation, state handling, and conversational resilience.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, Mapping

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z\s'\-]{1,79}$")

PLATFORM_ALIASES: Mapping[str, str] = {
    "youtube": "YouTube",
    "yt": "YouTube",
    "instagram": "Instagram",
    "insta": "Instagram",
    "ig": "Instagram",
    "tiktok": "TikTok",
    "tik tok": "TikTok",
    "linkedin": "LinkedIn",
    "facebook": "Facebook",
    "fb": "Facebook",
}

SUPPORTED_PLATFORMS = ("YouTube", "Instagram", "TikTok", "LinkedIn", "Facebook")


@dataclass(frozen=True)
class LeadStages:
    NONE: str = ""
    AWAITING_NAME: str = "awaiting_name"
    AWAITING_EMAIL: str = "awaiting_email"
    AWAITING_PLATFORM: str = "awaiting_platform"
    COMPLETED: str = "completed"


STAGES = LeadStages()


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email.strip()))


def is_valid_name(name: str) -> bool:
    return bool(NAME_RE.match(name.strip()))


def detect_platform(text: str) -> str:
    lowered = text.lower().strip()

    # Try exact matches first for speed and precision.
    if lowered in PLATFORM_ALIASES:
        return PLATFORM_ALIASES[lowered]

    for alias, normalized in PLATFORM_ALIASES.items():
        if alias in lowered:
            return normalized

    return ""


def _default_intent_classifier(_: str) -> str:
    return "unknown"


def _default_retriever(_: str) -> str:
    return (
        "I can help with pricing, features, refunds, or onboarding. "
        "Could you share what you want to know?"
    )


def _default_lead_capture(name: str, email: str, platform: str) -> Dict[str, str]:
    return {
        "message": (
            f"Thanks {name}! We captured your details ({email}) for {platform}. "
            "Our team will reach out shortly."
        )
    }


def _normalize_state(state: Dict[str, Any]) -> Dict[str, Any]:
    state.setdefault("messages", [])
    state.setdefault("lead_captured", False)
    state.setdefault("lead_stage", STAGES.NONE)
    state.setdefault("intent", "unknown")
    state.setdefault("platform", "")
    return state


def process_message(
    state: Dict[str, Any],
    user_message: str,
    *,
    classify_intent_fn: Callable[[str], str] | None = None,
    retrieve_answer_fn: Callable[[str], str] | None = None,
    lead_capture_fn: Callable[[str, str, str], Dict[str, str]] | None = None,
) -> str:
    """Process a single user message while updating the mutable conversation state."""
    classify_intent_fn = classify_intent_fn or _default_intent_classifier
    retrieve_answer_fn = retrieve_answer_fn or _default_retriever
    lead_capture_fn = lead_capture_fn or _default_lead_capture

    state = _normalize_state(state)

    message = user_message.strip()
    if not message:
        return "Please send a message so I can help you."

    state["messages"].append({"role": "user", "content": message})

    if state["lead_captured"]:
        return "Your lead has already been captured successfully."

    intent = classify_intent_fn(message)
    state["intent"] = intent

    detected_platform = detect_platform(message)
    if detected_platform and not state.get("platform"):
        state["platform"] = detected_platform

    stage = state.get("lead_stage", STAGES.NONE)

    if intent == "product_inquiry" and stage == STAGES.NONE:
        return retrieve_answer_fn(message)

    if intent == "greeting" and stage == STAGES.NONE:
        return (
            "Hi! I can help with AutoStream pricing, features, refunds, "
            "and sign-up."
        )

    if intent == "high_intent_lead" and stage == STAGES.NONE:
        state["lead_stage"] = STAGES.AWAITING_NAME
        return "Great! You're interested in AutoStream. May I have your full name?"

    if stage == STAGES.AWAITING_NAME:
        if not is_valid_name(message):
            return "Please share your real name (letters, spaces, apostrophes, or hyphens)."

        state["name"] = message
        state["lead_stage"] = STAGES.AWAITING_EMAIL
        return "Thanks! Please share your best email address."

    if stage == STAGES.AWAITING_EMAIL:
        if not is_valid_email(message):
            return "Please share a valid email address (example: name@domain.com)."

        state["email"] = message.lower()

        if state.get("platform"):
            result = lead_capture_fn(state["name"], state["email"], state["platform"])
            state["lead_captured"] = True
            state["lead_stage"] = STAGES.COMPLETED
            return result["message"]

        state["lead_stage"] = STAGES.AWAITING_PLATFORM
        return (
            "Thanks! Which creator platform do you use most? "
            f"({', '.join(SUPPORTED_PLATFORMS)})"
        )

    if stage == STAGES.AWAITING_PLATFORM:
        state["platform"] = detected_platform or message.title()

        result = lead_capture_fn(state["name"], state["email"], state["platform"])
        state["lead_captured"] = True
        state["lead_stage"] = STAGES.COMPLETED
        return result["message"]

    # Handle mixed intent during lead capture by answering then guiding back.
    if intent == "product_inquiry" and stage != STAGES.NONE:
        answer = retrieve_answer_fn(message)
        prompts = {
            STAGES.AWAITING_NAME: "When you're ready, please share your full name.",
            STAGES.AWAITING_EMAIL: "When you're ready, please share your email address.",
            STAGES.AWAITING_PLATFORM: "When you're ready, tell me your creator platform.",
        }
        return f"{answer}\n\n{prompts.get(stage, '')}".strip()

    return (
        "Sorry, I didn’t fully understand that. You can ask about pricing, features, "
        "refunds, or say you want to get started."
    )