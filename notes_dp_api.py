import sqlite3

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from zoneinfo import ZoneInfo

app = FastAPI()
DB_FILE = "notes.db"


class NoteCreate(BaseModel):
    title: str = Field(min_length=1)
    content: str
    pinned: bool = False


class Note(BaseModel):
    id: int
    title: str
    content: str
    pinned: bool
    created_at: str


def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            title   TEXT NOT NULL,
            content TEXT NOT NULL,
            pinned  INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.get("/notes")
def list_notes(pinned : bool | None = None ,db: sqlite3.Connection = Depends(get_db)) -> list[Note]:
    rows=[]
    if pinned is None:
        rows = db.execute("SELECT * FROM notes ORDER BY pinned DESC, id DESC").fetchall()
    else:
        rows = db.execute("SELECT * FROM notes WHERE pinned = ? ORDER BY id DESC",
        (int(pinned),)).fetchall()

    return [dict(r) for r in rows]

@app.get("/notes/count")
def notes_count(db: sqlite3.Connection = Depends(get_db))->int:
    cnt=db.execute("SELECT COUNT(*) as total FROM notes").fetchone()
    return cnt["total"]

@app.get("/notes/search")
def search_notes(q: str, db: sqlite3.Connection = Depends(get_db)) -> list[Note]:
    rows = db.execute(
        "SELECT * FROM notes WHERE title LIKE ? ORDER BY id DESC", (f"%{q}%",)
    ).fetchall()
    return [dict(r) for r in rows]


@app.post("/notes", status_code=201)
def create_note(data: NoteCreate, db: sqlite3.Connection = Depends(get_db)) -> Note:
    cur = db.execute(
        "INSERT INTO notes (title, content, pinned) VALUES (?, ?, ?)",
        (data.title, data.content, int(data.pinned)),
    )
    db.commit()
    row = db.execute("SELECT * FROM notes WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)

@app.get("/notes/{note_id}")
def get_note(note_id: int, db: sqlite3.Connection = Depends(get_db)) -> Note:
    row = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return dict(row)


@app.put("/notes/{note_id}")
def update_note(note_id: int, data: NoteCreate, db: sqlite3.Connection = Depends(get_db)) -> Note:
    cur = db.execute(
        "UPDATE notes SET title = ?, content = ?, pinned = ? WHERE id = ?",
        (data.title, data.content, int(data.pinned), note_id),
    )
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    row = db.execute("SELECT * FROM notes WHERE id = ?",(note_id,)).fetchone()
    return dict(row)

@app.patch("/notes/{note_id}/pin")
def flip_note(note_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute(
        "UPDATE notes SET  pinned = 1-pinned WHERE id = ?",
        (note_id,),
    )
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    row = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    return dict(row)
    
    

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: sqlite3.Connection = Depends(get_db)):
    cur = db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")