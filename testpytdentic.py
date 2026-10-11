from pydantic import BaseModel,Field,EmailStr
from fastapi import FastAPI

data={
    'name':'Artyom',
    'author':'batya',
    'age':10,
    'email':'Abo@mail.ru'
}

def age_adder(info: dict):
    info['age']+=1
    return info

class UserSchema(BaseModel):
    name: str  | None
    age: int | None
    author: str | None
    email:str | None

"""a=UserSchema(**data)
print(a)
"""
