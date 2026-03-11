#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

import mysql.connector

from db import DBConfig, MySQLFlashcardRepository, discover_csv_decks, import_csv_deck, load_db_config


def run_cmd(cmd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def ensure_mysql_rhel():
    run_cmd(["sudo", "dnf", "-y", "install", "mysql-server"])
    run_cmd(["sudo", "systemctl", "enable", "--now", "mysqld"])
    run_cmd(["sudo", "systemctl", "is-active", "--quiet", "mysqld"])


def ensure_database_and_user(config: DBConfig, root_user: str, root_password: str):
    conn = mysql.connector.connect(
        host=config.host,
        port=config.port,
        user=root_user,
        password=root_password,
        autocommit=True,
    )
    cur = conn.cursor()
    try:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{config.database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cur.execute(
            f"CREATE USER IF NOT EXISTS '{config.user}'@'%' IDENTIFIED BY %s",
            (config.password,),
        )
        cur.execute(
            f"ALTER USER '{config.user}'@'%' IDENTIFIED BY %s",
            (config.password,),
        )
        cur.execute(
            f"GRANT ALL PRIVILEGES ON `{config.database}`.* TO '{config.user}'@'%'"
        )
        cur.execute("FLUSH PRIVILEGES")
    finally:
        cur.close()
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Install/setup MySQL and import flashcard CSVs")
    parser.add_argument("--ensure-mysql", action="store_true", help="Install and start MySQL service on RHEL 8/9 using dnf")
    parser.add_argument("--root-user", default="root", help="MySQL admin username")
    parser.add_argument("--root-password", default="", help="MySQL admin password")
    parser.add_argument("--csv-dir", default=".", help="Directory containing CSV files")
    args = parser.parse_args()

    if args.ensure_mysql:
        ensure_mysql_rhel()

    config = load_db_config()
    ensure_database_and_user(config, args.root_user, args.root_password)

    repo = MySQLFlashcardRepository(config)
    repo.ensure_schema()

    csv_dir = Path(args.csv_dir).resolve()
    for csv_path in discover_csv_decks(csv_dir):
        print(f"Importing {csv_path.name} -> deck '{csv_path.stem.lower()}'")
        import_csv_deck(repo, csv_path)

    print("MySQL setup and CSV import complete.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"Command failed: {exc}", file=sys.stderr)
        sys.exit(exc.returncode)
