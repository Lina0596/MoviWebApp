from flask import Flask, request, url_for, render_template, flash, redirect
from MoviWebApp.datamanager.sqlite_data_manager import SQLiteDataManager
import requests


app = Flask(__name__)
app.secret_key = '0944e3979fa07a3ab609cd515cbcc687'
data_manager = SQLiteDataManager('moviwebapp.db')


def get_movie_from_api(title):
    api_key = '93630ab7'
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
    request_movie = requests.get(url)
    movie = request_movie.json()
    return movie


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


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
        movie = get_movie_from_api(title)
        if movie["Response"] == "True":
            data_manager.add_movie(movie, user_id)
            return redirect(url_for('list_user_movies', user_id=user_id))
        flash('This movie does not exist.', 'error')
        return redirect(url_for('add_movie', user_id=user_id))
    return render_template('add_movie.html')


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    user_movies = data_manager.get_user_movies(user_id)
    movie_to_update = next((movie for movie in user_movies if movie.id == movie_id), None)
    if request.method == 'POST':
        movie_to_update.rating = request.form['rating']
        data_manager.update_movie(movie_to_update)
        return redirect(url_for('list_user_movies', user_id=user_id))
    return render_template('update_movie.html', user_id=user_id, movie=movie_to_update)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)