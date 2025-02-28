from flask import Flask, request, url_for, render_template, redirect
from MoviWebApp.datamanager.sqlite_data_manager import SQLiteDataManager
import requests


app = Flask(__name__)
try:
    data_manager = SQLiteDataManager('moviwebapp.db')
except IOError as e:
    print("An IOError occurred: ", str(e))


def get_movie_from_api(title):
    """
    Fetches movie details from the OMDB API using the given title.
    :param title: The title of the movie to fetch.
    :return: A dictionary containing movie details.
    """
    api_key = '93630ab7'
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    request_movie = requests.get(url)
    movie = request_movie.json()
    return movie


def validate_data_id(data, data_id):
    """
    Validates if a given data ID exists within a list of data objects.
    :param data: A list of data objects.
    :param data_id: The ID to check for existence.
    :return: True if the ID exists, False otherwise.
    """
    return any(data_object.id == data_id for data_object in data)


@app.route('/')
def home():
    """
    Renders the home page.
    :return: The home.html template.
    """
    return render_template('home.html')


@app.route('/users')
def list_users():
    """
    Gets all users from the database.
    :return: The users.html template populated with user data.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def list_user_movies(user_id):
    """
    Gets all movies associated with a specific user from the database.
    :param user_id: The ID of the user.
    :return: The movies.html template populated with the user's movies.
    """
    users = data_manager.get_all_users()
    if not validate_data_id(users, user_id):
        error = 'User id does not exists.'
        return render_template('404.html', error=error)
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=user_movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Adds a new user to the database with the data from POST request.
    :return: The add_user.html template if there is a GET request,
    redirects to users.html template if the POST request was send successfully.
    """
    if request.method == 'POST':
        new_user = request.form['name']
        if not new_user:
            error = 'Please enter your name.'
            return render_template('add_user.html', error=error)
        data_manager.add_user(new_user)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Adds a new movie to a specific user's movie collection.
    :param user_id: The ID of the user.
    :return: The add_movie.html template if there is a GET request,
    or redirects to movies.html template if the POST request eas send successfully.
    """
    if request.method == 'POST':
        title = request.form['title']
        new_movie = get_movie_from_api(title)
        if new_movie["Response"] == "True":
            user_movies = data_manager.get_user_movies(user_id)
            for movie in user_movies:
                if movie.title == new_movie["Title"]:
                    error = 'This movie already exists in your library.'
                    return render_template('add_movie.html', user_id=user_id, error=error)
            data_manager.add_movie(new_movie, user_id)
            return redirect(url_for('list_user_movies', user_id=user_id))
        else:
            error = 'We can not find the movie.'
            return render_template('add_movie.html', user_id=user_id, error=error)
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Updates the rating of a movie in a user's collection.
    :param user_id: The ID of the user.
    :param movie_id: The ID of the movie to be updated.
    :return: The update_movie.html template if there is a GET request,
    or redirects to movies.html template if the POST request eas send successfully.
    """
    user_movies = data_manager.get_user_movies(user_id)
    movie_to_update = next((movie for movie in user_movies if movie.id == movie_id), None)
    if movie_to_update is None:
        error = 'Movie id does not exists.'
        return render_template('404.html', error=error)
    if request.method == 'POST':
        updated_rating = request.form['rating']
        if not updated_rating or not updated_rating.isdigit() or int(updated_rating) < 1 or int(updated_rating) > 10:
            error = 'Invalid rating! Please enter a number between 1 and 10.'
            return render_template('update_movie.html', user_id=user_id, movie=movie_to_update, error=error)
        else:
            movie_to_update.rating = updated_rating
            data_manager.update_movie(movie_to_update)
            return redirect(url_for('list_user_movies', user_id=user_id))
    return render_template('update_movie.html', user_id=user_id, movie=movie_to_update)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET'])
def delete_movie(user_id, movie_id):
    """
    Deletes a movie from a user's collection.
    :param user_id: The ID of the user.
    :param movie_id: The ID of the movie to be deleted.
    :return: Redirects to the movies.html template.
    """
    data_manager.delete_movie(movie_id)
    return redirect(url_for('list_user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    """
    Handles 404 errors and displays a custom error page.
    :param error: The error object.
    :return: The 404.html template with an error message.
    """
    return render_template('404.html', error=error), 404


if __name__ == '__main__':
    app.run(debug=True)
