CATEGORY_RULES = {
    "HVAC_AC": [
        "ac", "air conditioner", "air conditioning", "thermostat",
        "vent", "ventilation", "airflow", "cooling",
    ],

    "ELECTRICAL": [
        "electricity", "electrical", "power outlet", "wall socket",
        "socket", "power supply", "wiring", "shock",
    ],

    "SAFETY_HAZARD": [
        "safety", "hazard", "danger", "obstruction", "smoke",
        "fire", "unsafe", "safety sign", "broken railing", "railing",
    ],

    "PLUMBING_WATER": [
        "water", "leak", "leaking", "pipe", "faucet", "drain",
        "plumbing", "sink",
    ],

    "ELEVATOR": [
        "elevator", "lift", "الأسانسير", "اسانسير",
    ],

    "IT_HARDWARE_PRINTING": [
        "laptop", "computer", "printer", "printing", "mouse",
        "keyboard", "monitor", "desktop", "adapter",
    ],

    "IT_NETWORK_ACCOUNTS": [
        "wifi", "wi-fi", "internet", "network", "router", "connection",
        "account", "email", "password", "login",
    ],

    "AV_CLASSROOM_EQUIPMENT": [
        "projector", "microphone", "speaker", "screen",
        "classroom equipment", "lecture screen",
    ],

    "CLEANING_WASTE": [
        "clean", "dirty", "trash", "garbage", "waste", "bin",
        "bathroom", "waste bin", "overflowing",
    ],

    "GROUNDS_OUTDOOR": [
        "gate", "walkway", "outdoor", "garden", "courtyard",
        "parking",
    ],

    "FURNITURE_FIXTURES": [
        "shelf", "chair", "desk", "table", "bench", "furniture",
        "door handle", "cabinet",
    ],

    "BUILDING_STRUCTURE": [
        "wall", "ceiling", "floor tile", "crack", "structure",
        "window", "building",
    ],

    "OTHER": [],
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