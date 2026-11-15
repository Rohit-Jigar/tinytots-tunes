import pytest
from core.safety import SafetyChecker, CopyrightSafetyError

def test_original_character_passes():
    is_safe, violations = SafetyChecker.check_text("Barnaby Bear in teal dungarees sings a song")
    assert is_safe is True
    assert len(violations) == 0

def test_copyrighted_character_detected():
    is_safe, violations = SafetyChecker.check_text("Singing along with Peppa Pig and George Pig")
    assert is_safe is False
    assert "peppa pig" in violations or "peppa" in violations

def test_cocomelon_detected():
    is_safe, violations = SafetyChecker.check_text("Join JJ and Cocomelon for nursery rhymes")
    assert is_safe is False
    assert "cocomelon" in violations

def test_safety_enforcement_raises_exception():
    with pytest.raises(CopyrightSafetyError):
        SafetyChecker.enforce_safety("Baby Shark doo doo doo doo", context="Lyric test")

def test_sanitize_prompt():
    prompt = "A cute cartoon scene with Mickey Mouse in a park"
    sanitized = SafetyChecker.sanitize_prompt(prompt)
    assert "mickey mouse" not in sanitized.lower()

