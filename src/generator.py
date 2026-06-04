import secrets
import string

class PasswordGenerator:
    # A list of 100 simple, safe English words for generating Diceware-style passphrases
    DEFAULT_WORDLIST = [
        "apple", "banana", "cherry", "danger", "eagle", "forest", "garden", "harbor", "island",
        "jacket", "kitten", "lemon", "monkey", "nature", "ocean", "pencil", "quartz", "rabbit",
        "shadow", "tiger", "umbrella", "valley", "window", "yellow", "zebra", "active", "bright",
        "clever", "direct", "exotic", "flying", "gentle", "honest", "island", "jolly", "kindly",
        "lovely", "modern", "narrow", "oxygen", "polite", "quietly", "robust", "silent", "tender",
        "unique", "vibrant", "warmth", "youth", "zealous", "anchor", "beacon", "candle", "dune",
        "echo", "feather", "glimmer", "haven", "ivory", "journal", "kettle", "lantern", "meadow",
        "nomad", "oasis", "pebble", "quiver", "ripple", "summit", "timber", "urn", "velvet",
        "whisper", "yarn", "zenith", "brave", "chill", "dawn", "earth", "flame", "grace",
        "heart", "iron", "jade", "knight", "lunar", "mist", "night", "opal", "pearl",
        "quest", "river", "stone", "tower", "unity", "vocal", "wave", "amber", "bronze", "clay"
    ]

    def __init__(self):
        pass

    def generate(self, 
                 length: int = 16, 
                 use_upper: bool = True, 
                 use_lower: bool = True, 
                 use_digits: bool = True, 
                 use_special: bool = True,
                 exclude_similar: bool = True) -> str:
        """
        Generates a cryptographically secure random password based on requirements.
        """
        # Character pools
        upper_pool = string.ascii_uppercase
        lower_pool = string.ascii_lowercase
        digits_pool = string.digits
        # Safe special characters
        special_pool = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if exclude_similar:
            # Remove characters like: l, 1, I, o, 0, O, |, etc.
            similar_chars = "l1Io0O|`~'\""
            upper_pool = "".join(c for c in upper_pool if c not in similar_chars)
            lower_pool = "".join(c for c in lower_pool if c not in similar_chars)
            digits_pool = "".join(c for c in digits_pool if c not in similar_chars)
            special_pool = "".join(c for c in special_pool if c not in similar_chars)

        # Assemble pool
        pool = ""
        mandatory_chars = []

        if use_upper and upper_pool:
            pool += upper_pool
            mandatory_chars.append(secrets.choice(upper_pool))
        if use_lower and lower_pool:
            pool += lower_pool
            mandatory_chars.append(secrets.choice(lower_pool))
        if use_digits and digits_pool:
            pool += digits_pool
            mandatory_chars.append(secrets.choice(digits_pool))
        if use_special and special_pool:
            pool += special_pool
            mandatory_chars.append(secrets.choice(special_pool))

        if not pool:
            # Fallback if nothing is selected
            pool = string.ascii_lowercase
            mandatory_chars.append(secrets.choice(pool))

        # Fill remaining characters
        remaining_length = length - len(mandatory_chars)
        if remaining_length > 0:
            mandatory_chars.extend(secrets.choice(pool) for _ in range(remaining_length))

        # Shuffle the list to prevent predictable start characters
        secrets.SystemRandom().shuffle(mandatory_chars)

        return "".join(mandatory_chars[:length])

    def generate_passphrase(self, num_words: int = 4, separator: str = "-") -> str:
        """
        Generates a Diceware-style passphrase using a list of simple words.
        """
        words = [secrets.choice(self.DEFAULT_WORDLIST) for _ in range(num_words)]
        return separator.join(words)
