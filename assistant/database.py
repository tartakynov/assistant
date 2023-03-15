from contextlib import contextmanager


@contextmanager
def get_cursor(conn):
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


def create_tables(conn):
    with get_cursor(conn) as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY,
                conversation_id INTEGER,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        """)
        conn.commit()


def get_conversation_id(conn, name):
    with get_cursor(conn) as cursor:
        cursor.execute("""
            SELECT id FROM conversations WHERE name = ?
        """, (name,))
        result = cursor.fetchone()
        if result:
            return result[0]
    return None


def create_conversation(conn, name):
    with get_cursor(conn) as cursor:
        cursor.execute("""
            INSERT OR IGNORE INTO conversations (name) VALUES (?)
        """, (name,))
        conn.commit()
    return get_conversation_id(conn, name)


def list_conversations(conn):
    with get_cursor(conn) as cursor:
        cursor.execute("""
            SELECT name FROM conversations
        """)
        return [row[0] for row in cursor.fetchall()]


def remove_conversation(conn, name):
    conversation_id = get_conversation_id(conn, name)
    if not conversation_id:
        return False

    with get_cursor(conn) as cursor:
        cursor.execute("""
            DELETE FROM conversation_history WHERE conversation_id = ?
        """, (conversation_id,))
        cursor.execute("""
            DELETE FROM conversations WHERE id = ?
        """, (conversation_id,))
        conn.commit()
    return True


def insert_message(conn, conversation_id, role, content):
    with get_cursor(conn) as cursor:
        cursor.execute("""
            INSERT INTO conversation_history (conversation_id, role, content)
            VALUES (?, ?, ?)
        """, (conversation_id, role, content))
        conn.commit()


def load_conversation_history(conn, conversation_id):
    with get_cursor(conn) as cursor:
        cursor.execute("""
            SELECT role, content
            FROM conversation_history
            WHERE conversation_id = ?
        """, (conversation_id,))
        history = [{"role": role, "content": content} for role, content in cursor.fetchall()]
        return history
