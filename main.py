from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Хранилище фильмов (в памяти)
movies = []
next_id = 1

@app.route('/')
def root():
    return {"message": "Видеотека API работает!", "endpoints": ["GET /movies", "POST /movies", "DELETE /movies/<id>"]}

@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

@app.route('/movies', methods=['POST'])
def add_movie():
    global next_id
    data = request.json
    
    movie = {
        "id": next_id,
        "title": data.get('title'),
        "director": data.get('director'),
        "year": data.get('year'),
        "genre": data.get('genre'),
        "rating": data.get('rating')
    }
    movies.append(movie)
    next_id += 1
    return jsonify(movie), 201

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    global movies
    movies = [m for m in movies if m['id'] != movie_id]
    return jsonify({"message": "Фильм удален"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
