from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

movies = []
next_id = 1

@app.route('/')
def home():
    return {"message": "Видеотека API работает!"}

@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

@app.route('/movies', methods=['POST'])
def add_movie():
    global next_id
    data = request.get_json()
    
    # genres приходит как массив, сохраняем как строку через запятую
    genres_list = data.get('genres', [])
    genres_str = ', '.join(genres_list) if genres_list else ''
    
    movie = {
        "id": next_id,
        "title": data.get('title'),
        "director": data.get('director'),
        "year": data.get('year'),
        "genres": genres_str,  # сохраняем как "Боевик, Драма"
        "rating": data.get('rating'),
        "description": data.get('description', ''),
        "poster": data.get('poster', '')
    }
    movies.append(movie)
    next_id += 1
    return jsonify(movie)

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    global movies
    movies = [m for m in movies if m['id'] != movie_id]
    return jsonify({"message": "deleted"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
