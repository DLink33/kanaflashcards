# Kana Flashcards

A small Python app for practicing Japanese kana and vocabulary from CSV decks.

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
