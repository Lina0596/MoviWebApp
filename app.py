from flask import Flask, request, url_for, render_template, flash, redirect
from MoviWebApp.datamanager.sqlite_data_manager import SQLiteDataManager
import requests


app = Flask(__name__)
data_manager = SQLiteDataManager('moviwebapp.db')


def get_movie_from_api(title):
    api_key = '93630ab7'
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    request_movie = requests.get(url)
    movie = request_movie.json()
    return movie


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def list_user_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=user_movies, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user = request.form['name']
        data_manager.add_user(new_user)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form['title']
        new_movie = get_movie_from_api(title)
        if new_movie["Response"] == "True":
            user_movies = data_manager.get_user_movies(user_id)
            for movie in user_movies:
                if movie.title == new_movie["Title"]:
                    message = "This movie already exists in your library."
                    return render_template('add_movie.html', message=message)
            data_manager.add_movie(new_movie, user_id)
            return redirect(url_for('list_user_movies', user_id=user_id))
        else:
            error = "We can not find the movie. Please try again."
            return render_template('add_movie.html', error=error)
    return render_template('add_movie.html')


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user_movies = data_manager.get_user_movies(user_id)
    movie_to_update = next((movie for movie in user_movies if movie.id == movie_id), None)
    if request.method == 'POST':
        updated_rating = request.form['rating']
        if not updated_rating or not updated_rating.isdigit() or int(updated_rating) < 1 or int(updated_rating) > 10:
            error = "Invalid rating! Please enter a number between 1 and 10."
            return render_template('update_movie.html', user_id=user_id, movie=movie_to_update, error=error)
        else:
            movie_to_update.rating = updated_rating
            data_manager.update_movie(movie_to_update)
            return redirect(url_for('list_user_movies', user_id=user_id))
    return render_template('update_movie.html', user_id=user_id, movie=movie_to_update)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('list_user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)


"""
TO DO:
- handle users and movies that does not exist
- Error handling pages
- Link back
- add docstrings
- add css style
(- add cover url)
(- check if users are in the database in add_user)
(- ask delete message in delete_movie)
"""