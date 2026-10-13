import sqlite3

conn = sqlite3.connect("practice.db")   # creates the file if missing
conn.row_factory = sqlite3.Row          # lets us read columns by name
cur = conn.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    content TEXT NOT NULL,
    pinned  INTEGER NOT NULL DEFAULT 0
)
""")
conn.commit()

# cur.execute(
#     "INSERT INTO notes (title,content) VALUES (?,?)",
#     ("Todo ","learn FASTAPI"),
# )

# cur.execute(
#     "INSERT INTO notes (title,content,pinned) VALUES (?,?,?)",
#     ("idea ","fuck off",1),
# )

# conn.commit()

cur.execute("SELECT COUNT(*) AS total FROM notes")

if cur.fetchone()["total"] == 0:
    sample = [
        ("Todo", "Learn FastAPI", 0),
        ("Idea", "Build a notes project", 1),
        ("Todo list", "Finish SQL basics", 1),
        ("Shopping", "Milk and bread", 0),
        ("Study plan", "Python, SQL, FastAPI", 0),
    ]
    cur.executemany(
        "INSERT INTO notes (title, content, pinned) VALUES (?, ?, ?)", sample
    )

conn.commit()

# cur.execute("SELECT * FROM notes ORDER BY pinned DESC, id DESC LIMIT 5")
# for row in cur.fetchall():
#     print(dict(row))

# cur.execute("SELECT COUNT(*) AS total FROM notes")
# print(cur.fetchone()["total"])



# def get_note(note_id):
#     cur.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
#     row = cur.fetchone()
#     if row is None:
#         return None
#     return dict(row)


# print(get_note(1))
# print(get_note(999))

evil = "x'); DROP TABLE notes; --"
cur.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (evil, "test"))
conn.commit()
print(cur.execute("SELECT title FROM notes ORDER BY id DESC LIMIT 1").fetchone()[0])












