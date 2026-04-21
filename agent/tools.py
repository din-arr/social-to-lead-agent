def mock_lead_capture(name, email, platform):
    message = f"Lead captured successfully: {name}, {email}, {platform}"
    print(message)
    return {
        "status": "success",
        "message": message
    }