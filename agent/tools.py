def mock_lead_capture(name, email, platform):
    print(f"Lead captured successfully: {name}, {email}, {platform}")
    return {
        "status": "success",
        "message": f"Thanks {name}! Your interest for {platform} has been recorded. Our team will contact you at {email} soon."
    }
