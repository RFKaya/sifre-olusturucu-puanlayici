import os
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

class BreachChecker:
    def __init__(self):
        self.offline_mode = os.getenv("OFFLINE_MODE", "false").lower() == "true"
        self.api_url = os.getenv("HIBP_API_URL", "https://api.pwnedpasswords.com/range/").strip()
        self.timeout = int(os.getenv("REQUEST_TIMEOUT_SECONDS", 5))

    def check_password_breaches(self, password: str) -> dict:
        """
        Queries Have I Been Pwned API securely using k-Anonymity.
        
        Returns:
            dict: {
                "status": "clean" | "breached" | "offline" | "error",
                "count": int (number of times leaked),
                "message": str (description)
            }
        """
        if self.offline_mode:
            return {
                "status": "offline",
                "count": 0,
                "message": "Offline mode active. Breach check skipped. / Çevrimdışı mod aktif. İhlal kontrolü atlandı."
            }

        if not password:
            return {
                "status": "clean",
                "count": 0,
                "message": "Empty password. / Boş parola."
            }

        try:
            # 1. Compute SHA-1 hash of the password (uppercase hex string)
            sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]

            # 2. Query HIBP range API
            url = f"{self.api_url}{prefix}"
            headers = {
                "User-Agent": "Password-Security-Analyzer-Academic-Project"
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 404:
                return {
                    "status": "clean",
                    "count": 0,
                    "message": "No breaches found. / Parola sızıntısı bulunamadı."
                }
            elif response.status_code != 200:
                return {
                    "status": "error",
                    "count": 0,
                    "message": f"API responded with status code {response.status_code}. / API hata kodu döndü: {response.status_code}"
                }

            # 3. Parse output to find suffix match
            # HIBP returns lines like: SUFFIX:COUNT
            lines = response.text.splitlines()
            breach_count = 0
            for line in lines:
                if ":" in line:
                    res_suffix, count_str = line.split(":", 1)
                    if res_suffix.upper() == suffix:
                        breach_count = int(count_str)
                        break

            if breach_count > 0:
                return {
                    "status": "breached",
                    "count": breach_count,
                    "message": f"CRITICAL: This password has been leaked {breach_count:,} times! / KRİTİK: Bu parola daha önce {breach_count:,} kez sızdırılmış!"
                }
            else:
                return {
                    "status": "clean",
                    "count": 0,
                    "message": "Safe: No breaches found in database. / Güvenli: Sızıntı veritabanında bulunamadı."
                }

        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "count": 0,
                "message": "Connection timeout when checking HIBP API. / HIBP API bağlantı zaman aşımı."
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "count": 0,
                "message": f"Network error: {str(e)} / Ağ hatası oluştu."
            }
        except Exception as e:
            return {
                "status": "error",
                "count": 0,
                "message": f"An unexpected error occurred: {str(e)} / Beklenmeyen hata oluştu."
            }
