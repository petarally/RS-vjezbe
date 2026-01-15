from pydantic import BaseModel, field_validator
from typing import Optional, Literal

class Actor(BaseModel):
    name: str
    surname: str

class Writer(Actor):
    pass

class Movie(BaseModel):
    # Obavezni atributi
    Title: str 
    Year: str
    Rated: str
    Runtime: str
    Genre: str
    Language: str
    Country: str
    Actors: str
    Plot: str
    Writer: str
    
    # Neobavezni atributi sa zadanim vrijednostima
    ComingSoon: Optional[bool] = False
    Director: Optional[str] = "N/A"
    Awards: Optional[str] = "N/A"
    Poster: Optional[str] = "N/A"
    Metascore: Optional[str] = "N/A"
    imdbRating: Optional[str] = "N/A"
    imdbVotes: Optional[str] = "N/A"
    imdbID: Optional[str] = "N/A"
    Released: Optional[str] = "N/A"
    Response: Optional[str] = "True"
    Images: list[str] = []
    
    # Type mora biti "movie" ili "series"
    Type: Literal["movie", "series"] = "movie"
    
    @field_validator("Year")
    @classmethod
    def validate_year(cls, v: str) -> str:
        # Izvlači godinu iz formata "2016" ili "2016–"
        year_str = v.replace("–", "").replace("-", "")[:4]
        if year_str.isdigit():
            year = int(year_str)
            if year <= 1900:
                raise ValueError("Godina mora biti veća od 1900")
        return v
    
    @field_validator("Runtime")
    @classmethod
    def validate_runtime(cls, v: str) -> str:
        if v == "N/A":
            return v
        # Izvlači broj iz formata "120 min"
        runtime_str = v.split()[0]
        if runtime_str.isdigit():
            runtime = int(runtime_str)
            if runtime <= 0:
                raise ValueError("Trajanje filma mora biti veće od 0")
        return v
    
    @field_validator("imdbRating")
    @classmethod
    def validate_rating(cls, v: str) -> str:
        if v == "N/A":
            return v
        try:
            rating = float(v)
            if rating < 0 or rating > 10:
                raise ValueError("Ocjena mora biti između 0 i 10")
        except ValueError:
            pass
        return v
    
    @field_validator("imdbVotes")
    @classmethod
    def validate_votes(cls, v: str) -> str:
        if v == "N/A":
            return v
        # Uklanja zareze iz broja (npr. "1,234,567" -> "1234567")
        votes_str = v.replace(",", "")
        if votes_str.isdigit():
            votes = int(votes_str)
            if votes <= 0:
                raise ValueError("Broj glasova mora biti veći od 0")
        return v
    
    @field_validator("Images")
    @classmethod
    def validate_images(cls, v: list[str]) -> list[str]:
        for url in v:
            if not url.startswith(("http://", "https://")):
                raise ValueError(f"Nevažeća URL adresa slike: {url}")
        return v


class Series(Movie):
    totalSeasons: Optional[str] = "1"
    Type: Literal["series"] = "series"