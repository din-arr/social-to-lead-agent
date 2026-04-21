def classify_intent(user_message: str) -> str:
    text = user_message.lower().strip()

    high_intent_keywords = [
        "sign up",
        "get started",
        "i want to try",
        "i want pro",
        "subscribe",
        "buy",
        "interested",
        "want to use",
        "want to join",
        "start pro",
        "try pro",
        "i want the pro plan",
        "start"
    ]

    inquiry_keywords = [
        "price",
        "pricing",
        "plan",
        "plans",
        "feature",
        "features",
        "refund",
        "support",
        "cost",
        "resolution",
        "videos"
    ]

    greeting_keywords = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening",
        "good afternoon"
    ]

    for phrase in high_intent_keywords:
        if phrase in text:
            return "high_intent_lead"

    for phrase in inquiry_keywords:
        if phrase in text:
            return "product_inquiry"

    for phrase in greeting_keywords:
        if phrase in text:
            return "greeting"

    return "product_inquiry"