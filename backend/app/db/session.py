import sqlite3

from app.config import SQLITE_DB_PATH, SQLITE_DIR


def get_connection() -> sqlite3.Connection:
    SQLITE_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(SQLITE_DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                status TEXT NOT NULL,
                upload_time TEXT NOT NULL,
                parsed_text_path TEXT,
                error_message TEXT
            );

            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                chunk_text TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                metadata_json TEXT NOT NULL,
                FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE CASCADE
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_chunks_document_index
            ON chunks(document_id, chunk_index);

            CREATE TABLE IF NOT EXISTS workorders (
                work_order_id TEXT PRIMARY KEY,
                equipment_type TEXT,
                fault_symptom TEXT NOT NULL,
                fault_understanding TEXT NOT NULL,
                possible_causes_json TEXT NOT NULL,
                repair_steps_json TEXT NOT NULL,
                safety_notes_json TEXT NOT NULL,
                safety_actions_json TEXT NOT NULL DEFAULT '[]',
                sources_json TEXT NOT NULL,
                operator_note TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(documents)").fetchall()
        }
        if "error_message" not in columns:
            connection.execute("ALTER TABLE documents ADD COLUMN error_message TEXT")
        workorder_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(workorders)").fetchall()
        }
        if "safety_actions_json" not in workorder_columns:
            connection.execute("ALTER TABLE workorders ADD COLUMN safety_actions_json TEXT NOT NULL DEFAULT '[]'")
