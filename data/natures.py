"""
All 25 Pokemon natures and their stat modifiers.

boosted_stat and lowered_stat are set to "neutral" for natures that don't
change any stats. Valid stat values: attack, defense, special_attack,
special_defense, speed.

This is the only file that needs to change if nature data ever needs updating.
"""

NATURES: dict[str, dict[str, str]] = {
    # Neutral
    "hardy":   {"boosted_stat": "neutral", "lowered_stat": "neutral"},
    "docile":  {"boosted_stat": "neutral", "lowered_stat": "neutral"},
    "serious": {"boosted_stat": "neutral", "lowered_stat": "neutral"},
    "bashful": {"boosted_stat": "neutral", "lowered_stat": "neutral"},
    "quirky":  {"boosted_stat": "neutral", "lowered_stat": "neutral"},

    # Attack+
    "lonely":  {"boosted_stat": "attack", "lowered_stat": "defense"},
    "brave":   {"boosted_stat": "attack", "lowered_stat": "speed"},
    "adamant": {"boosted_stat": "attack", "lowered_stat": "special_attack"},
    "naughty": {"boosted_stat": "attack", "lowered_stat": "special_defense"},

    # Defense+
    "bold":    {"boosted_stat": "defense", "lowered_stat": "attack"},
    "relaxed": {"boosted_stat": "defense", "lowered_stat": "speed"},
    "impish":  {"boosted_stat": "defense", "lowered_stat": "special_attack"},
    "lax":     {"boosted_stat": "defense", "lowered_stat": "special_defense"},

    # Speed+
    "timid":   {"boosted_stat": "speed", "lowered_stat": "attack"},
    "hasty":   {"boosted_stat": "speed", "lowered_stat": "defense"},
    "jolly":   {"boosted_stat": "speed", "lowered_stat": "special_attack"},
    "naive":   {"boosted_stat": "speed", "lowered_stat": "special_defense"},

    # Sp. Attack+
    "modest":  {"boosted_stat": "special_attack", "lowered_stat": "attack"},
    "mild":    {"boosted_stat": "special_attack", "lowered_stat": "defense"},
    "quiet":   {"boosted_stat": "special_attack", "lowered_stat": "speed"},
    "rash":    {"boosted_stat": "special_attack", "lowered_stat": "special_defense"},

    # Sp. Defense+
    "calm":    {"boosted_stat": "special_defense", "lowered_stat": "attack"},
    "gentle":  {"boosted_stat": "special_defense", "lowered_stat": "defense"},
    "sassy":   {"boosted_stat": "special_defense", "lowered_stat": "speed"},
    "careful": {"boosted_stat": "special_defense", "lowered_stat": "special_attack"},
}

MODIFIABLE_STATS: list[str] = [
    "attack", "defense", "special_attack", "special_defense", "speed"
]


def build_modifiers(entry: dict[str, str]) -> dict[str, float]:
    """Returns a multiplier for each stat based on the given nature entry."""
    modifiers: dict[str, float] = {"hp": 1.0}
    for stat in MODIFIABLE_STATS:
        if entry["boosted_stat"] == stat:
            modifiers[stat] = 1.1
        elif entry["lowered_stat"] == stat:
            modifiers[stat] = 0.9
        else:
            modifiers[stat] = 1.0
    return modifiers
