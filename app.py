from flask import Flask, request, url_for, render_template, flash, redirect
from MoviWebApp.datamanager.sqlite_data_manager import SQLiteDataManager


app = Flask(__name__)
data_manager = SQLiteDataManager('moviwebapp.db')


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>', methods=['GET'])
def list_user_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('movies.html', movies=user_movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        new_user = request.form['name']
        data_manager.add_user(new_user)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')

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