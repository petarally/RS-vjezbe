from fastapi import APIRouter, HTTPException, Query
from models.models import Movie, Series
from typing import Optional, Literal
import json

router = APIRouter(prefix="/filmovi", tags=["Filmovi"])

# Učitavanje podataka direktno u routeru
def load_data():
    with open("Film.json", encoding="utf-8") as f:
        data = json.load(f)
    
    movies, series = [], []
    for item in data:
        if not item:
            continue
        if item.get("Type") == "series":
            series.append(Series(**item))
        else:
            movies.append(Movie(**item))
    return movies, series

movies, series = load_data()
all_content = movies + series

# Dohvaćanje svih filmova
@router.get("/")
async def get_all_movies(
    min_year: Optional[int] = Query(None, ge=1900, description="Minimalna godina"),
    max_year: Optional[int] = Query(None, le=2030, description="Maksimalna godina"),
    min_rating: Optional[float] = Query(None, ge=0, le=10, description="Minimalna ocjena"),
    max_rating: Optional[float] = Query(None, ge=0, le=10, description="Maksimalna ocjena"),
    type: Optional[Literal["movie", "series"]] = Query(None, description="Tip: movie ili series")
):
    results = all_content
    
    if type:
        results = [m for m in results if m.Type == type]
    
    if min_year:
        results = [m for m in results if int(m.Year[:4]) >= min_year]
    
    if max_year:
        results = [m for m in results if int(m.Year[:4]) <= max_year]
    
    if min_rating:
        results = [m for m in results if m.imdbRating != "N/A" and float(m.imdbRating) >= min_rating]
    
    if max_rating:
        results = [m for m in results if m.imdbRating != "N/A" and float(m.imdbRating) <= max_rating]

    return results

# Dohvaćanje filmova prema IMDB_ID-u
@router.get("/id/{imdb_id}")
async def get_movie_by_id(imdb_id: str):
    for movie in movies:
        if movie.imdbID == imdb_id:
            return movie
    raise HTTPException(status_code=404, detail="Film nije pronađen")

# Dohvaćanje filmova prema naslovu filma
@router.get("/title/{title}")
async def get_movie_by_title(title: str):
    for movie in movies:
        if movie.Title.lower() == title.lower():
            return movie
    raise HTTPException(status_code=404, detail="Film nije pronađen")