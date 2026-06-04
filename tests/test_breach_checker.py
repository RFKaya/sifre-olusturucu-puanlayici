import pytest
from unittest.mock import patch, MagicMock
from src.breach_checker import BreachChecker

def test_breach_checker_offline():
    checker = BreachChecker()
    checker.offline_mode = True
    
    res = checker.check_password_breaches("testpassword")
    assert res["status"] == "offline"
    assert res["count"] == 0

@patch('requests.get')
def test_breach_checker_clean(mock_get):
    # Mocking standard HIBP Range API response when password is clean (not in returned suffixes)
    mock_response = MagicMock()
    mock_response.status_code = 200
    # Let's say suffix is NOT in this response
    mock_response.text = "ABCDEF12345:10\nFFAABBCCDD:25"
    mock_get.return_value = mock_response

    checker = BreachChecker()
    checker.offline_mode = False
    
    # We pass a password that yields a different SHA1 hash
    res = checker.check_password_breaches("completelyuniquepassword999!!!")
    assert res["status"] == "clean"
    assert res["count"] == 0

@patch('requests.get')
def test_breach_checker_breached(mock_get):
    # Let's mock a breached response
    # password "Password123" SHA1 hash: B2E98AD6F6EB8508DD6A14CFA704BAD7F05F6FB1
    # prefix: B2E98
    # suffix: AD6F6EB8508DD6A14CFA704BAD7F05F6FB1
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "AD6F6EB8508DD6A14CFA704BAD7F05F6FB1:4820\nFFAABBCCDD:25"
    mock_get.return_value = mock_response

    checker = BreachChecker()
    checker.offline_mode = False
    
    res = checker.check_password_breaches("Password123")
    assert res["status"] == "breached"
    assert res["count"] == 4820
