import sys
import random
import statistics
import requests
import os
from dotenv import load_dotenv
from fonts_and_colours import BRIGHT_CYAN, BRIGHT_GREEN, RED, RESET
from menu import menus
from storage_json import StorageJson


load_dotenv(dotenv_path='../config/.env')
API_KEY = os.getenv('API_KEY')
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="
FILE_PATH = "../static/index_template.html"


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_menu_display(self):
        """
        This fn displays the menu on the command prompt.
        """
        print(f"\nMenu:{RESET}")
        for option, menu in menus.items():
            print(f"{BRIGHT_CYAN}{option}.{menu}{RESET}")
        print()

    def _commad_exit_program(self):
        """
        This fn exits the program , if the user chooses exit from the menu.
        """
        print("Bye")
        sys.exit()

    def _command_display_movies(self, movies_data):
        """
        Lists all movies with their ratings and release years.
        """
        movies_dic_length = len(movies_data)
        print(f"\n{BRIGHT_GREEN}{movies_dic_length} movies in total{RESET}")
        for movie, details in movies_data.items():
            print(f'{BRIGHT_CYAN}{movie} ({details["year"]}) :'
                  f' {details["rating"]}{RESET}')

    def _command_list_movies(self):
        movies_data = self._storage.list_movies()
        if not movies_data:
            print(f"{RED}No movies to display {RESET}")
            return True
        self._command_display_movies(movies_data)
        return True

    def _command_add_movies(self):
        """
          This fn add new movie when the user choice is "Add movie".
          """
        while True:
            movies_data = self._storage.list_movies()
            add_movie_name = input(f"{BRIGHT_GREEN}Enter new movie name : {RESET}")
            if not add_movie_name:
                print(f"{RED}Movie name must not  be empty{RESET}")
                continue
            try:
                req_url = URL + add_movie_name
                res = requests.get(req_url)
                if res.status_code == 200:
                    movie_data = res.json()
                    if movie_data['Response'] == 'True':  # Check if the movie is found
                        movie_name = movie_data['Title']
                        if movie_name in movies_data:
                            # check if movie name exist
                            print(f"{RED}Movie{RESET} {add_movie_name} {RED}already exist!{RESET}")
                            return True
                        movie_year = movie_data['Year']
                        rating = movie_data['imdbRating']
                        poster = movie_data['Poster']
                        movies_data[add_movie_name] = {"rating": rating, "year": movie_year, "poster": poster}
                        self._storage.add_movie(add_movie_name, movie_year, rating, poster)
                        print(f"{BRIGHT_GREEN}Movie{RESET} {add_movie_name}"
                              f" {BRIGHT_GREEN}successfully added{RESET}")
                        return True
                    else:
                        print(f"{add_movie_name} {movie_data["Error"]}")


            except requests.exceptions.HTTPError as http_err:
                print(f"{RED}HTTP error occurred: {http_err}{RESET}")

            except requests.exceptions.RequestException as req_err:
                print(f"{RED}Error occurred while making the request: {req_err}{RESET}")

            except Exception as err:
                print(f"{RED}An unexpected error occurred: {err}{RESET}")

    def _command_delete_movies(self):
        """
          This fn deletes the movie when the user selects "Delete movie" from the menu.
          """
        movies_data = self._storage.list_movies()
        delete_movie_name = input(f"{BRIGHT_GREEN}Enter movie name to delete: {RESET}")
        if not delete_movie_name:
            print(f"{RED}Movie  doesn't exist!{RESET}")
            return True
        if delete_movie_name not in movies_data:
            print(f"{RED}Movie{RESET} {delete_movie_name} {RED}doesn't exist!!{RESET}")
            return True
        self._storage.delete_movie(delete_movie_name)
        print(f"{BRIGHT_GREEN}Movie{RESET} {delete_movie_name}"
              f" {BRIGHT_GREEN}successfully deleted!{RESET}")
        return True

    def _command_update_movie(self):
        """
          This fn updates the movie when the user selects "Update movie" from the menu.

          """
        movies_data = self._storage.list_movies()
        update_movie_name = input(f"{BRIGHT_GREEN}Enter movie name : {RESET}")
        if not update_movie_name:
            print(f"{RED}Movie  doesn't exist!{RESET}")
            return True
        if update_movie_name not in movies_data:
            print(f"{RED}Movie{RESET} {update_movie_name} {RED}doesn't exist!!{RESET}")
            return True
        while True:
            rating = self.get_valid_input(f"{BRIGHT_GREEN}Enter new movie rating:{RESET}", float,
                                     f"{RED}Please enter a valid rating{RESET}")
            self._storage.update_movie(update_movie_name, rating)
            print(f"{BRIGHT_GREEN}Movie{RESET} {update_movie_name} {BRIGHT_GREEN}"
                  f"successfully updated!{RESET}")
            return True

    def _command_movie_stats(self):
        """
          This fn , provides the average , median , best and worst movies details
          when the user selects "Stats" from the menu .
          """
        movies_data = self._storage.list_movies()
        average_rating = self.movie_status_average(movies_data)
        median = self.movie_status_median(movies_data)
        print(f"{BRIGHT_CYAN}Average Rating :{RESET} {average_rating}"
              f"{BRIGHT_CYAN}\nMedian :{RESET}{median}")
        best_movies, worst_movies = self.best_worst_movie(movies_data)
        print(f"{BRIGHT_CYAN}Best Movie : {RESET}")
        for best_movie in best_movies:
            print(f'{best_movie} - {movies_data[best_movie]["rating"]} ', end=", ")
        print()
        print(f"{BRIGHT_CYAN}Worst Movie : {RESET}")
        for worst_movie in worst_movies:
            print(f'{worst_movie}- {movies_data[worst_movie]["rating"]}', end=", ")
        return True

    def movie_status_average(self, movies_data):
        """
          This fn , calculates the average rating.

          """
        average = sum(float(movie["rating"]) for movie in movies_data.values()) / len(movies_data)
        return round(average, 1)

    def movie_status_median(self, movies_data):
        """
        This fn , calculates the median rating.
        """
        median = statistics.median(float(movie["rating"])for movie in movies_data.values())
        return median

    def best_worst_movie(self, movies_data):
        """
        This fn , determines the best and worst movie.
        """
        best_movie_rating = max(float(movie["rating"]) for movie in movies_data.values())
        worst_movie_rating = min(float(movie["rating"]) for movie in movies_data.values())
        best_movies = [movie_name for movie_name, value in movies_data.items()
                       if float(value["rating"]) == best_movie_rating]
        worst_movies = [movie_name for movie_name, value in movies_data.items()
                        if float(value["rating"]) == worst_movie_rating]
        return best_movies, worst_movies

    def _command_random_movies(self):
        """
        This fn , gives random  movie when the user choice is Random movie.
        """
        movies_data = self._storage.list_movies()
        random_movie_list = random.choice(list(movies_data.items()))
        random_movie = random_movie_list[0]
        random_movie_rating = random_movie_list[1]["rating"]
        print(f"{BRIGHT_GREEN}Your movie for tonight:{RESET} {random_movie} ,"
              f" {BRIGHT_GREEN}it's rated{RESET} {random_movie_rating}")
        return True

    def _command_search_movies(self):
        """
        This fn , list the movies based on the search string , when the user choice is "Search movie".
        """
        movies_data = self._storage.list_movies()
        search_string = input(f"{BRIGHT_GREEN}Enter part of movie name : {RESET}")
        search_results = []
        if not search_string:
            for movie_name, value in movies_data.items():
                print(f'{BRIGHT_CYAN}{movie_name} {RESET}, {value["rating"]}')
            return True
        search_string = search_string.lower()
        for movie in movies_data:
            if search_string in movie.lower():
                search_results.append(movie)
        if len(search_results) != 0:
            for result in search_results:
                print(f"{BRIGHT_CYAN}{result} ,{RESET}", movies_data[result]["rating"])
            return True
        print(f"{RED}No Movie with the word{RESET} - {search_string}")
        return True

    def _command_movies_sorted_by_rating(self):
        """
        This fn sorts movies based on rating,
        """
        movies_data = self._storage.list_movies()
        sorted_movies = sorted(movies_data.items(), key=lambda item: float(item[1]["rating"]), reverse=True)
        for movie, details in sorted_movies:
            movie_name = movie
            movie_rating = details["rating"]
            print(f"{BRIGHT_CYAN}{movie_name} :{RESET} {movie_rating}")
        return True

    def _command_movies_sorted_by_year(self):
        """
        Sorts movies based on their release year.
        - Latest movies first: when the user inputs 'Y'.
        - Oldest movies first: when the user inputs 'N'.
        """
        movies_data = self._storage.list_movies()
        #converting year (str) to int
        for movie, details in movies_data.items():
            details["year"] = int(details["year"])

        while True:
            sort_order = (input(f"{BRIGHT_GREEN}Do you want the latest movies first? (Y/N) {RESET}")
                          .strip().upper())
            if sort_order not in ("Y", "N"):
                print(f'{RED}Please enter "Y" or "N"{RESET}')
                continue
            reverse_order = sort_order == "Y"
            sorted_movies = sorted(movies_data.items(), key=lambda
                item: item[1]["year"], reverse=reverse_order)
            for movie, details in sorted_movies:
                movie_name = movie
                movie_rating = details["rating"]
                movie_year = details["year"]
                print(f"{BRIGHT_CYAN}{movie_name} ({movie_year}):{RESET} {movie_rating}")
            return True

    def get_valid_input(self, prompt, cast_type, error_message):
        """
        This validates the input for ValueError.
        """
        while True:
            try:
                return cast_type(input(prompt))
            except ValueError:
                print(error_message)

    def _load_template_data(self,file_path):
        """
        This fn reads the "index_template.html" file .
        :param file_path:
        :return: file content
        """
        with open(file_path, "r") as handle:
            return handle.read()


    def _generate_website(self,movies_data=None):
        """
        Generate the HTML for the movie grid.
        """
        if not movies_data:
            # If no movies are passed, load them from the storage
            movies_data = self._storage.list_movies()

        movie_grid_html = ""
        for movie_name, details in movies_data.items():
            movie_grid_html += f'''
                    <li>
                        <div class="movie">
                            <img class = "movie-poster" src="{details['poster']}" alt ="{movie_name}" >
                            <div class = "movie_title">{movie_name}</div>
                            <div class = "movie_year">{details['year']}</div>
                        </div>
                    </li>
                    '''

        # Read the HTML template
        template = self._load_template_data(FILE_PATH)
        website_title = "My Movie APP"

        # Replace the placeholders with movie data
        template = template.replace('__TEMPLATE_MOVIE_GRID__', movie_grid_html)
        template = template.replace('__TEMPLATE_TITLE__', website_title)

        # Write the final HTML to a new file (index.html)
        with open('index.html', 'w') as html_file:
            html_file.write(template)

        print("Website generated successfully! Check the 'index.html' file.")
        return True

    def run(self):
        """
        This fn prints the  menu .Get useer command and execute it.
        """
        menu_length = len(menus) - 1
        # nested dictionary , which holds the menu and their corresponding fn to be invoked
        function_names = {"Exit": self._commad_exit_program,
                          "List movies": self._command_list_movies,
                          "Add movie": self._command_add_movies,
                          "Delete movie": self._command_delete_movies,
                          "Update movie": self._command_update_movie,
                          "Stats": self._command_movie_stats,
                          "Random movie": self._command_random_movies,
                          "Search movie": self._command_search_movies,
                          "Movies sorted by rating": self._command_movies_sorted_by_rating,
                          "Movies sorted by year": self._command_movies_sorted_by_year,
                          "Generate website":self._generate_website
                          }
        print(f"{BRIGHT_GREEN}************* My Movies Database ************")
        while True:
            try:
                self._command_menu_display()
                user_choice = int(input(f"{BRIGHT_GREEN}Enter choice (0-{menu_length}): {RESET}"))
                print()
                if 0 <= user_choice <= menu_length:
                    action = menus[user_choice]
                    function_name = function_names[action]
                    should_continue = function_name()
                    if should_continue:
                        input(f"{BRIGHT_GREEN}\n\nPlease enter to continue :{RESET}")

                else:
                    print(f"{RED}Invalid choice{RESET}")
            except ValueError:
                print(f"{RED}Invalid choice{RESET}")

            except Exception as e:
                print(e)