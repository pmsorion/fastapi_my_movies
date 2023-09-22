from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field

from starlette.requests import Request
from jwt_manager import create_token, validate_token

from typing import Optional, List
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer



import datetime

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.3"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)

fecha_actual = datetime.datetime.now()
anho_actual = fecha_actual.year

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=150)
    overview: str = Field(min_length=15, max_length=100)
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
        'overview': "En un exuberante planeta llamado Pandora viven los Navi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 2,
        'title': 'Avatar II',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, Lo mismo que la uno pero en el agua",
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
    if user.email == "admin@gmail.com" and user.password == "admin123":
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=20)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Se registro la pelicula"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message": "The movie data has been modified"})

@app.delete('/movies/{id}',  tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int= Path(ge=1, le=2000)) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "The movie has been removed"})