from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __repr__(self):
        return f'User(id = {self.id}, name = {self.name})'


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    director = Column(String)
    year_of_release = Column(Integer)