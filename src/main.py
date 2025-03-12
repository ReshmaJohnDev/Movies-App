from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

def main ():
    """
    This fn is runs the app
    In the main function, it creates an StorageJson object or StorageCsv object.
    Then it create a MovieApp object, with the StorageJson object . MovieApp object runs the app.
    """

    # storage = StorageJson('../data/data.json')
    # movie_app = MovieApp(storage)
    # movie_app.run()

    storage = StorageCsv('../data/data.csv')
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()

