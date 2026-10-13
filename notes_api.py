from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import Field


app= FastAPI()


class NoteCreate(BaseModel):
    title:str=Field(min_length=1)
    content:str
    pinned: bool=False


class Note(BaseModel):
    id:int
    title:str
    content:str
    pinned: bool=False
        



notes: list[Note]=[]

def next_id()->int:
    return max((n.id for n in notes),default=0)+1

@app.get("/notes")
def list_notes()->list[Note]:
    return notes

@app.post("/notes",status_code=201)
def create_note(data:NoteCreate)->Note:
    note=Note(id=next_id(),title=data.title,content=data.content)
    notes.append(note)
    return note

@app.get("/notes/search")
def get_notes(q: str) -> list[Note]:
    matching_notes: list[Note] = []

    for n in notes:
        if q.lower() in n.title.lower():
            matching_notes.append(n)

    return matching_notes



@app.get("/notes/{note_id}")
def get_note(note_id:int)->Note:
    for n in notes:
        if n.id==note_id:
            return n

    raise HTTPException(status_code=404, detail="Note not found")


@app.put("/notes/{note_id}")
def update_note(note_id: int, data: NoteCreate) -> Note:
    for n in notes:
        if n.id == note_id:
            n.title = data.title
            n.content = data.content
            return n
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    for n in notes:
        if n.id == note_id:
            notes.remove(n)
            return
    raise HTTPException(status_code=404, detail="Note not found")





