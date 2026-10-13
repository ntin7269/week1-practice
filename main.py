from fastapi import FastAPI
from datetime import datetime

app=FastAPI()


@app.get("/")
def home():
    return {"msg":"hello backend"}

@app.get("/about")
def about():
    return {"name":"my first api","version":1}

@app.get("/hello/{name}")
def hello(name:str):
    return {"message":f"hello {name}!"}

@app.get("/add")
def add(a:int,b:int=0):
    return {"result":a+b}

@app.get("/health")
def health():
    return {"health":"OK"}
def get_time():
    return {"time":datetime.now().isoformat()}

@app.get("/square/{n}")
def square(n:int):
    return {"n":n,"square":n*n}



