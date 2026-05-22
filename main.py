from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import asyncpg

app = FastAPI(title="Видеотека API", description="Справочная система фильмов")

# Разрешаем запросы с любых фронтендов (для курсовой)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель фильма
class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    director: str
    year: int
    genre: str
    rating: float

# Временно храним данные в памяти (пока нет БД)
movies_db = []
counter = 1

@app.get("/")
def root():
    return {"message": "Видеотека API работает!", "docs": "/docs"}

@app.get("/movies", response_model=List[Movie])
def get_movies():
    return movies_db

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies_db:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Фильм не найден")

@app.post("/movies", response_model=Movie)
def add_movie(movie: Movie):
    global counter
    new_movie = movie.dict()
    new_movie["id"] = counter
    counter += 1
    movies_db.append(new_movie)
    return new_movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    global movies_db
    for i, movie in enumerate(movies_db):
        if movie["id"] == movie_id:
            movies_db.pop(i)
            return {"message": "Фильм удален"}
    raise HTTPException(status_code=404, detail="Фильм не найден")
