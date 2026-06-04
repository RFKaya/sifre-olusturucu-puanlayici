import os
import math
import re
from dotenv import load_dotenv
from zxcvbn import zxcvbn

# Load environment variables
load_dotenv()

class PasswordAnalyzer:
    def __init__(self):
        # Load policy configurations with defaults
        self.min_length = int(os.getenv("MIN_PASSWORD_LENGTH", 12))
        self.require_uppercase = os.getenv("REQUIRE_UPPERCASE", "true").lower() == "true"
        self.require_lowercase = os.getenv("REQUIRE_LOWERCASE", "true").lower() == "true"
        self.require_numbers = os.getenv("REQUIRE_NUMBERS", "true").lower() == "true"
        self.require_special = os.getenv("REQUIRE_SPECIAL_CHARACTERS", "true").lower() == "true"
        
        # Load custom blacklist
        blacklist_str = os.getenv("CUSTOM_BLACKLIST_WORDS", "")
        self.custom_blacklist = [
            word.strip().lower() 
            for word in blacklist_str.split(",") 
            if word.strip()
        ]

    def check_policy(self, password: str) -> dict:
        """
        Validates the password against the configured security policies.
        """
        length_ok = len(password) >= self.min_length
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        # Special character definition: punctuation and symbols
        special_chars_regex = re.compile(r'[!@#$%^&*(),.?":{}|<>[\]\\\'`~_\-+=;/]')
        has_special = bool(special_chars_regex.search(password))
        
        # Check custom blacklist words
        blacklisted_found = []
        password_lower = password.lower()
        for word in self.custom_blacklist:
            if word in password_lower:
                blacklisted_found.append(word)
                
        blacklist_ok = len(blacklisted_found) == 0

        # Build policy evaluations
        rules = {
            "length": {
                "description": f"Minimum length / Minimum uzunluk ({self.min_length})",
                "passed": length_ok,
                "value": f"{len(password)} chars"
            }
        }
        
        if self.require_uppercase:
            rules["uppercase"] = {
                "description": "Uppercase letters / Büyük harf",
                "passed": has_upper,
                "value": "Yes" if has_upper else "No"
            }
        if self.require_lowercase:
            rules["lowercase"] = {
                "description": "Lowercase letters / Küçük harf",
                "passed": has_lower,
                "value": "Yes" if has_lower else "No"
            }
        if self.require_numbers:
            rules["numbers"] = {
                "description": "Numeric digits / Rakam",
                "passed": has_digit,
                "value": "Yes" if has_digit else "No"
            }
        if self.require_special:
            rules["special"] = {
                "description": "Special characters / Özel karakter",
                "passed": has_special,
                "value": "Yes" if has_special else "No"
            }
            
        rules["blacklist"] = {
            "description": "Custom dictionary check / Özel sözlük engeli",
            "passed": blacklist_ok,
            "value": "Passed" if blacklist_ok else f"Failed (Matched: {', '.join(blacklisted_found)})"
        }

        is_compliant = all(rule["passed"] for rule in rules.values())

        return {
            "is_compliant": is_compliant,
            "rules": rules,
            "blacklisted_found": blacklisted_found
        }

    def calculate_entropy(self, password: str) -> float:
        """
        Calculates mathematical entropy based on character pool size.
        H = L * log2(R)
        """
        if not password:
            return 0.0

        pool_size = 0
        if any(c.islower() for c in password):
            pool_size += 26
        if any(c.isupper() for c in password):
            pool_size += 26
        if any(c.isdigit() for c in password):
            pool_size += 10
        # If there are any characters not covered above, they are considered special/other characters
        has_other = any(not (c.isalnum()) for c in password)
        if has_other:
            pool_size += 33 # Standard printable ASCII special character set count

        # If pool size is still 0 (e.g. non-ascii letters, fallback to 256 for bytes representation)
        if pool_size == 0:
            pool_size = 256

        entropy = len(password) * math.log2(pool_size)
        return round(entropy, 2)

    def analyze_strength(self, password: str) -> dict:
        """
        Leverages zxcvbn to evaluate password strength realistically.
        """
        res = zxcvbn(password)
        
        score = res.get("score", 0)  # 0 to 4
        feedback = res.get("feedback", {})
        warning = feedback.get("warning", "")
        suggestions = feedback.get("suggestions", [])
        
        # Human readable crack times estimations
        crack_times = res.get("crack_times_display", {})
        online_throttled = crack_times.get("online_no_throttling_10_per_second", "instant")
        offline_fast = crack_times.get("offline_fast_hashing_1e10_per_second", "instant")

        # Map zxcvbn score to human-readable label
        score_labels = {
            0: "Too Weak / Çok Zayıf",
            1: "Weak / Zayıf",
            2: "Fair / Orta",
            3: "Strong / Güçlü",
            4: "Very Strong / Çok Güçlü"
        }
        
        return {
            "score": score,
            "label": score_labels.get(score, "Unknown"),
            "warning": warning,
            "suggestions": suggestions,
            "online_throttled_time": online_throttled,
            "offline_fast_hash_time": offline_fast,
            "guesses": res.get("guesses", 0)
        }
