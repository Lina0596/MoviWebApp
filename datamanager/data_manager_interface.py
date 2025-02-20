from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """
        Returns a list of all users in the database.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Returns a list of all movies of a specific user.
        """
        pass

    @abstractmethod
    def add_user(self, user):
        """
        Adds a new user to the database.
        """
        pass

    @abstractmethod
    def add_movie(self, movie):
        """
        Updates the details of a specific movie in the database.
        """
        pass

    @abstractmethod
    def update_movie(self, movie):
        """
        Deletes a specific movie from the database.
        """
        pass