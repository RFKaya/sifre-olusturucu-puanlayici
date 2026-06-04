import getpass
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import BarColumn, Progress
from rich import print as rprint
from src.analyzer import PasswordAnalyzer
from src.breach_checker import BreachChecker
from src.generator import PasswordGenerator

console = Console()

def display_header():
    """
    Renders a premium university project header.
    """
    header_content = (
        "[bold cyan]İSTİNYE ÜNİVERSİTESİ[/bold cyan] • Siber Güvenlik Bölümü\n"
        "[bold white]BGT006 Sızma Testi Dersi Bahar 2025-2026 Final Projesi[/bold white]\n"
        "[bold magenta]PAROLA GÜVENLİK ANALİZÖRÜ & ÜRETİCİSİ[/bold magenta]\n"
        "─────────────────────────────────────────────────────────────\n"
        "[dim]Danışman: Keyvan Arasteh (@keyvanarasteh) | qline.tech[/dim]"
    )
    console.print(Panel(header_content, style="cyan", border_style="cyan", expand=False))

def display_policy_settings(analyzer: PasswordAnalyzer):
    """
    Renders current policy rules.
    """
    table = Table(title="Aktif Parola Politikası / Active Password Policy", border_style="blue")
    table.add_column("Kural / Rule", style="bold white")
    table.add_column("Gereksinim / Requirement", style="yellow")

    table.add_row("Min Uzunluk / Min Length", str(analyzer.min_length))
    table.add_row("Büyük Harf / Uppercase", "Zorunlu / Required" if analyzer.require_uppercase else "İsteğe Bağlı / Optional")
    table.add_row("Küçük Harf / Lowercase", "Zorunlu / Required" if analyzer.require_lowercase else "İsteğe Bağlı / Optional")
    table.add_row("Rakam / Number", "Zorunlu / Required" if analyzer.require_numbers else "İsteğe Bağlı / Optional")
    table.add_row("Özel Karakter / Special Char", "Zorunlu / Required" if analyzer.require_special else "İsteğe Bağlı / Optional")
    
    blacklist_status = "Aktif / Active" if analyzer.custom_blacklist else "Pasif / Inactive"
    if analyzer.custom_blacklist:
        blacklist_status += f" (Engellenen: {', '.join(analyzer.custom_blacklist)})"
    table.add_row("Özel Sözlük Filtresi / Dictionary", blacklist_status)

    console.print(table)

def display_analysis(password: str, analyzer: PasswordAnalyzer, breach_checker: BreachChecker):
    """
    Performs full analysis of the password and prints the results in a beautiful format.
    """
    if not password:
        console.print("[red]Hata: Boş şifre analiz edilemez. / Error: Empty password cannot be analyzed.[/red]")
        return

    # Run checks
    policy = analyzer.check_policy(password)
    strength = analyzer.analyze_strength(password)
    
    with console.status("[bold yellow]Sızıntı kontrolü yapılıyor (HIBP API)... / Checking breaches...[/bold yellow]"):
        breach = breach_checker.check_password_breaches(password)

    # 1. Title Panel
    console.print("\n[bold green]📊 ANALİZ SONUÇLARI / ANALYSIS RESULTS[/bold green]")
    
    # 2. Score bar / progress
    score = strength["score"] # 0 to 4
    score_colors = {
        0: "red",
        1: "orange3",
        2: "yellow",
        3: "green3",
        4: "bright_green"
    }
    color = score_colors[score]
    
    # Custom ASCII strength bar
    score_bar = "█" * (score + 1) + "░" * (4 - score)
    
    score_info = (
        f"Güç Seviyesi / Strength Score: [bold {color}]{strength['label']} ({score}/4)[/bold {color}]\n"
        f"Görsel Seviye / Progress Bar:  [bold {color}]{score_bar}[/bold {color}]\n"
        f"Tahmin Hızı / Guesses Complexity: [bold white]{strength['guesses']:,}[/bold white]"
    )
    console.print(Panel(score_info, title="Parola Gücü / Password Strength", border_style=color))

    # 3. Policy Compliance Table
    policy_table = Table(title="Politika Uyumluluk Tablosu / Policy Compliance Table", border_style="cyan")
    policy_table.add_column("Kriter / Criteria", style="bold white")
    policy_table.add_column("Durum / Status", justify="center")
    policy_table.add_column("Değer / Actual Value", style="yellow")

    for key, rule in policy["rules"].items():
        status = "[bold green]✓ GEÇTİ[/bold green]" if rule["passed"] else "[bold red]✗ KALDI[/bold red]"
        policy_table.add_row(rule["description"], status, rule["value"])

    status_overall = "[bold green]✓ UYUMLU / COMPLIANT[/bold green]" if policy["is_compliant"] else "[bold red]✗ UYUMSUZ / NON-COMPLIANT[/bold red]"
    policy_table.add_row("[bold white]Genel Uyum / Overall Compliance[/bold white]", status_overall, "")
    console.print(policy_table)

    # 4. Crack Times Table
    crack_table = Table(title="Tahmini Kırma Süreleri / Estimated Crack Times", border_style="magenta")
    crack_table.add_column("Saldırı Türü / Attack Type", style="bold white")
    crack_table.add_column("Tahmini Süre / Estimated Time", style="bold yellow")
    
    crack_table.add_row("Çevrimiçi Limitli (10/sn) / Online Throttled", strength["online_throttled_time"])
    crack_table.add_row("Çevrimdışı Hızlı (1e10/sn) / Offline Fast Hash", strength["offline_fast_hash_time"])
    console.print(crack_table)

    # 5. Breach Check Panel
    breach_status = breach["status"]
    if breach_status == "breached":
        breach_panel = Panel(
            f"[bold red]⚠️ TEHLİKE / DANGER[/bold red]\n\n"
            f"Bu parola daha önce [bold red]{breach['count']:,}[/bold red] kez sızıntılarda görülmüş!\n"
            f"NIST kurallarına göre bu şifreyi [bold red]KULLANMAYIN[/bold red].",
            border_style="red",
            title="Veri İhlali Durumu / Breach Status"
        )
    elif breach_status == "clean":
        breach_panel = Panel(
            f"[bold green]✓ GÜVENLİ / SAFE[/bold green]\n\n"
            f"Parola bilinen hiçbir veri sızıntısında tespit edilmedi.\n"
            f"Have I Been Pwned veritabanında kaydı yok.",
            border_style="green",
            title="Veri İhlali Durumu / Breach Status"
        )
    elif breach_status == "offline":
        breach_panel = Panel(
            f"[yellow]ℹ ÇEVRİMDIŞI MOD / OFFLINE MODE[/yellow]\n\n"
            f"Sızıntı sorgusu atlandı.",
            border_style="yellow",
            title="Veri İhlali Durumu / Breach Status"
        )
    else:
        breach_panel = Panel(
            f"[red]⚠️ HATA / ERROR[/red]\n\n"
            f"{breach['message']}",
            border_style="red",
            title="Veri İhlali Durumu / Breach Status"
        )
    console.print(breach_panel)

    # 6. Suggestions
    suggestions = strength["suggestions"]
    warning = strength["warning"]
    if warning or suggestions or not policy["is_compliant"] or breach_status == "breached":
        console.print("\n[bold yellow]💡 İyileştirme Önerileri / Security Suggestions:[/bold yellow]")
        if warning:
            console.print(f"  • [bold red]Uyarı:[/bold red] {warning}")
        for sug in suggestions:
            console.print(f"  • {sug}")
        if not policy["is_compliant"]:
            console.print("  • Parola politikası kriterlerini karşılayacak şekilde karakter ekleyin.")
        if breach_status == "breached":
            console.print("  • Parolanız sızdırıldığı için derhal değiştirin ve benzersiz bir parola seçin.")
    console.print("\n" + "═" * 60 + "\n")

def run_interactive_loop():
    """
    Main interactive shell loop.
    """
    analyzer = PasswordAnalyzer()
    breach_checker = BreachChecker()
    generator = PasswordGenerator()

    while True:
        display_header()
        
        rprint("[bold white]Ana Menü / Main Menu:[/bold white]")
        rprint("  [cyan]1.[/cyan] Parola Analiz Et / Analyze Password")
        rprint("  [cyan]2.[/cyan] Güvenli Parola Üret / Generate Secure Password")
        rprint("  [cyan]3.[/cyan] Parola Grubu (Passphrase) Üret / Generate Passphrase")
        rprint("  [cyan]4.[/cyan] Aktif Politikaları Görüntüle / View Active Policies")
        rprint("  [cyan]5.[/cyan] Çıkış / Exit")
        
        choice = input("\nSeçiminiz / Enter choice (1-5): ").strip()

        if choice == "1":
            # Mask input for safety
            password = getpass.getpass("Analiz edilecek parolayı girin (yazarken gizlenir): ")
            display_analysis(password, analyzer, breach_checker)
            input("Devam etmek için ENTER tuşuna basın... / Press ENTER to continue...")
        elif choice == "2":
            try:
                length_str = input("Uzunluk girin / Enter length [default: 16]: ").strip()
                length = int(length_str) if length_str else 16
                
                exclude_sim = input("Benzer karakterler hariç tutulsun mu (1, l, o, O vb.)? (E/h) / Exclude similar? (Y/n): ").strip().lower() != "h"
                
                generated = generator.generate(length=length, exclude_similar=exclude_sim)
                
                rprint(f"\n[bold green]✓ Güvenli Parola Üretildi / Secure Password Generated:[/bold green]")
                rprint(Panel(f"[bold yellow]{generated}[/bold yellow]", style="white"))
                
                # Automatically score the generated password
                display_analysis(generated, analyzer, breach_checker)
            except ValueError:
                rprint("[red]Hata: Geçersiz uzunluk girdiniz.[/red]")
            input("Devam etmek için ENTER tuşuna basın... / Press ENTER to continue...")
        elif choice == "3":
            try:
                words_str = input("Kelime sayısı / Word count [default: 4]: ").strip()
                words = int(words_str) if words_str else 4
                
                sep = input("Ayırıcı karakter / Separator [default: -]: ").strip()
                if not sep:
                    sep = "-"
                    
                passphrase = generator.generate_passphrase(num_words=words, separator=sep)
                rprint(f"\n[bold green]✓ Parola Grubu Üretildi / Passphrase Generated:[/bold green]")
                rprint(Panel(f"[bold yellow]{passphrase}[/bold yellow]", style="white"))
                
                display_analysis(passphrase, analyzer, breach_checker)
            except ValueError:
                rprint("[red]Hata: Geçersiz kelime sayısı girdiniz.[/red]")
            input("Devam etmek için ENTER tuşuna basın... / Press ENTER to continue...")
        elif choice == "4":
            display_policy_settings(analyzer)
            input("Devam etmek için ENTER tuşuna basın... / Press ENTER to continue...")
        elif choice == "5":
            rprint("[green]Program kapatılıyor. İyi çalışmalar! / Exiting, have a safe day![/green]")
            break
        else:
            rprint("[red]Geçersiz seçim. Tekrar deneyin. / Invalid choice, try again.[/red]")
            input("Devam etmek için ENTER tuşuna basın... / Press ENTER to continue...")
        
        # Clear screen for next iteration
        console.clear()
