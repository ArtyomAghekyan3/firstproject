from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped,mapped_column
from fastapi import FastAPI

app = FastAPI()

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
