from fastapi import FastAPI
from routers import filmovi

app = FastAPI()

app.include_router(filmovi.router)

@app.get("/")
async def root():
    return "Hello World"