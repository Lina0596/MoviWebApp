from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from MoviWebApp.datamanager.data_manager_interface import DataManagerInterface
from MoviWebApp.datamanager.data_models import Base, User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///data/{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_all_users(self):
        """
        Returns a list of all users in the database.
        """
        with self.Session() as session:
            return session.query(User).all()

    def get_user_movies(self, user_id):
        """
        Returns a list of all movies of a specific user.
        """
        with self.Session() as session:
            user_movies = session.query(Movie).filter(Movie.user_id == user_id).all()
            return user_movies

    def add_user(self, user):
        """
        Adds a new user to the database.
        """
        with self.Session() as session:
            new_user = User(
                name=user
            )
            session.add(new_user)
            session.commit()

    def add_movie(self, movie):
        """
        Adds a new movie to the database.
        """
        with self.Session() as session:
            new_movie = Movie(
                title=movie['Title'],
                director=movie['Director'],
                year_of_release=movie['Year'],
                rating=movie['imdbRating'],
                user_id=1
            )
            session.add(new_movie)
            session.commit()

    def update_movie(self, movie):
        """
        Updates the details of a specific movie in the database.
        """
        with self.Session() as session:
            movie_to_update = session.query(Movie).filter(Movie.id == movie.id).first()
            movie_to_update.title = movie.title
            movie_to_update.director = movie.director
            movie_to_update.year_of_release = movie.year_of_release
            movie_to_update.rating = movie.rating
            session.commit()

    def delete_movie(self, movie_id):
        """
        Deletes a specific movie from the database.
        """
        with self.Session() as session:
            movie_to_delete = session.query(Movie).filter(Movie.id == movie_id).first()
            session.delete(movie_to_delete)
            session.commit()
