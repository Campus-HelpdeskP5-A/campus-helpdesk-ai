import sys
from pathlib import Path

import joblib

sys.path.append(str(Path(__file__).resolve().parent.parent))


MODEL_DIR = Path(__file__).resolve().parent.parent / "models" / "category"


# Gomal gdeeda tamaman, mesh mawgoda fel training data, betghati kol
# el keywords el metnaza3 3aleeha (water, power, AC, network, PC, door, floor).
# Kol group beghati sina3ryo mo5talef 3ashan nesh2af kol el model 3andaho
# context understanding 7a2i2i wala bas lexical shortcuts.

BOUNDARY_TESTS = [
    # --- "water" trap: HVAC_AC vs PLUMBING_WATER ---
    ("Water dripping from the AC unit onto the desk", "HVAC_AC"),
    ("AC condensation is leaking near the window", "HVAC_AC"),
    ("Sink is overflowing and flooding the floor", "PLUMBING_WATER"),
    ("Pipe burst under the kitchen counter", "PLUMBING_WATER"),
    ("Water stain on the ceiling below the AC vent", "HVAC_AC"),

    # --- "power" trap: AV_CLASSROOM_EQUIPMENT vs ELECTRICAL ---
    ("Speaker system has no power in the auditorium", "AV_CLASSROOM_EQUIPMENT"),
    ("Smart board won't turn on during lecture", "AV_CLASSROOM_EQUIPMENT"),
    ("Wall outlet has no power at all", "ELECTRICAL"),
    ("Circuit breaker keeps tripping in the hallway", "ELECTRICAL"),
    ("Microphone stopped working mid presentation, no power light", "AV_CLASSROOM_EQUIPMENT"),

    # --- "AC" trap: HVAC_AC vs IT_HARDWARE_PRINTING ---
    ("My laptop's AC charger stopped working", "IT_HARDWARE_PRINTING"),
    ("Need a replacement AC power cord for my computer", "IT_HARDWARE_PRINTING"),
    ("The office AC is blowing warm air instead of cold", "HVAC_AC"),
    ("Classroom AC unit is making a loud rattling noise", "HVAC_AC"),
    ("Charger adapter for desktop PC is missing", "IT_HARDWARE_PRINTING"),

    # --- "network" / "PC" trap: IT_NETWORK_ACCOUNTS vs IT_HARDWARE_PRINTING ---
    ("This computer can't connect to the campus Wi-Fi", "IT_NETWORK_ACCOUNTS"),
    ("Lab desktop screen is completely black, won't boot", "IT_HARDWARE_PRINTING"),
    ("Can't log into my student portal account", "IT_NETWORK_ACCOUNTS"),
    ("Keyboard on the library PC is unresponsive", "IT_HARDWARE_PRINTING"),
    ("Internet connection keeps dropping in the lab", "IT_NETWORK_ACCOUNTS"),

    # --- "door" trap: BUILDING_STRUCTURE vs IT_NETWORK_ACCOUNTS vs FURNITURE_FIXTURES ---
    ("The server room door lock is broken", "BUILDING_STRUCTURE"),
    ("Classroom door won't close properly", "BUILDING_STRUCTURE"),
    ("Cabinet door hinge is loose in the office", "FURNITURE_FIXTURES"),
    ("Network switch cabinet has a broken latch", "BUILDING_STRUCTURE"),

    # --- "floor" trap: CLEANING_WASTE vs BUILDING_STRUCTURE vs HVAC_AC ---
    ("Floor is sticky and needs mopping in the cafeteria", "CLEANING_WASTE"),
    ("Floor tile cracked near the entrance", "BUILDING_STRUCTURE"),
    ("Water pooling on the floor under the AC vent", "HVAC_AC"),
    ("Trash scattered across the hallway floor", "CLEANING_WASTE"),

    # --- Extra ambiguous / real-world style short tickets ---
    ("Elevator stuck between floors", "ELEVATOR"),
    ("Grass overgrown near the parking lot", "GROUNDS_OUTDOOR"),
    ("Smoke smell coming from the electrical panel", "SAFETY_HAZARD"),
]


def main():
    model_path = MODEL_DIR / "category_model.joblib"
    vectorizer_path = MODEL_DIR / "category_vectorizer.joblib"

    if not model_path.exists() or not vectorizer_path.exists():
        print("Model not found. Run train_category_model.py first.")
        return

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    correct = 0
    total = len(BOUNDARY_TESTS)

    print(f"--- Boundary / Trap Test ({total} unseen sentences) ---\n")

    for text, expected in BOUNDARY_TESTS:
        vector = vectorizer.transform([text])
        prediction = model.predict(vector)[0]
        confidence = max(model.predict_proba(vector)[0])

        status = "OK" if prediction == expected else "WRONG"
        if prediction == expected:
            correct += 1

        print(f"[{status}] '{text}'")
        print(f"       -> predicted={prediction} (expected={expected}, confidence={confidence:.2f})\n")

    accuracy = correct / total
    print(f"Boundary/Trap test accuracy: {correct}/{total} ({accuracy:.2%})")


if __name__ == "__main__":
    main()