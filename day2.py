import json

# Dictionary

user= {"name":"Nitin","age":22,"skills":["c++","python"]}

print(user["name"])

print(user.get("phone"))

user["email"]="n@gmail.com"

print(user["skills"][1])


# List
user= [
    {"name":"nitin","age":22},
    {"name":"harsh","age":23},
    {"name":"riya","age":26}
]

for u in user:
    print(u["name"],u["age"])

# function

def find_user(users:list,name:str):
    for u in users:
        if(u["name"])==name:
            return u["age"]

    return None

def add(a:int,b:int=0):
    return a+b


print(find_user(user,"riya"))
print(add(5),add(5,9))

# Comprehensive way of creating dict and lists

names=[u["name"] for u in user]
adults=[u["name"] for u in user if u["age"]>=23]
mpp={u["name"] : u["age"] for u in user}

print(names)
print(adults)
print(mpp)


# classes and oop

class Note:
    def __init__(self,title:str,cont:str):
        self.title=title
        self.cont=cont


    def summ(self)->str:
        return self.cont[:20]


n= Note("me","my name is nitin singh i am an iit grad form  ee")

print(n.title,"->",n.summ())



# JSON

data = {"name": "Nitin", "skills": ["python", "sql"]}

text=json.dumps(data)
print(text)
back=json.loads(text)
print(back)

with open("data.json","w") as f:
    json.dump(data,f,indent=2)

with open("data.json","r") as f:
    texted=json.load(f)

print(texted)

# Error Handling

try:
    with open("missing.json")as f:
        data=json.load(f)
except FileNotFoundError:
    print("file not found")
    data={}
except json.JSONDecodeError:
    print("file not valid.json")
    data={}

print(data)


from datetime import datetime
print(datetime.now())
