import re
from agent.intent import classify_intent
from agent.rag import retrieve_answer
from agent.tools import mock_lead_capture


def is_valid_email(email: str) -> bool:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


def detect_platform(text: str) -> str:
    text = text.lower()
    platforms = ["youtube", "instagram", "tiktok", "linkedin", "facebook"]
    for platform in platforms:
        if platform in text:
            return platform.capitalize()
    return ""


def process_message(state, user_message: str) -> str:
    user_message = user_message.strip()
    state["messages"].append({"role": "user", "content": user_message})

    if state.get("lead_captured", False):
        return "Your lead has already been captured successfully."

    if "lead_stage" not in state:
        state["lead_stage"] = ""

    intent = classify_intent(user_message)
    state["intent"] = intent

    if not state.get("platform"):
        detected_platform = detect_platform(user_message)
        if detected_platform:
            state["platform"] = detected_platform

    # Greeting only when not already in lead flow
    if intent == "greeting" and state.get("lead_stage") == "":
        return "Hi! I can help you with AutoStream pricing, features, refunds, and sign-up."

    # Enter lead flow
    if intent == "high_intent_lead" and state.get("lead_stage") == "":
        state["lead_stage"] = "awaiting_name"
        return "Great! You're interested in AutoStream. May I have your name?"

    # Lead flow step 1: name
    if state.get("lead_stage") == "awaiting_name":
        state["name"] = user_message
        state["lead_stage"] = "awaiting_email"
        return "Thanks! Please share your email address."

    # Lead flow step 2: email
    if state.get("lead_stage") == "awaiting_email":
        if not is_valid_email(user_message):
            return "Please share a valid email address."

        state["email"] = user_message

        if state.get("platform"):
            result = mock_lead_capture(
                state["name"],
                state["email"],
                state["platform"]
            )
            state["lead_captured"] = True
            state["lead_stage"] = "completed"
            return result["message"]

        state["lead_stage"] = "awaiting_platform"
        return "Thanks! Which creator platform do you use? (YouTube, Instagram, etc.)"

    # Lead flow step 3: platform
    if state.get("lead_stage") == "awaiting_platform":
        detected_platform = detect_platform(user_message)
        if detected_platform:
            state["platform"] = detected_platform
        else:
            state["platform"] = user_message

        result = mock_lead_capture(
            state["name"],
            state["email"],
            state["platform"]
        )
        state["lead_captured"] = True
        state["lead_stage"] = "completed"
        return result["message"]

    # Normal product query
    if intent == "product_inquiry":
        return retrieve_answer(user_message)

    return "Sorry, I didn’t fully understand that. You can ask about pricing, features, refunds, or say you want to get started."