import pytest
from characters.models import Character
from characters.manager import character_manager
from core.safety import CopyrightSafetyError

def test_preset_characters_loaded():
    chars = character_manager.list_characters()
    assert len(chars) >= 5
    names = [c.name for c in chars]
    assert "Barnaby Bear" in names
    assert "Pip the Bird" in names
    assert "Penny Bunny" in names
    assert "Zara Zebra" in names
    assert "Sunny" in names

def test_get_character_by_id():
    char = character_manager.get_character("barnaby_bear")
    assert char is not None
    assert "Teddy Bear" in char.species
    assert len(char.color_palette) > 0

def test_character_copyright_safety_violation():
    with pytest.raises(CopyrightSafetyError):
        invalid_char = Character(
            id="fake_cocomelon",
            name="JJ Cocomelon",
            species="Boy",
            clothing="Blue pajamas",
            distinctive_features="Melon curl",
            personality="Cheerful",
            visual_prompt="JJ from Cocomelon"
        )
        character_manager.save_character(invalid_char)

