import os
import sys
import argparse

# Proje kök dizinini sys.path listesine ekleyerek her iki çalıştırma yöntemini de destekliyoruz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analyzer import PasswordAnalyzer
from src.breach_checker import BreachChecker
from src.generator import PasswordGenerator
from src.cli import display_analysis, run_interactive_loop, display_header

# Ensure terminal outputs UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(
        description="Parola Güvenlik Analizörü & Üreticisi / Password Security Analyzer & Generator"
    )
    parser.add_argument(
        "-p", "--password",
        type=str,
        help="Analiz edilecek parola / Password to analyze directly"
    )
    parser.add_argument(
        "-g", "--generate",
        action="store_true",
        help="Doğrudan güvenli parola üret / Generate a secure password directly"
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=16,
        help="Üretilecek parola uzunluğu (Varsayılan: 16) / Length of the generated password (Default: 16)"
    )

    args = parser.parse_args()

    # Route logic based on arguments
    if args.password:
        analyzer = PasswordAnalyzer()
        breach_checker = BreachChecker()
        display_header()
        display_analysis(args.password, analyzer, breach_checker)
        sys.exit(0)

    elif args.generate:
        generator = PasswordGenerator()
        analyzer = PasswordAnalyzer()
        breach_checker = BreachChecker()
        
        display_header()
        generated = generator.generate(length=args.length)
        print(f"\nÜretilen Parola / Generated Password:\n{generated}\n")
        display_analysis(generated, analyzer, breach_checker)
        sys.exit(0)

    else:
        # Launch interactive CLI menu
        try:
            run_interactive_loop()
        except (KeyboardInterrupt, EOFError):
            print("\n\nProgram sonlandırıldı. / Program terminated.")
            sys.exit(0)

if __name__ == "__main__":
    main()
