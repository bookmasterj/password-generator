import secrets
import string
from password_checker_connector import score_password, display_score

# Character sets
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
symbols = string.punctuation

# Combine all characters
all_chars = lowercase + uppercase + digits + symbols

# Password length (RoboForm default-ish)
length = 16

# Generate secure password
pw = ''.join(secrets.choice(all_chars) for _ in range(length))

print("Generated Password:", pw)

# Send password to checker
raw_score, strength, suggestions = score_password(pw)

score_for_ui = display_score(raw_score)

print("Score:", score_for_ui)
print("Strength:", strength)
print("Suggestions:")
print("".join(suggestions))