import json
notes=[]
class Note:
    def __init__(self,id:int,title:str,content:str):
        self.id=id
        self.title=title
        self.content=content
        notes.append(self)
        save_to_file()

    def to_dict(self):
        return{
            "id":self.id,
            "title":self.title,
            "content":self.content
        }

    

def add_note(title:str,content:str):
        id=0
        for n in notes:
            id=max(id,n[0])

        note=Note(id,title,content)
        save_to_file()
        return note

        
        

def get_note(id):
    for n in notes:
        if n.id==id:
            return n
    return None

def del_note(id):
    note=get_note(id)
    if note is None:
         return False
    
    notes.remove(note)
    save_to_file()
    return True

def list_notes():
    return notes


def save_to_file():
    with open("notes.json","w") as f:
        json.dump([note.to_dict() for note in notes],f,indent=2)

def load_from_file():
    try:
        with open("notes.json") as f:
            data=json.load(f)

        for i in data:
            Note(i["id"],i["title"],i["content"])

    except FileNotFoundError:
        pass

load_from_file()

if __name__ == "__main__":
    
    note = add_note("Todo", "Learn Python and FastAPI")

    print("Added:", note.to_dict())
    print("All notes:", [n.to_dict() for n in list_notes()])

    found = get_note(note.id)
    if found:
        print("Found:", found.content)







    



    
        

    
        


    

    
        