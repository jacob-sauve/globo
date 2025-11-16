from fastapi import FastAPI
from pydantic import BaseModel
from search_script import search  # this is the Python script you shared

app = FastAPI()

class SearchRequest(BaseModel):
    prompt: str
    budget: float = None
    origin_airport: str = None

@app.post("/search")
def run_search(data: SearchRequest):
    csv_path = search(
        prompt=data.prompt,
        budget=data.budget,
        origin_airport=data.origin_airport
    )
    return {"csv_path": csv_path}
