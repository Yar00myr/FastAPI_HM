import asyncio
from fastapi import FastAPI
from sqlalchemy import select
from pydantic import BaseModel
from uvicorn import Server, Config
from .db import Session, User


app = FastAPI()

config = Config(app=app, host="localhost", port=8080)

from . import db


def main() -> None:
    server = Server(config)
    asyncio.run(server.serve())


if __name__ == "__main__":
    main()


class User_Data(BaseModel):
    login: str
    password: str


@app.get("/users", response_model=list[User_Data])
async def get_users():
    with Session.begin() as session:
        users = session.scalars(select(User)).all()
        return users


@app.post("/create_user")
async def create_user(user: User_Data):
    with Session.begin() as session:
        user = User(**user.model_dump())
        session.add(user)
        return user


@app.put("/user/{user_id}")
async def update_user(user_id: int, user: User_Data):
    with Session.begin() as session:
        current_user = session.scalar(select(User).where(User.id == user_id))
        if user:
            current_user.login = user.login
            current_user.password = user.password

            return current_user


@app.delete("/user/{user_id}")
async def delete_user(user_id: int):
    with Session.begin() as session:
        current_user = session.scalar(select(User).where(User.id == user_id))
        session.delete(current_user)
        return "User deleted successfully"
