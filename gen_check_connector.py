import string
from pathlib import Path

# -----------------------------
# Load wordlists once (cached)
# -----------------------------
_BASE_DIR = Path(__file__).resolve().parent
_LISTS_DIR = _BASE_DIR / "lists"

_COMMON_PW_PATH = _LISTS_DIR / "100k-most-used-passwords-NCSC.txt"
_WORDS_PATH = _LISTS_DIR / "words.txt"

def _load_set(path: Path) -> set[str]:
    # Using utf-8 with ignore to avoid odd characters crashing the app
    if not path.exists():
        # Fail loudly with a helpful message
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        return set(line.strip().lower() for line in f if line.strip())

COMMON_PASSWORDS = _load_set(_COMMON_PW_PATH)
ENGLISH_WORDS = _load_set(_WORDS_PATH)


# -----------------------------
# Public API: score_password()
# -----------------------------
def score_password(pw: str):
    """
    Scores password using the same logic as password-checker.py.

    Returns:
        score (int)          : raw score (can go negative due to penalties)
        strength (str)       : Very-Weak / Weak / Moderate / Strong / Very-Strong
        suggestions (list)   : list of suggestion strings
    """
    suggestions = []
    score = 0

    # ---- Length ----
    if pw == "":
        suggestions.append("Strong password suggestions will appear here!\n")
        return 0, "Very-Weak", suggestions

    if len(pw) < 8:
        suggestions.append("Passwords should be no shorter than 8 characters!\n")
        score += -50
    elif len(pw) < 12:
        suggestions.append("Medium passwords should be at least 12 characters!\n")
        score += 15
    elif len(pw) < 16:
        suggestions.append("The strongest passwords have more than 16 characters!\n")
        score += 20
    else:
        score += 25

    # ---- English words ----
    pw_lower = pw.lower()
    found_english = False
    for w in ENGLISH_WORDS:
        if len(w) >= 4 and w in pw_lower:
            suggestions.append("Avoid using english words in your password!\n")
            score += -10
            found_english = True
            break
    if not found_english:
        score += 5

    # ---- Common password ----
    pw_norm = pw.strip().lower()
    if pw_norm in COMMON_PASSWORDS:
        suggestions.append("This is a common password!!\n")
        score += -500
    else:
        score += 5

    # ---- Capitalization ----
    lower = any(c.islower() for c in pw)
    upper = any(c.isupper() for c in pw)

    if lower and upper:
        score += 25
    elif lower or upper:
        suggestions.append("Passwords should contain lower and uppercase characters\n")
        score += -20
    else:
        score += 0

    # ---- Special characters ----
    special_characters = set(string.punctuation)
    special_positions = [i for i, c in enumerate(pw) if c in special_characters]

    if not special_positions:
        suggestions.append("Consider adding some special characters!\n")
        score += 0
    else:
        n = len(pw)
        in_middle = [i for i in special_positions if not (i < 2 or i >= n - 2)]

        # Only edge specials
        if len(in_middle) == 0:
            suggestions.append("Special characters shouldn't only be at the beginning or end of a password!\n")
            score += 5
        # At least one middle special
        elif len(in_middle) == 1:
            score += 15
        else:
            score += 25

    # ---- Numbers ----
    digit_positions = [i for i, c in enumerate(pw) if c.isdigit()]
    if not digit_positions:
        suggestions.append("Consider adding some numbers!\n")
        score += 0
    else:
        n = len(pw)
        in_middle = [i for i in digit_positions if not (i < 2 or i >= n - 2)]

        # Detect ascending 3-digit sequence like 123
        sequence = False
        for i in range(len(pw) - 2):
            if pw[i].isdigit() and pw[i + 1].isdigit() and pw[i + 2].isdigit():
                if ord(pw[i + 1]) == ord(pw[i]) + 1 and ord(pw[i + 2]) == ord(pw[i]) + 2:
                    sequence = True
                    break

        if len(in_middle) == 0:
            num_score = 10
        elif len(in_middle) == 1:
            num_score = 20
        else:
            num_score = 30

        if sequence:
            suggestions.append("Avoid using sequences of numbers in your password!\n")
            num_score -= 10

        score += max(num_score, 0)

    # ---- Strength bucket (same thresholds as your UI) ----
    if score <= 20:
        strength = "Very-Weak"
    elif score <= 40:
        strength = "Weak"
    elif score <= 60:
        strength = "Moderate"
    elif score <= 80:
        strength = "Strong"
    else:
        strength = "Very-Strong"

    return score, strength, suggestions


def display_score(score: int) -> int:
    """
    Optional helper for UI display.
    Your raw scoring can go negative or over 100.
    RoboForm-ish UIs usually show 0-100, so clamp it.
    """
    return max(0, min(100, score))