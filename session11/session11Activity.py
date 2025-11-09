"""
Northwind SQLite Browser (CLI)

This program connects to a SQLite Northwind database, lists tables (stored in a
Python list), allows the user to select a table, displays all records with
column names and row numbers, and supports (I)nsert, (U)pdate, and (D)elete.
"""

from __future__ import annotations
import sys
import sqlite3
from typing import List, Tuple, Any, Dict, Optional

def connect_db(db_path: str) -> sqlite3.Connection:
    """
    Open a read/write connection to the SQLite database.

    Args:
        db_path: Path to the SQLite database file.

    Returns:
        sqlite3.Connection: An open database connection.

    Raises:
        sqlite3.Error: If the database cannot be opened.
        ValueError: If db_path appears empty.
    """
    if not db_path:
        raise ValueError("Database path must not be empty.")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def list_tables(conn: sqlite3.Connection) -> List[str]:
    """
    Retrieve a list of user tables in the database.

    Args:
        conn: Open SQLite connection.

    Returns:
        List[str]: Table names sorted alphabetically.
    """
    sql = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name COLLATE NOCASE;
    """
    cur = conn.execute(sql)
    return [row["name"] for row in cur.fetchall()]


def get_table_schema(conn: sqlite3.Connection, table: str) -> List[Dict[str, Any]]:
    """
    Get schema info for a table via PRAGMA table_info.

    Args:
        conn: Open SQLite connection.
        table: Table name.

    Returns:
        List[Dict[str, Any]]: Each dict has keys: cid, name, type, notnull, dflt_value, pk
    """
    rows = conn.execute(f"PRAGMA table_info({quote_ident(table)});").fetchall()
    return [dict(row) for row in rows]


def get_primary_key_columns(schema: List[Dict[str, Any]]) -> List[str]:
    """
    Determine primary key column names from table schema.

    Args:
        schema: Output of get_table_schema.

    Returns:
        List[str]: PK columns in ordinal order (pk>0 sorted by pk).
    """
    pk_cols = sorted([col for col in schema if col["pk"] > 0], key=lambda c: c["pk"])
    return [c["name"] for c in pk_cols]


def has_rowid_storage(conn: sqlite3.Connection, table: str) -> bool:
    """
    Check whether a table uses rowid storage (i.e., not declared WITHOUT ROWID).

    Args:
        conn: Open SQLite connection.
        table: Table name.

    Returns:
        bool: True if table has ROWID; False otherwise.
    """
    sql = """
        SELECT sql
        FROM sqlite_master
        WHERE type='table' AND name=?;
    """
    row = conn.execute(sql, (table,)).fetchone()
    if not row or row["sql"] is None:
        return True
    return "WITHOUT ROWID" not in row["sql"].upper()

def fetch_all(conn: sqlite3.Connection, table: str) -> Tuple[List[str], List[sqlite3.Row]]:
    """
    Fetch all rows from a table.

    Args:
        conn: Open SQLite connection.
        table: Table name.

    Returns:
        (columns, rows): Column names and a list of sqlite3.Row.
    """
    cur = conn.execute(f"SELECT * FROM {quote_ident(table)};")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description] if cur.description else []
    return columns, rows

def print_table(columns: List[str], rows: List[sqlite3.Row]) -> None:
    """
    Pretty-print a table with row numbers.

    Args:
        columns: Column names.
        rows: Rows to print.
    """
    if not columns:
        print("\n(No columns)\n")
        return

    # Determine column widths
    values = [[str(r[c]) if r[c] is not None else "NULL" for c in columns] for r in rows]
    widths = [max(len(c), *(len(v[i]) for v in values) if values else [len(c)]) for i, c in enumerate(columns)]
    rownum_w = max(3, len(str(len(rows))))

    # Header
    print()
    print(f"{'#':>{rownum_w}}  " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(columns)))
    print("-" * (rownum_w + 2 + sum(widths) + 3 * (len(columns) - 1)))

    # Rows
    for idx, r in enumerate(rows, start=1):
        line = " | ".join((str(r[c]) if r[c] is not None else "NULL").ljust(widths[i]) for i, c in enumerate(columns))
        print(f"{idx:>{rownum_w}}  {line}")
    print()

def parse_value(user_input: str, decl_type: str) -> Any:
    """
    Convert a user's string input to a Python value based on SQLite declared type.

    Args:
        user_input: Raw input string.
        decl_type: Declared SQLite type (e.g., 'INTEGER', 'REAL', 'TEXT', 'NUMERIC').

    Returns:
        Parsed Python value or None for empty string (use NULL).
    """
    if user_input == "":
        return None

    t = (decl_type or "").upper()
    # Map affinities per SQLite rules (simple approach)
    if "INT" in t:
        try:
            return int(user_input)
        except ValueError:
            pass
    if any(x in t for x in ("REAL", "FLOA", "DOUB")):
        try:
            return float(user_input)
        except ValueError:
            pass
    if "NUM" in t:
        # Try int then float, else leave as string
        try:
            return int(user_input)
        except ValueError:
            try:
                return float(user_input)
            except ValueError:
                return user_input
    # Default TEXT/BLOB: keep as string
    return user_input


def prompt_int(prompt: str, lo: int, hi: int) -> int:
    """
    Prompt for an integer within [lo, hi].

    Args:
        prompt: Prompt text.
        lo: Minimum allowed value.
        hi: Maximum allowed value.

    Returns:
        int within [lo, hi].
    """
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if lo <= val <= hi:
                return val
        except ValueError:
            pass
        print(f"Please enter a number between {lo} and {hi}.")


def prompt_choice(prompt: str, choices: List[str]) -> str:
    """
    Prompt for a single-character choice from a list (case-insensitive).

    Args:
        prompt: Prompt text.
        choices: Allowed choices, e.g., ['I','U','D','Q'].

    Returns:
        Uppercased chosen character.
    """
    choices_upper = [c.upper() for c in choices]
    while True:
        s = input(prompt).strip().upper()
        if s in choices_upper:
            return s
        print(f"Please choose one of: {', '.join(choices_upper)}")

def insert_record(conn: sqlite3.Connection, table: str, schema: List[Dict[str, Any]]) -> None:
    """
    Insert a record into the given table by prompting for each non-auto column.

    Rules:
        - Skip INTEGER PRIMARY KEY (auto-increment rowid alias) when possible.
        - Empty input becomes NULL (or default applies if not null with default).
        - Values are parsed according to declared types.

    Args:
        conn: Open SQLite connection.
        table: Table name.
        schema: Table schema (PRAGMA table_info).
    """
    print("\n-- Insert Row --")
    cols: List[str] = []
    vals: List[Any] = []

    for col in schema:
        name = col["name"]
        decl_type = col["type"]
        is_pk = col["pk"] > 0
        notnull = bool(col["notnull"])
        dflt = col["dflt_value"]

        # Heuristic: if single-column INTEGER PK, let SQLite auto-assign.
        if is_pk and "INT" in (decl_type or "").upper() and primary_key_is_single_int(schema):
            print(f"(Skipping auto PK column '{name}')")
            continue

        prompt = f"{name} ({decl_type or 'TEXT'}"
        if notnull and dflt is None:
            prompt += ", NOT NULL"
        if dflt is not None:
            prompt += f", DEFAULT={dflt}"
        prompt += ") [Enter to use NULL/DEFAULT]: "

        raw = input(prompt)
        val = parse_value(raw, decl_type)

        if val is None and notnull and dflt is None:
            print(f"Column '{name}' is NOT NULL with no default. Please provide a value.")
            # retry once in a small loop
            while True:
                raw = input(f"{name} (required): ").strip()
                if raw != "":
                    val = parse_value(raw, decl_type)
                    break
                print("This field is required.")
        cols.append(name)
        vals.append(val)

    placeholders = ", ".join("?" for _ in cols)
    col_list = ", ".join(quote_ident(c) for c in cols)
    sql = f"INSERT INTO {quote_ident(table)} ({col_list}) VALUES ({placeholders});"

    try:
        conn.execute("BEGIN;")
        conn.execute(sql, vals)
        conn.commit()
        print("Insert successful.\n")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Insert failed: {e}\n")

def update_record(conn: sqlite3.Connection, table: str,
                  columns: List[str], rows: List[sqlite3.Row],
                  schema: List[Dict[str, Any]]) -> None:
    """
    Update one field of a selected row.

    Args:
        conn: Open SQLite connection.
        table: Table name.
        columns: Column names for display and validation.
        rows: Rows from the last fetch, used to select which record to update.
        schema: Table schema to parse types and PKs.
    """
    if not rows:
        print("No rows to update.\n")
        return

    print("-- Update Row --")
    row_idx = prompt_int(f"Select row number to update (1-{len(rows)}): ", 1, len(rows)) - 1
    target_row = rows[row_idx]

    # Choose column to update
    print("Columns:", ", ".join(f"{i+1}:{c}" for i, c in enumerate(columns)))
    col_idx = prompt_int(f"Select column number to update (1-{len(columns)}): ", 1, len(columns)) - 1
    col_name = columns[col_idx]

    # New value
    decl_type = next((c["type"] for c in schema if c["name"] == col_name), "TEXT")
    new_raw = input(f"New value for {col_name} ({decl_type or 'TEXT'}) [Enter for NULL]: ")
    new_val = parse_value(new_raw, decl_type)

    # Build WHERE by primary key; fallback to rowid if needed
    where_sql, where_params = build_row_where(conn, table, schema, target_row)

    sql = f"UPDATE {quote_ident(table)} SET {quote_ident(col_name)} = ? WHERE {where_sql};"
    params = [new_val, *where_params]

    try:
        conn.execute("BEGIN;")
        cur = conn.execute(sql, params)
        if cur.rowcount == 0:
            print("No rows updated (record may have changed).")
            conn.rollback()
        else:
            conn.commit()
            print("Update successful.\n")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Update failed: {e}\n")

def delete_record(conn: sqlite3.Connection, table: str,
                  rows: List[sqlite3.Row], schema: List[Dict[str, Any]]) -> None:
    """
    Delete a selected row.

    Args:
        conn: Open SQLite connection.
        table: Table name.
        rows: Rows from the last fetch, used to select which record to delete.
        schema: Table schema for PK detection.
    """
    if not rows:
        print("No rows to delete.\n")
        return

    print("-- Delete Row --")
    row_idx = prompt_int(f"Select row number to delete (1-{len(rows)}): ", 1, len(rows)) - 1
    target_row = rows[row_idx]

    confirm = prompt_choice(f"Are you sure you want to delete row {row_idx+1}? (Y/N): ", ["Y", "N"])
    if confirm != "Y":
        print("Delete cancelled.\n")
        return

    where_sql, where_params = build_row_where(conn, table, schema, target_row)
    sql = f"DELETE FROM {quote_ident(table)} WHERE {where_sql};"

    try:
        conn.execute("BEGIN;")
        cur = conn.execute(sql, where_params)
        if cur.rowcount == 0:
            print("No rows deleted (record may have changed).")
            conn.rollback()
        else:
            conn.commit()
            print("Delete successful.\n")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Delete failed: {e}\n")

def build_row_where(conn: sqlite3.Connection, table: str,
                    schema: List[Dict[str, Any]],
                    row: sqlite3.Row) -> Tuple[str, List[Any]]:
    """
    Build a WHERE clause and parameter list to uniquely identify a row.

    Preference:
        1) Use primary key columns and their values from 'row'.
        2) If no PK, and table has rowid storage, use 'rowid'.

    Args:
        conn: Open SQLite connection.
        table: Table name.
        schema: Table schema.
        row: The selected row (sqlite3.Row).

    Returns:
        (where_sql, params): WHERE clause (without the word WHERE) and parameters.

    Raises:
        RuntimeError: If the row cannot be uniquely identified.
    """
    pk_cols = get_primary_key_columns(schema)
    if pk_cols:
        where_parts = [f"{quote_ident(c)} = ?" for c in pk_cols]
        params = [row[c] for c in pk_cols]
        return " AND ".join(where_parts), params

    if has_rowid_storage(conn, table):
        # Re-fetch rowid for this row by matching all column values (best-effort)
        columns = [col["name"] for col in schema]
        where_parts = [f"{quote_ident(c)} IS ?" if row[c] is None else f"{quote_ident(c)} = ?" for c in columns]
        params = [row[c] for c in columns]
        sql = f"SELECT rowid FROM {quote_ident(table)} WHERE " + " AND ".join(where_parts) + " LIMIT 1;"
        got = conn.execute(sql, params).fetchone()
        if got is not None:
            return "rowid = ?", [got["rowid"]]

    raise RuntimeError("Unable to build a unique WHERE clause for this row.")

def primary_key_is_single_int(schema: List[Dict[str, Any]]) -> bool:
    """
    Heuristic to see if there's a single INTEGER PRIMARY KEY suitable for auto value.

    Args:
        schema: Table schema list.

    Returns:
        bool
    """
    pks = [c for c in schema if c["pk"] > 0]
    if len(pks) != 1:
        return False
    return "INT" in (pks[0]["type"] or "").upper()

def quote_ident(identifier: str) -> str:
    """
    Safely quote a SQLite identifier (basic).

    Args:
        identifier: Identifier string.

    Returns:
        Quoted identifier suitable for SQL string formatting.
    """
    if not identifier.replace("_", "").replace("-", "").isalnum():
        # fallback quoting for unusual names; double quotes escape by doubling
        return '"' + identifier.replace('"', '""') + '"'
    return f'"{identifier}"'

def choose_table(tables: List[str]) -> Optional[str]:
    """
    Prompt user to choose a table by number.

    Args:
        tables: List of table names.

    Returns:
        Selected table name, or None if the user quits.
    """
    if not tables:
        print("No tables found.")
        return None

    print("\nAvailable tables:")
    for i, t in enumerate(tables, start=1):
        print(f"  {i}. {t}")

    print("  0. Quit")
    choice = prompt_int(f"Select a table (0-{len(tables)}): ", 0, len(tables))
    if choice == 0:
        return None
    return tables[choice - 1]

def main_menu(conn: sqlite3.Connection, table: str) -> None:
    """
    Show the main loop for a selected table: display, then I/U/D/Q choices.

    Args:
        conn: Open SQLite connection.
        table: Table name selected by the user.
    """
    while True:
        schema = get_table_schema(conn, table)
        columns, rows = fetch_all(conn, table)

        print(f"\n=== {table} ({len(rows)} rows) ===")
        print_table(columns, rows)

        action = prompt_choice("Choose (I)nsert, (U)pdate, (D)elete, (S)witch table, or (Q)uit: ",
                               ["I", "U", "D", "S", "Q"])
        if action == "I":
            insert_record(conn, table, schema)
        elif action == "U":
            update_record(conn, table, columns, rows, schema)
        elif action == "D":
            delete_record(conn, table, rows, schema)
        elif action == "S":
            return
        else:
            print("Goodbye!")
            sys.exit(0)

def run(db_path: str) -> None:
    """
    Orchestrate the CLI workflow:
      - Connect
      - List tables (store in a list)
      - Let user choose a table, then enter CRUD loop

    Args:
        db_path: Path to SQLite database file.
    """
    try:
        conn = connect_db(db_path)
    except Exception as e:
        print(f"Could not open database: {e}")
        return

    print("Northwind SQLite Browser — (I)nsert, (U)pdate, (D)elete, (S)witch, (Q)uit")

    try:
        while True:
            tables = list_tables(conn)  # stored in a Python list, as required
            table = choose_table(tables)
            if table is None:
                print("Goodbye!")
                break
            main_menu(conn, table)
    finally:
        conn.close()

if __name__ == "__main__":
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_db = os.path.join(script_dir, "Northwind.db")
    db_path = sys.argv[1] if len(sys.argv) >= 2 else default_db
    run(db_path)