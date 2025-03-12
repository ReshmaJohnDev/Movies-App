from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        """
        Returns a dictionary of dictionaries that
        contains the movies information in the database.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        The abstract function that adds movie to the database
        file and returns the data.
        """

        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        The abstract function that deletes movie from  the database
        file and returns the data.
        """

        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        The abstract function that updates movie in the database
        file and returns the data.
        """
        pass
