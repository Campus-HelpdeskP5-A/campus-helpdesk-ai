def suggest_category(title: str, description: str):
    text = f"{title} {description}".lower()

    if any(word in text for word in [
        "wifi", "internet", "network", "router", "connection"
    ]):
        return "IT", 0.9, "Ticket contains network-related keywords."

    if any(word in text for word in [
        "ac", "air conditioner", "electricity", "light", "water",
        "leak", "plumbing", "maintenance", "broken"
    ]):
        return "Maintenance", 0.9, "Ticket contains maintenance-related keywords."

    if any(word in text for word in [
        "clean", "dirty", "trash", "garbage"
    ]):
        return "Cleaning", 0.9, "Ticket contains cleaning-related keywords."

    return "Other", 0.5, "No specific category keyword was detected."


def suggest_priority(title: str, description: str):
    text = f"{title} {description}".lower()

    if any(word in text for word in [
        "emergency", "urgent", "fire", "danger", "flood",
        "no electricity", "security"
    ]):
        return "High", 0.9, "Ticket contains urgent or safety-related keywords."

    if any(word in text for word in [
        "not working", "broken", "problem", "issue"
    ]):
        return "Medium", 0.75, "Ticket describes a service or equipment issue."

    return "Low", 0.6, "No urgent or critical keyword was detected."