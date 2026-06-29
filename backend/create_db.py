import sqlite3
import json

conn = sqlite3.connect("matesia.db")
cursor = conn.cursor()

# ── Create Tables ──────────────────────────────────────────────

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS settlements (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        x REAL,
        y REAL,
        population INTEGER,
        state_id INTEGER,
        culture_id INTEGER,
        tier TEXT,
        biome_name TEXT,
        is_capital INTEGER,
        is_port INTEGER,
        has_market INTEGER,
        has_walls INTEGER,
        has_citadel INTEGER
    );

    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id INTEGER,
        to_id INTEGER,
        type TEXT,
        FOREIGN KEY (from_id) REFERENCES settlements(id),
        FOREIGN KEY (to_id) REFERENCES settlements(id)
    );

    CREATE TABLE IF NOT EXISTS cultures (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS states (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        base_price INTEGER,
        rarity TEXT,
        weight INTEGER,
        production_rate INTEGER
    );

    CREATE TABLE IF NOT EXISTS item_biomes (
        item_id INTEGER,
        biome_name TEXT,
        FOREIGN KEY (item_id) REFERENCES items(id)
    );

    CREATE TABLE IF NOT EXISTS economy (
        settlement_id INTEGER,
        item_id INTEGER,
        stock INTEGER,
        price INTEGER,
        PRIMARY KEY (settlement_id, item_id),
        FOREIGN KEY (settlement_id) REFERENCES settlements(id),
        FOREIGN KEY (item_id) REFERENCES items(id)
    );

    CREATE TABLE IF NOT EXISTS merchants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        tier TEXT,
        x REAL,
        y REAL,
        current_settlement_id INTEGER,
        destination_id INTEGER,
        gold INTEGER,
        FOREIGN KEY (current_settlement_id) REFERENCES settlements(id),
        FOREIGN KEY (destination_id) REFERENCES settlements(id)
    );

    CREATE TABLE IF NOT EXISTS merchant_inventory (
        merchant_id INTEGER,
        item_id INTEGER,
        quantity INTEGER,
        PRIMARY KEY (merchant_id, item_id),
        FOREIGN KEY (merchant_id) REFERENCES merchants(id),
        FOREIGN KEY (item_id) REFERENCES items(id)
    );
""")

# ── Load JSON files ────────────────────────────────────────────

with open("world_seed.json", "r", encoding="utf-8") as f:
    world = json.load(f)

with open("economy_state.json", "r", encoding="utf-8") as f:
    economy = json.load(f)

with open("items.json", "r", encoding="utf-8") as f:
    items_data = json.load(f)

# ── Populate settlements ───────────────────────────────────────

for s in world["settlements"]:
    cursor.execute("""
        INSERT OR REPLACE INTO settlements 
        (id, name, x, y, population, state_id, culture_id, tier, biome_name,
         is_capital, is_port, has_market, has_walls, has_citadel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        s["id"], s["name"], s["x"], s["y"], s["population"],
        s["state"], s["culture"], s["tier"], s["biome_name"],
        s.get("is_capital", 0), s.get("is_port", 0),
        s.get("has_market", 0), s.get("has_walls", 0),
        s.get("has_citadel", 0)
    ))

# ── Populate routes ────────────────────────────────────────────

for r in world["routes"]:
    cursor.execute("""
        INSERT INTO routes (from_id, to_id, type)
        VALUES (?, ?, ?)
    """, (r["from_id"], r["to_id"], r["type"]))

# ── Populate cultures ──────────────────────────────────────────

for c in world["cultures"]:
    cursor.execute("""
        INSERT OR REPLACE INTO cultures (id, name)
        VALUES (?, ?)
    """, (c["id"], c["name"]))

# ── Populate states ────────────────────────────────────────────

for s in world["states"]:
    cursor.execute("""
        INSERT OR REPLACE INTO states (id, name)
        VALUES (?, ?)
    """, (s["id"], s["name"]))

# ── Populate items and item_biomes ─────────────────────────────

for i in items_data["items"]:
    cursor.execute("""
        INSERT OR REPLACE INTO items 
        (id, name, category, base_price, rarity, weight, production_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        i["id"], i["name"], i["category"], i["base_price"],
        i["rarity"], i["weight"], i["production_rate"]
    ))
    for biome in i["produced_by"]:
        cursor.execute("""
            INSERT INTO item_biomes (item_id, biome_name)
            VALUES (?, ?)
        """, (i["id"], biome))

# ── Populate economy ───────────────────────────────────────────

for s in economy:
    for item_id, item_data in s["inventory"].items():
        cursor.execute("""
            INSERT OR REPLACE INTO economy (settlement_id, item_id, stock, price)
            VALUES (?, ?, ?, ?)
        """, (
            s["id"], int(item_id),
            item_data["stock"], item_data["price"]
        ))

# ── Finish ─────────────────────────────────────────────────────

conn.commit()
conn.close()

print("Database created successfully!")
print(f"Settlements: {len(world['settlements'])}")
print(f"Routes: {len(world['routes'])}")
print(f"Cultures: {len(world['cultures'])}")
print(f"States: {len(world['states'])}")
print(f"Items: {len(items_data['items'])}")
print(f"Economy entries: {len(economy)}")