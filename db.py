import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional



@dataclass
class DBConfig:
    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "kana_user"
    password: str = "kana_password"
    database: str = "kanaflashcards"


def load_db_config() -> DBConfig:
    return DBConfig(
        host=os.getenv("KANA_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("KANA_DB_PORT", "3306")),
        user=os.getenv("KANA_DB_USER", "kana_user"),
        password=os.getenv("KANA_DB_PASSWORD", "kana_password"),
        database=os.getenv("KANA_DB_NAME", "kanaflashcards"),
    )


SCHEMA_SQL = [
    """
    CREATE TABLE IF NOT EXISTS decks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(128) NOT NULL UNIQUE,
        source_file VARCHAR(255) NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS cards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        deck_id INT NOT NULL,
        position INT NOT NULL,
        UNIQUE KEY unique_deck_position (deck_id, position),
        FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sides (
        id INT AUTO_INCREMENT PRIMARY KEY,
        deck_id INT NOT NULL,
        name VARCHAR(128) NOT NULL,
        UNIQUE KEY unique_side_name_per_deck (deck_id, name),
        FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS card_values (
        card_id INT NOT NULL,
        side_id INT NOT NULL,
        value TEXT NOT NULL,
        PRIMARY KEY (card_id, side_id),
        FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE,
        FOREIGN KEY (side_id) REFERENCES sides(id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tags (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(128) NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS card_tags (
        card_id INT NOT NULL,
        tag_id INT NOT NULL,
        PRIMARY KEY (card_id, tag_id),
        FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
    )
    """,
]


def parse_tags(raw: str) -> List[str]:
    if not raw:
        return []
    cleaned = raw.strip()
    if cleaned.startswith("[") and cleaned.endswith("]"):
        cleaned = cleaned[1:-1]
    return [token for token in cleaned.split() if token]


class MySQLFlashcardRepository:
    def __init__(self, config: Optional[DBConfig] = None):
        self.config = config or load_db_config()

    def connect(self, with_database: bool = True):
        kwargs = {
            "host": self.config.host,
            "port": self.config.port,
            "user": self.config.user,
            "password": self.config.password,
            "autocommit": False,
        }
        if with_database:
            kwargs["database"] = self.config.database
        import mysql.connector

        return mysql.connector.connect(**kwargs)

    def ensure_schema(self):
        conn = self.connect(with_database=True)
        cur = conn.cursor()
        try:
            for statement in SCHEMA_SQL:
                cur.execute(statement)
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def list_tags(self, deck_name: str) -> List[str]:
        conn = self.connect()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                SELECT DISTINCT t.name
                FROM decks d
                JOIN cards c ON c.deck_id = d.id
                JOIN card_tags ct ON ct.card_id = c.id
                JOIN tags t ON t.id = ct.tag_id
                WHERE d.name = %s
                ORDER BY t.name
                """,
                (deck_name,),
            )
            return [row[0] for row in cur.fetchall()]
        finally:
            cur.close()
            conn.close()

    def load_deck(self, deck_name: str) -> List[Dict[str, str]]:
        conn = self.connect()
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id FROM decks WHERE name=%s", (deck_name,))
            deck_row = cur.fetchone()
            if not deck_row:
                raise ValueError(f"Deck '{deck_name}' was not found in database")
            deck_id = deck_row["id"]

            cur.execute(
                "SELECT id, name FROM sides WHERE deck_id=%s ORDER BY id",
                (deck_id,),
            )
            sides = cur.fetchall()
            side_names = {row["id"]: row["name"] for row in sides}

            cur.execute(
                "SELECT id, position FROM cards WHERE deck_id=%s ORDER BY position",
                (deck_id,),
            )
            cards = cur.fetchall()

            deck_cards: List[Dict[str, str]] = []
            for card in cards:
                card_id = card["id"]
                cur.execute(
                    "SELECT side_id, value FROM card_values WHERE card_id=%s",
                    (card_id,),
                )
                values = {
                    side_names[row["side_id"]]: row["value"]
                    for row in cur.fetchall()
                }

                cur.execute(
                    """
                    SELECT t.name
                    FROM card_tags ct
                    JOIN tags t ON t.id = ct.tag_id
                    WHERE ct.card_id=%s
                    ORDER BY t.name
                    """,
                    (card_id,),
                )
                tags = [row["name"] for row in cur.fetchall()]
                if tags:
                    values["tags"] = "[" + " ".join(tags) + "]"
                elif "tags" not in values:
                    values["tags"] = "[]"

                deck_cards.append(values)

            return deck_cards
        finally:
            cur.close()
            conn.close()


def discover_csv_decks(base_dir: Path) -> List[Path]:
    return sorted(base_dir.glob("*.csv"))


def import_csv_deck(repo: MySQLFlashcardRepository, csv_path: Path):
    deck_name = csv_path.stem.lower()
    conn = repo.connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO decks (name, source_file) VALUES (%s, %s) ON DUPLICATE KEY UPDATE source_file=VALUES(source_file)",
            (deck_name, csv_path.name),
        )
        cur.execute("SELECT id FROM decks WHERE name=%s", (deck_name,))
        deck_id = cur.fetchone()[0]

        cur.execute("DELETE FROM card_tags WHERE card_id IN (SELECT id FROM cards WHERE deck_id=%s)", (deck_id,))
        cur.execute("DELETE FROM card_values WHERE card_id IN (SELECT id FROM cards WHERE deck_id=%s)", (deck_id,))
        cur.execute("DELETE FROM sides WHERE deck_id=%s", (deck_id,))
        cur.execute("DELETE FROM cards WHERE deck_id=%s", (deck_id,))

        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                conn.commit()
                return

            normalized_headers = [header.lower() for header in reader.fieldnames]
            side_headers = [h for h in normalized_headers if h != "tags"]
            side_id_map = {}
            for side_name in side_headers:
                cur.execute("INSERT INTO sides (deck_id, name) VALUES (%s, %s)", (deck_id, side_name))
                side_id_map[side_name] = cur.lastrowid

            for position, row in enumerate(reader):
                normalized = {k.lower(): (v if v is not None else "") for k, v in row.items()}
                cur.execute(
                    "INSERT INTO cards (deck_id, position) VALUES (%s, %s)",
                    (deck_id, position),
                )
                card_id = cur.lastrowid

                for side_name in side_headers:
                    cur.execute(
                        "INSERT INTO card_values (card_id, side_id, value) VALUES (%s, %s, %s)",
                        (card_id, side_id_map[side_name], normalized.get(side_name, "")),
                    )

                for tag in parse_tags(normalized.get("tags", "")):
                    cur.execute("INSERT INTO tags (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=name", (tag,))
                    cur.execute("SELECT id FROM tags WHERE name=%s", (tag,))
                    tag_id = cur.fetchone()[0]
                    cur.execute(
                        "INSERT IGNORE INTO card_tags (card_id, tag_id) VALUES (%s, %s)",
                        (card_id, tag_id),
                    )

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
