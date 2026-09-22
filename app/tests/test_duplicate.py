from app.duplicate import DuplicateDetector, suggest_duplicates


def test_empty_pool_returns_no_candidates():
    detector = DuplicateDetector()
    detector.fit([])

    result = detector.find_duplicates("AC not working", "room 101")

    assert result == []


def test_finds_exact_duplicate():
    existing_tickets = [
        {"id": "t1", "text": "AC not working in room 101"},
        {"id": "t2", "text": "Wifi is down in the library"},
    ]

    detector = DuplicateDetector()
    detector.fit(existing_tickets)

    result = detector.find_duplicates("AC not working in room 101", "", top_k=1)

    assert len(result) == 1
    assert result[0]["ticket_id"] == "t1"
    assert result[0]["similarity_score"] > 0.5


def test_suggest_duplicates_handles_crash_safely():
    # existing_tickets malformed 3ashan nejarrab el fallback
    result = suggest_duplicates("AC issue", "room 101", existing_tickets=None)

    assert result == []