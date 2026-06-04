import pytest
from src.analyzer import PasswordAnalyzer

def test_password_entropy():
    analyzer = PasswordAnalyzer()
    
    # Empty password
    assert analyzer.calculate_entropy("") == 0.0
    
    # All lowercase: pool of 26
    # Entropy = 8 * log2(26) = 8 * 4.7004 = 37.60
    assert analyzer.calculate_entropy("password") == pytest.approx(37.60, abs=0.1)

    # Mixed uppercase & lowercase: pool of 52
    # Entropy = 8 * log2(52) = 8 * 5.7004 = 45.60
    assert analyzer.calculate_entropy("Password") == pytest.approx(45.60, abs=0.1)

def test_password_policy():
    analyzer = PasswordAnalyzer()
    
    # Configure strict rules manually for test predictability
    analyzer.min_length = 8
    analyzer.require_uppercase = True
    analyzer.require_lowercase = True
    analyzer.require_numbers = True
    analyzer.require_special = True
    analyzer.custom_blacklist = ["istinye", "bgt006"]
    
    # Test compliant password
    res = analyzer.check_policy("P@ssword123")
    assert res["is_compliant"] is True
    
    # Test short password
    res = analyzer.check_policy("P@s12")
    assert res["is_compliant"] is False
    assert res["rules"]["length"]["passed"] is False

    # Test missing special character
    res = analyzer.check_policy("Password123")
    assert res["is_compliant"] is False
    assert res["rules"]["special"]["passed"] is False

    # Test custom blacklist hit
    res = analyzer.check_policy("IstinyeP@ss123")
    assert res["is_compliant"] is False
    assert res["rules"]["blacklist"]["passed"] is False
    assert "istinye" in res["blacklisted_found"]
