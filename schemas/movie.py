from pydantic import BaseModel, Field
from typing import Optional

import datetime

fecha_actual = datetime.datetime.now()
anho_actual = fecha_actual.year

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
