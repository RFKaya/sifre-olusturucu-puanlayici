# ROADMAP — Parola Güvenlik Analizörü
# ROADMAP — Password Security Analyzer

> Course / Ders: Penetration Testing (BGT006) · Istinye University
> Instructor / Danışman: Keyvan Arasteh

---

## Phase 0 / Faz 0: Understand Before You Build / Yazmadan Önce Anla

Before writing a single line of code, I answered these questions:
Tek satır kod yazmadan önce şu soruları yanıtladım:

- **What is the project? / Proje nedir?**
  A command-line and interactive application to evaluate password strength, analyze security policy compliance, detect patterns (keyboard walks, dictionary words, etc.), and securely query Have I Been Pwned database using k-anonymity to see if the password has been leaked.

- **How does it work? / Nasıl çalışır?**
  1. It reads password inputs from the user securely (hiding input characters).
  2. Evaluates the password compliance against customizable rules (.env configured).
  3. Uses `zxcvbn` to calculate entropy and guess-strength (rating it from 0 to 4).
  4. Hashes the password using SHA-1, sends the first 5 characters to Have I Been Pwned Range API, receives a list of suffixes, and searches for a match locally.
  5. Displays a beautiful terminal dashboard with detailed reports and suggestions.

- **What are the inputs/outputs? / Girdiler/çıktılar neler?**
  - **Input**: User-provided password, custom policy configurations via environment variables (`.env`).
  - **Output**: Multi-section security assessment report (Policy check table, entropy & zxcvbn details, HIBP breach count, recommendations) formatted beautifully in the terminal.

- **What tools will I use and why? / Hangi araçları kullanacağım ve neden?**
  - Python: Main language of development.
  - `zxcvbn-python`: Realistic password strength evaluation.
  - `requests`: HTTP client to query HIBP Range API.
  - `rich`: Formatting clean, premium, and readable CLI tables, panels, and colors.
  - `pytest`: Automation of unit tests.

---

## Phase 1 / Faz 1: Research & Investigation / Araştırma ve Keşif

> Folder / Klasör: `docs/research/`

| Topic / Konu | Status / Durum | Notes / Notlar |
|--------------|----------------|----------------|
| Password Entropy & zxcvbn | ⚡ Completed / Tamamlandı | Detail in `docs/research/research_notes.md` |
| HIBP k-Anonymity Range API | ⚡ Completed / Tamamlandı | Detail in `docs/research/research_notes.md` |
| NIST SP 800-63B Standards | ⚡ Completed / Tamamlandı | Detail in `docs/research/research_notes.md` |

---

## Phase 2 / Faz 2: Environment Setup / Ortam Kurulumu

- [ ] Isolated lab environment (Docker / VM) / İzole lab ortamı
- [ ] Tools installed and verified / Araçlar kuruldu ve test edildi
- [ ] `.env.example` created / oluşturuldu

---

## Phase 3 / Faz 3: Implementation / Uygulama

### Module / Modül: Password Analyzer & Checker

1. **Step 1 / Adım 1** — Initialize project configuration and environment parser (`cli.py`, `main.py`).
2. **Step 2 / Adım 2** — Build the core analyzer (`analyzer.py`) integrating `zxcvbn` and policy verification checks.
3. **Step 3 / Adım 3** — Develop the secure leak check module (`breach_checker.py`) connecting to Have I Been Pwned API via k-Anonymity.
4. **Step 4 / Adım 4** — Build interactive/batch UI shell using the `rich` layout engine.
5. **Step 5 / Adım 5** — Add helper generator module (`generator.py`) to suggest strong passwords to users when theirs are weak.

---

## Phase 4 / Faz 4: Testing & Reporting / Test ve Raporlama

- [ ] Ran tests against target/sample / Hedef/örnek üzerinde testler çalıştırıldı
- [ ] Documented all findings with evidence / Tüm bulgular kanıtlarıyla belgelendi
- [ ] Wrote final report (Markdown) / Final raporu yazıldı

---

## Phase 5 / Faz 5: Delivery / Teslim

- [ ] GitHub repository is clean and organized / Repo temiz ve düzenli
- [ ] README.md complete / eksiksiz
- [ ] Docker verified (`docker-compose up`) / doğrulandı
- [ ] Instructor invited as collaborator / Danışman collaborator olarak eklendi → **keyvanarasteh**

---

## What I Learned / Öğrendiklerim

[Honest reflection: What was hard? What surprised you? / Dürüst değerlendirme: Ne zordu? Ne sizi şaşırttı?]

