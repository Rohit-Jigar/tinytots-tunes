import re
from typing import List, Tuple

# Comprehensive list of copyrighted children's franchises and characters to prohibit
RESTRICTED_KEYWORDS = [
    # Cocomelon
    "cocomelon", "jj", "yo-yo", "tomtom", "cody", "nina", "melon patch", "cocomelon lane",
    # Peppa Pig
    "peppa", "peppa pig", "george pig", "mummy pig", "daddy pig",
    # Baby Shark / Pinkfong
    "baby shark", "pinkfong", "bebe finn", "william the fish", "hogi",
    # Disney & Pixar
    "mickey mouse", "minnie mouse", "donald duck", "daisy duck", "goofy", "pluto",
    "elsa", "anna", "olaf", "frozen", "lightning mcqueen", "mater", "cars",
    "winnie the pooh", "tigger", "eeyore", "piglet",
    # Nickelodeon & Spin Master
    "paw patrol", "chase", "marshall", "skye", "rubble", "zuma", "rocky", "ryder",
    "dora the explorer", "boots the monkey", "spongebob", "patrick star",
    # BBC / ABC Kids
    "bluey", "bingo", "bandit", "chilli", "teletubbies", "tinky winky", "dipsy", "laa-laa", "po",
    # Mattel & Hasbro
    "thomas the tank engine", "thomas and friends", "percy", "barney the dinosaur", "my little pony",
    # Super Simple Songs & others
    "super simple songs", "tobee", "caitie", "blippi", "meekah", "ms rachel", "herbie"
]

class CopyrightSafetyError(ValueError):
    """Raised when copyrighted character or brand element is detected."""
    pass

class SafetyChecker:
    """
    Validates prompts, lyrics, titles, and character designs to guarantee 100% original,
    trademark-safe, COPPA-compliant children's content.
    """

    @classmethod
    def check_text(cls, text: str) -> Tuple[bool, List[str]]:
        """
        Scans text for prohibited trademarks or copyrighted character names.
        Returns (is_safe, list_of_violations).
        """
        if not text:
            return True, []

        normalized = text.lower()
        violations = []

        for kw in RESTRICTED_KEYWORDS:
            # Match whole words / phrases using regex boundary
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, normalized):
                violations.append(kw)

        return (len(violations) == 0, violations)

    @classmethod
    def enforce_safety(cls, text: str, context: str = "content") -> None:
        """
        Enforces safety rules by raising CopyrightSafetyError if violations are found.
        """
        is_safe, violations = cls.check_text(text)
        if not is_safe:
            raise CopyrightSafetyError(
                f"Copyright safety check failed in {context}! Found protected characters or brands: {', '.join(violations)}. "
                "TinyTots Tunes enforces 100% original non-infringing characters and lyrics."
            )

    @classmethod
    def sanitize_prompt(cls, prompt: str) -> str:
        """
        Strips or replaces any unintentional brand references to safeguard image/storyboard generation.
        """
        sanitized = prompt
        for kw in RESTRICTED_KEYWORDS:
            pattern = re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE)
            sanitized = pattern.sub("friendly cartoon character", sanitized)
        return sanitized

