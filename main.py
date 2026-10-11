import uvicorn
from fastapi import FastAPI, HTTPException

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


@app.get(
    "/books",
tags=["books"],
summary="Get all books",)
def read_books():
    return books

@app.get(
    "/books/{book_id}",
tags = ["book"],
summary = "Get book by id",
)
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")




if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)