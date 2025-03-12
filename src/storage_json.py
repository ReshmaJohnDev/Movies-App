from istorage import IStorage
import json

class StorageJson(IStorage):
    def __init__(self, file_path):
        self._file_path = file_path

    def list_movies(self):
        """
            The function loads the information from the JSON
            file and returns the data.

            """
        with open(self._file_path, "r") as file_obj:
            data = json.loads(file_obj.read())
            return data

    def save_movies(self, movies):
        """
        Gets all your movies as an argument and saves them to the JSON file.
        """
        with open(self._file_path, "w") as file_write_obj:
            json_string = json.dumps(movies)
            file_write_obj.write(json_string)

    def add_movie(self, title, year, rating, poster):
        """
            Loads the information from the JSON file, add the movie,
            and saves it.
            """
        movies = self.list_movies()
        movies[title] = {"rating": str(rating), "year": str(year), "poster": poster}
        self.save_movies(movies)

    def delete_movie(self, title):
        """
            Loads the information from the JSON file, deletes the movie,
            and saves it.
            """
        movies = self.list_movies()
        del movies[title]
        self.save_movies(movies)

    def update_movie(self, title, rating):
        """
            Loads the information from the JSON file, updates the movie,
            and saves it.
            """
        movies = self.list_movies()
        movies[title]["rating"] = str(rating)
        self.save_movies(movies)

