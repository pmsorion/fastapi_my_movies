from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token
import datetime

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

fecha_actual = datetime.datetime.now()
anho_actual = fecha_actual.year

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=anho_actual)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=20)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": anho_actual,
                    "rating": 9.9,
                    "category": "Acción"
                }
            ]
        }
    }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 2,
        'title': 'Avatar II',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2022',
        'rating': 7.8,
        'category': 'Acción'
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "pmsorgion@gmail.com" and user.password == "admin123":
        create_token(user.dict())
    return user


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item["id"] == id:
            return JSONResponse(status_code=200, content=item)
    return JSONResponse(status_code=404, content=[])


@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)) -> List[Movie]:
    data = [ item for item in movies if item['category'] == category]
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Se registro la pelicula"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(status_code=200, content={"message": "Se ha modificado la pelicula"})

@app.delete('/movies/{id}',  tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int= Path(ge=1, le=2000)) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la pelicula"})