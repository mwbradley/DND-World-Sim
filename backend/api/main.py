from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sim.tick import tick
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("matesia.db", check_same_thread=False)
conn.row_factory = sqlite3.Row  # lets you access columns by name like a dict
cursor = conn.cursor()

@app.get("/")
def root():
    return {"message": "DnD ABM API is running"}


@app.get("/world-state")
def get_world_state():
    cursor.execute("SELECT * FROM settlements")
    settlements = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM routes")
    routes = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM cultures")
    cultures = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM states")
    states = [dict(row) for row in cursor.fetchall()]

    cursor.execute("""
        SELECT e.settlement_id, e.item_id, i.name, e.stock, e.price 
        FROM economy e
            INNER JOIN settlements s on s.id = e.settlement_id
            INNER JOIN items i on i.id = e.item_id
        """)
    economy = [dict(row) for row in cursor.fetchall()]

    return {
        "world": {
            "settlements": settlements,
            "routes": routes,
            "cultures": cultures,
            "states": states
        },
        "economy": economy
    }

@app.post("/tick")
def run_tick():
    tick()
    return {"status": "ok"}