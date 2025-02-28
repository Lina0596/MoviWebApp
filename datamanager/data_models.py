from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    """
    Represents a user in the system.
    Attributes:
        id (int): The primary key, auto-incremented.
        name (str): The name of the user, cannot be null.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f'User(id = {self.id}, name = {self.name})'


class Movie(Base):
    """
    Represents a movie in the system.
    Attributes:
        id (int): The primary key, auto-incremented.
        title (str): The title of the movie, cannot be null.
        director (str): The director of the movie, cannot be null.
        year_of_release (int): The release year of the movie, cannot be null.
        rating (int): The rating of the movie.
        user_id (int): Foreign key linking to the user who added the movie, cannot be null.
    """
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    year_of_release = Column(Integer, nullable=False)
    rating = Column(Integer)
    user_id =Column(ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'Movie(id = {self.id}, title = {self.title}, director = {self.director}, year_of_release = {self.year_of_release}, rating = {self.rating}, user_id = {self.user_id})'