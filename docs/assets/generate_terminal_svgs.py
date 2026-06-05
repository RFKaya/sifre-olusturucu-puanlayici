import os
import sys
import io

# Proje kök dizinini sys.path'e ekliyoruz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from rich.console import Console
import src.cli
from src.analyzer import PasswordAnalyzer
from src.breach_checker import BreachChecker

def generate_svgs():
    assets_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Zayıf Parola Analizi
    # Console'u StringIO ile oluşturup Windows cp1254 kodlama sorununu aşıyoruz
    buffer_weak = io.StringIO()
    src.cli.console = Console(file=buffer_weak, record=True, width=85, force_terminal=True, color_system="truecolor")
    
    analyzer = PasswordAnalyzer()
    breach_checker = BreachChecker()
    
    src.cli.display_header()
    src.cli.display_analysis("sifre123", analyzer, breach_checker)
    
    svg_weak_path = os.path.join(assets_dir, "analysis_weak.svg")
    src.cli.console.save_svg(svg_weak_path, title="Zayıf Parola Analizi / Weak Password Analysis")
    print(f"Oluşturuldu: {svg_weak_path}")

    # 2. Güçlü Parola Analizi
    buffer_strong = io.StringIO()
    src.cli.console = Console(file=buffer_strong, record=True, width=85, force_terminal=True, color_system="truecolor")
    
    src.cli.display_header()
    
    strong_pwd = "K3yv@n_Ar@st3h_IsU_2026!"
    # CLI çıktısında parolanın yazdırılmasını taklit edelim
    src.cli.console.print(f"\nAnaliz Edilen Parola / Password Analyzed: [bold yellow]{strong_pwd}[/bold yellow]\n")
    src.cli.display_analysis(strong_pwd, analyzer, breach_checker)
    
    svg_strong_path = os.path.join(assets_dir, "analysis_strong.svg")
    src.cli.console.save_svg(svg_strong_path, title="Güçlü Parola Analizi / Strong Password Analysis")
    print(f"Oluşturuldu: {svg_strong_path}")

if __name__ == "__main__":
    generate_svgs()
