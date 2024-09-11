from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory list of movies
movies = []

# Route to show all movies
@app.route('/')
@app.route('/movies')
def show_movies():
    return render_template('movies.html', movies=movies)

# Route to show the form for adding a new movie
@app.route('/movies/new', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        year = request.form['year']
        
        if not title or not director:
            flash("Title and Director are required!", "error")
            return redirect(url_for('add_movie'))
        
        new_movie = {
            'id': len(movies) + 1,
            'title': title,
            'director': director,
            'year': year
        }
        movies.append(new_movie)
        flash("Movie added successfully!", "success")
        return redirect(url_for('show_movies'))

    return render_template('add_movie.html')

# Route to edit an existing movie
@app.route('/movies/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movie = next((movie for movie in movies if movie['id'] == movie_id), None)
    if movie is None:
        flash("Movie not found!", "error")
        return redirect(url_for('show_movies'))

    if request.method == 'POST':
        movie['title'] = request.form['title']
        movie['director'] = request.form['director']
        movie['year'] = request.form['year']
        flash("Movie updated successfully!", "success")
        return redirect(url_for('show_movies'))

    return render_template('edit_movie.html', movie=movie)

# Route to delete a movie
@app.route('/movies/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    global movies
    movies = [movie for movie in movies if movie['id'] != movie_id]
    flash("Movie deleted successfully!", "success")
    return redirect(url_for('show_movies'))

# Error handling for 404 and 500
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0" , port = 5000)
