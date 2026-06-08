from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sim.tick import tick
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('world_seed.json', 'r') as file1, open('economy_state.json', 'r') as file2:
    world_state = json.load(file1)
    economy_state = json.load(file2)

@app.get("/")
def root():
    return {"message": "DnD ABM API is running"}


@app.get("/world-state")
def get_world_state():
    return {
        "world": world_state,
        "economy": economy_state
    }

@app.post("/tick")
def run_tick():
    global economy_state
    economy_state = tick()
    return economy_state