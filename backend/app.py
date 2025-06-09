import csv
from pathlib import Path
from typing import List, Dict
from fastapi import FastAPI

app = FastAPI()

def load_names() -> List[Dict[str, str]]:
    """Load names from CSV file"""
    csv_path = Path(__file__).parent / "data" / "names.csv"
    names = []
    
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            names.append(row)
    
    return names

@app.get("/")
async def hello_world():
    return {"message": "Hello World!"}

@app.get("/names")
async def get_names():
    """Get all names from the CSV"""
    names = load_names()
    return {"names": names} 