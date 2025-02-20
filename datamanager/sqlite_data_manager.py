from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from MoviWebApp.datamanager.data_manager_interface import DataManagerInterface
from data_models import Base, User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.engine = create_engine(f'sqlite:///data/{db_file_name}')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_all_users(self):
        """
        Returns a list of all users in the database.
        """
        pass

    def get_user_movies(self, user_id):
        """
        Returns a list of all movies of a specific user.
        """
        pass

    def add_user(self, user):
        """
        Adds a new user to the database.
        """
        pass

    def add_movie(self, movie):
        """
        Updates the details of a specific movie in the database.
        """
        pass

    def update_movie(self, movie):
        """
        Deletes a specific movie from the database.
        """
        pass
