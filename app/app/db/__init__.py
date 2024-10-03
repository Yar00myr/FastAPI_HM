from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///my_db.db", echo=True)
Session = sessionmaker(engine)
LocalSession = scoped_session(engine)


from .models import Base, User
