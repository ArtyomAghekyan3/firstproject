import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import testpytdentic
from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column
app= FastAPI()

books = [{
    "title": "Book 1",
    "author": "Artyom Aghekyan",
    "id": 1,
    },
    {
        "title": "Book 2",
        "author": "Nare Bdoyants",
        "id": 2,
    }
]

users=[]

class CreateBook(BaseModel):
    title: str
    author: str


@app.post("/users",tags=["Users"],summary="Create users")
def create_user(user: testpytdentic.UserSchema):
    users.append(user)
    return {'msg': 'successful'}


@app.get("/users",tags=["Users"],summary="Get users")
def get_users():
    return users



@app.post("/books",tags=["books"],summary="Create new book")
def create_books(book: CreateBook):
    books.append({"title": book.title,
                  "author": book.author,
                  "id": len(books) + 1
                  })


@app.get(
    "/books",
    tags=["books"],
    summary="Get all books", )
def read_books():
    return books


@app.get(
    "/books/{book_id}",
    tags=["books"],
    summary="Get book by id",
)
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")

class AuthorSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    age:str
    sex:bool


authors=[]
@app.get("/authors",tags=["authors"],summary="Get authors")
def get_authors():
    return authors

@app.post('/authors',tags=["authors"],summary="Create new author")
def create_author(author: AuthorSchema):
    authors.append(author)
    return {'msg': 'successful'}




engine = create_async_engine('sqlite+aiosqlite:///db.sqlite')

new_session = async_sessionmaker(bind=engine,expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session



class Base(DeclarativeBase):
    pass

class Books(Base):
    __tablename__ = 'books'

    id: Mapped [int]=mapped_column(primary_key=True)
    title: Mapped[str]
    author:Mapped[str]

@app.post('/setup',tags=["dbbb"])
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
list_for_login=[]
class LogSchema(BaseModel):
    name: str
    age: int = Field(gt=0)
    g : str | None
@app.get('/logg')
def get_logg()-> list:
    return list_for_login


@app.post('/logg')
def get_logg(a:LogSchema)-> dict:
    list_for_login.append({a.name: 'name', a.age: 'age', a.g: 'доп. инфо' })
    return {'msg': 'successful'}


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
