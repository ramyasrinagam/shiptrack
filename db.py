import sqlite3

def get_db():
    conn = sqlite3.connect("shiptrack.db")
    conn.row_factory = sqlite3.Row
    return conn

def add_shipment(s, conn=None):
    own = conn is None
    if own:
        conn = get_db()
    conn.execute(
        "INSERT INTO shipments (tracking_id, recipient, origin, destination, carrier, status, estimated_delivery, updated) VALUES (?,?,?,?,?,?,?,?)",
        (s["tracking_id"], s["recipient"], s["origin"], s["destination"],
         s["carrier"], s["status"], s["estimated_delivery"], s["updated"]))
    if own:
        conn.commit()
        conn.close()

def init_db(seed):
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS shipments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_id TEXT UNIQUE NOT NULL,
        recipient TEXT, origin TEXT, destination TEXT,
        carrier TEXT, status TEXT,
        estimated_delivery TEXT, updated TEXT
    )
    """)
    count = conn.execute("SELECT COUNT(*) FROM shipments").fetchone()[0]
    if count == 0:
        for s in reversed(seed):
            add_shipment(s, conn)
    conn.commit()
    conn.close()

def get_shipments():
    conn = get_db()
    rows = conn.execute("SELECT * FROM shipments ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_status(tracking_id, status):
    conn = get_db()
    conn.execute(
        "UPDATE shipments SET status = ?, updated = 'just now' WHERE tracking_id = ?",
        (status, tracking_id))
    conn.commit()
    conn.close()