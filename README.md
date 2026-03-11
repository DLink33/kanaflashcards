# Kana Flashcards

A Python app for practicing Japanese kana and vocabulary.

The app now reads flashcard content from **MySQL** (for both CLI and GUI). CSV files are treated as source data and imported into normalized database tables.

## Python version

Use **Python 3.11** to create the virtual environment (Python 3.10+ should also work, but 3.11 is the recommended target).

## Setup

1. Create a virtual environment:

```bash
python3.11 -m venv .venv
```

2. Activate it:

- macOS/Linux:

```bash
source .venv/bin/activate
```

- Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## MySQL setup for RHEL 8/9

Use the provided setup script to optionally install MySQL (via `dnf`), ensure `mysqld` is running, create the DB/user, create schema, and import all CSV files in the repo root.

```bash
python scripts/setup_mysql_db.py --ensure-mysql --root-user root --root-password '<root_password>'
```

If MySQL is already installed/running, omit `--ensure-mysql`.

### Environment variables

The app and import script read these values:

- `KANA_DB_HOST` (default `127.0.0.1`)
- `KANA_DB_PORT` (default `3306`)
- `KANA_DB_USER` (default `kana_user`)
- `KANA_DB_PASSWORD` (default `kana_password`)
- `KANA_DB_NAME` (default `kanaflashcards`)

## Updating data from CSV

To refresh database content after editing any CSV file, rerun:

```bash
python scripts/setup_mysql_db.py --root-user root --root-password '<root_password>'
```

The importer re-syncs deck content from all `*.csv` files in the specified CSV directory (default: repo root).

## Run the app

### CLI mode (default)

```bash
python main.py
```

### GUI mode (Tkinter)

```bash
python main.py --gui
```

## Run tests

From the project root:

```bash
python -m unittest -v
```
