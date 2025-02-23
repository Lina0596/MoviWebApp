from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    """
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f'User(id = {self.id}, name = {self.name})'


class Movie(Base):
    """
    """
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    director = Column(String)
    year_of_release = Column(Integer)
    rating = Column(Integer)
    user_id =Column(ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'Movie(id = {self.id}, title = {self.title}, director = {self.director}, year_of_release = {self.year_of_release}, rating = {self.rating}, user_id = {self.user_id})'