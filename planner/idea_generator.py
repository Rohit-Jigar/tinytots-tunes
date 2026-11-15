import random
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from core.safety import SafetyChecker

class SongTheme(BaseModel):
    category: str
    topic: str
    target_age: str
    educational_goals: List[str]
    suggested_tempo: str  # e.g., "Upbeat 120 BPM", "Gentle 80 BPM"
    sample_prompts: List[str]

PRESCHOOL_CURRICULUM: List[Dict[str, Any]] = [
    {
        "category": "Colors & Creativity",
        "topic": "The Rainbow Paintbox Song",
        "target_age": "2-5 years",
        "educational_goals": ["Identify Red, Blue, Yellow, Green, Purple", "Color association with fruits/nature"],
        "suggested_tempo": "Upbeat 116 BPM",
        "hook": "Red like an apple, blue like the sky, let's paint a rainbow you and I!"
    },
    {
        "category": "Healthy Daily Habits",
        "topic": "Brush Your Teeth with Barnaby Bear",
        "target_age": "1-4 years",
        "educational_goals": ["Morning & night hygiene routine", "Up and down brushing motion", "Positive habit reinforcement"],
        "suggested_tempo": "Bouncy 122 BPM",
        "hook": "Up and down, round and round, sparkly teeth without a frown!"
    },
    {
        "category": "Numbers & Counting",
        "topic": "Five Little Penguins Waddling in the Snow",
        "target_age": "2-5 years",
        "educational_goals": ["Counting from 1 to 5", "Subtraction concept (one hops away)", "Rhythm and balance"],
        "suggested_tempo": "Playful 118 BPM",
        "hook": "One, two, three, four, five! Five happy penguins jump and dive!"
    },
    {
        "category": "Animals & Nature",
        "topic": "The Animal Sounds Safari Hop",
        "target_age": "1-4 years",
        "educational_goals": ["Animal vocalizations (Roar, Ribbit, Chirp)", "Gross motor imitation", "Curiosity about wildlife"],
        "suggested_tempo": "Energetic 125 BPM",
        "hook": "Lions go roar, frogs go hop, dance with the animals, don't you stop!"
    },
    {
        "category": "Bedtime & Lullaby",
        "topic": "Sleepy Starling Sweet Dreams Lullaby",
        "target_age": "0-4 years",
        "educational_goals": ["Calm bedtime transition", "Gentle breathing rhythm", "Emotional security"],
        "suggested_tempo": "Gentle 75 BPM",
        "hook": "Twinkle little moonbeam, soft and bright, close your sleepy eyes, goodnight."
    },
    {
        "category": "Social & Emotional Learning",
        "topic": "Sharing is Caring (Pass the Crayon)",
        "target_age": "2-5 years",
        "educational_goals": ["Taking turns", "Empathy and friendship", "Collaborative play"],
        "suggested_tempo": "Warm 112 BPM",
        "hook": "One for you and one for me, happy friends as kind as can be!"
    }
]

class IdeaGenerator:
    """Generates original preschool song ideas aligned with toddler developmental milestones."""

    @classmethod
    def generate_idea(cls, category: str = None, preferred_character: str = None) -> Dict[str, Any]:
        pool = PRESCHOOL_CURRICULUM
        if category:
            matched = [c for c in pool if c["category"].lower() == category.lower()]
            if matched:
                pool = matched

        selected = random.choice(pool).copy()

        # Check safety
        SafetyChecker.enforce_safety(selected["topic"], context="Song Idea Topic")

        return {
            "title": selected["topic"],
            "category": selected["category"],
            "target_age": selected["target_age"],
            "educational_goals": selected["educational_goals"],
            "tempo": selected["suggested_tempo"],
            "hook": selected["hook"],
            "preferred_character": preferred_character or "barnaby_bear"
        }

    @classmethod
    def list_curriculum_categories(cls) -> List[str]:
        return list({c["category"] for c in PRESCHOOL_CURRICULUM})

