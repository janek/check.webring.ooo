import csv
import random
from pathlib import Path

from fastapi import FastAPI, Query

app = FastAPI()


def load_names() -> list[dict[str, str]]:
    """Load names from CSV file"""
    csv_path = Path(__file__).parent / "names.csv"
    names = []

    with open(csv_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            names.append(row)

    return names


@app.get("/")
async def hello_world():
    return {"message": "Hello World!"}


@app.get("/names")
async def get_names(
    count: int | None = Query(None, description="Number of random names to return"),
):
    """Get names from the CSV, optionally limited to a random sample"""
    names = load_names()

    if count is not None:
        # Return random sample if count specified
        sample_size = min(count, len(names))
        names = random.sample(names, sample_size)

    return {"names": names, "total": len(names)}
