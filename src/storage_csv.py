from istorage import IStorage
import csv

class StorageCsv(IStorage):
    def __init__(self, file_path):
        self._file_path = file_path

    def list_movies(self):
        """
        The function loads the movies from the csv
        file and returns the data.
        """
        with open(self._file_path, mode ='r') as file_obj:
            csv_reader = csv.DictReader(file_obj)
            movies_dict = {}
            for row in csv_reader:
                movie_title = row['Movie']  # The column name 'Movie' is now accessible as a key
                rating = float(row['Rating']) # Convert rating to a float
                year = int(row['Year'])  # Convert year to an integer
                poster = row['Poster']

                # Add to the dictionary with the movie title as the key
                movies_dict[movie_title] = {'rating': rating, 'year': year, 'poster':poster}
        return movies_dict

    def save_movies(self, movies):
        """
        Gets all your movies as an argument and saves them to the csv file.
        """
        with open(self._file_path, "w") as file_write_obj:
            field_names = ['Movie', 'Rating', 'Year', 'Poster']

            # Create a DictWriter object, specifying the fieldnames
            writer = csv.DictWriter(file_write_obj, fieldnames = field_names)

            # Write the header (column names) to the CSV file
            writer.writeheader()
            # Loop through the dictionary and write each movie entry as a row
            for movie, details in movies.items():
                row = {'Movie': movie, 'Rating': details['rating'],
                       'Year': details['year'], 'Poster':details['poster']}
                writer.writerow(row)

    def add_movie(self, title, year, rating, poster):
        """
            Loads the information from the csv file, add the movie,
            and saves it.
            """
        movies = self.list_movies()
        movies[title] = {"rating": rating, "year": year, "poster": poster}
        self.save_movies(movies)

    def delete_movie(self, title):
        """
            Loads the information from the csv file, deletes the movie,
            and saves it.
            """
        movies = self.list_movies()
        del movies[title]
        self.save_movies(movies)

    def update_movie(self, title, rating):
        """
            Loads the information from the csv file, updates the movie,
            and saves it.
            """
        movies = self.list_movies()
        movies[title]["rating"] = rating
        self.save_movies(movies)



