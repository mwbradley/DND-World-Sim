from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('world_seed.json', 'r') as file:
    world_state = json.load(file)

@app.get("/")
def root():
    return {"message": "DnD ABM API is running"}


@app.get("/world-state")
def get_world_state():
    return world_state