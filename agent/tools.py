def mock_lead_capture(name, email, platform):
    return {
        "status": "success",
        "message": f"Thanks {name}! Your interest for {platform} has been recorded. Our team will contact you at {email} soon."
    }