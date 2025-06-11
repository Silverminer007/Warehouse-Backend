# Packliste FastAPI Projekt

Dieses Projekt generiert Packlisten-PDFs via FastAPI, nutzt automatische Versionierung (SemVer) mit [semantic-release](https://semantic-release.gitbook.io/semantic-release/), baut und pusht Docker-Images in GHCR, und validiert Commit-Messages nach Conventional Commits.

---

## Voraussetzungen

- Python 3.11+
- Node.js 20+ (für semantic-release und commitlint)
- Docker (für Image-Builds)
- Git
- `npm` und `pip` Paketmanager
- `pre-commit` (optional, für Commit-Hooks)

---

## Repository klonen und Setup (Neuer PC)

```bash
# 1. Repo klonen
git clone https://github.com/deinbenutzername/deinrepo.git
cd deinrepo

# 2. Python-Umgebung einrichten (optional, empfohlen)
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# .\venv\Scripts\activate      # Windows PowerShell

# 3. Python-Abhängigkeiten installieren
pip install -r requirements.txt

# 4. Node.js Pakete installieren (global empfohlen)
npm install -g semantic-release @semantic-release/git @semantic-release/github @semantic-release/commit-analyzer @semantic-release/release-notes-generator @semantic-release/changelog @commitlint/cli @commitlint/config-conventional

# 5. Pre-commit Hook installieren (optional, empfohlen)
pip install pre-commit
pre-commit install --hook-type commit-msg
