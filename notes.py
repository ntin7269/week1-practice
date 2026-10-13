import json
notes=[]
class Note:
    def __init__(self,id:int,title:str,content:str):
        self.id=id
        self.title=title
        self.content=content
                                                

    def to_dict(self):
        return{
            "id":self.id,
            "title":self.title,
            "content":self.content
        }

    

def add_note(title:str,content:str):
        id=0
        for n in notes:
            id=max(id,n.id)
        id=id+1

        note=Note(id,title,content)
        notes.append(note)
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
            notes.append(Note(i["id"],i["title"],i["content"]))

    except FileNotFoundError:
        pass

load_from_file()

if __name__ == "__main__":
    
    print(del_note(2))     # True
    print(del_note(99))    # False
    print([n.id for n in list_notes()])   # [1, 3]






    



    
        

    
        


    

    
        