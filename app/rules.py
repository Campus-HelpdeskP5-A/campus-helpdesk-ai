CATEGORY_RULES = {
    "IT": [
        "wifi",
        "internet",
        "network",
        "router",
        "connection",
    ],

    "Maintenance": [
        "ac",
        "air conditioner",
        "electricity",
        "light",
        "water",
        "leak",
        "plumbing",
        "maintenance",
        "broken",
    ],

    "Cleaning": [
        "clean",
        "dirty",
        "trash",
        "garbage",
    ],
}


IMPACT_RULES = {
    "High": [
        "building",
        "entire building",
        "main system",
        "critical system",
        "server",
        "campus-wide",
    ],

    "Medium": [
        "group",
        "class",
        "classroom",
        "room",
        "laboratory",
        "lab",
    ],

    "Low": [
        "my room",
        "my device",
        "my computer",
        "personal",
        "one person",
    ],
}


URGENCY_RULES = {
    "High": [
        "emergency",
        "urgent",
        "fire",
        "danger",
        "flood",
        "no electricity",
        "cannot work",
        "can't work",
        "cannot access",
        "blocked",
        "stopped working",
    ],

    "Medium": [
        "affecting work",
        "affecting class",
        "not working",
        "broken",
        "problem",
        "issue",
    ],

    "Low": [
        "minor",
        "not urgent",
        "can wait",
        "when possible",
    ],
}


PRIORITY_MATRIX = {
    "High": {
        "Low": "Medium",
        "Medium": "High",
        "High": "Critical",
    },

    "Medium": {
        "Low": "Low",
        "Medium": "Medium",
        "High": "High",
    },

    "Low": {
        "Low": "Low",
        "Medium": "Low",
        "High": "Medium",
    },
}