from flask import Flask
from MoviWebApp.datamanager.sqlite_data_manager import SQLiteDataManager


app = Flask(__name__)
data_manager = SQLiteDataManager('moviwebapp.db')


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    pass


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    pass


@app.route('/users/<user_id>')
def add_user(user_id):
    pass


@app.route('/users/<user_id>/add_movie')
def add_movie(user_id):
    pass


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie(user_id, movie_id):
    pass


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(movie_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)