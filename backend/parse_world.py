import json

with open("MatesiaFull.json", "r", encoding="utf-8") as f:
    data = json.load(f)

burgs_data = data["pack"]["burgs"]

# Burg groups
# groups = {}
# for b in burgs[1:]:
#     g = b.get("group", "unknown")
#     groups[g] = groups.get(g, 0) + 1
# print("Burg groups:", groups)

# Tier breakdown using population
# cities  = [b for b in burgs[1:] if b["population"] >= 10]
# towns   = [b for b in burgs[1:] if 2 <= b["population"] < 10]
# villages = [b for b in burgs[1:] if b["population"] < 2]

# print(f"\nCities (10k+): {len(cities)}")
# print(f"Towns (2k-10k): {len(towns)}")
# print(f"Villages (<2k): {len(villages)}")

# Cultures
cultures_data = data["pack"]["cultures"]
# for c in cultures[1:]:
#     print(f"Culture {c['i']}: {c['name']}")

# States
states_data = data["pack"]["states"]

# Biomes
biomes_data = data["biomesData"]


# Routes
routes_data = data["pack"]["routes"]


settlements = [];

for s in burgs_data[1:]:
    pop = s["population"]
    if pop >= 10:
        tier = "city"
    elif pop >= 2:
        tier = "town"
    else:
        tier = "village"

    burg_dict = {
        "id": s["i"],
        "cell": s["cell"],
        "name": s["name"],
        "x": s["x"],
        "y": s["y"],
        "population": round(pop * 1000),
        "state": s["state"],
        "culture": s["culture"],
        "is_capital": s.get("capital", 0),
        "is_port": s.get("type") in ("Ocean", "River", "Lake"),
        "has_market": s.get("plaza", 0),
        "has_walls": s.get("walls", 0),
        "has_citadel": s.get("citadel", 0),
        "tier": tier
    }
    if (tier != "village"):
        settlements.append(burg_dict)

cultures = []

for c in cultures_data[1:]:
    culture_dict = {
        "id": c["i"],
        "name": c["name"]
    }
    cultures.append(culture_dict)


states = []

for s in states_data[1:]:
    state_dict = {
        "id": s["i"],
        "name": s["name"]
    }
    states.append(state_dict)


cell_to_burg = {}

for s in settlements:
    cell_to_burg[s["cell"]] = s["id"]


routes = []
seen_edges = set()

for r in routes_data:
    found = []
    for point in r["points"]:
        cell_id = point[2]
        if cell_id in cell_to_burg:
            found.append(cell_to_burg[cell_id])

    for i in range(len(found) - 1):
        a, b = found[i], found[i+1]
        edge_key = (min(a,b), max(a,b))
        if edge_key not in seen_edges:
            seen_edges.add(edge_key)
            routes.append({
                "from_id": a,
                "to_id": b,
                "type": r["group"]
            })


world = {
    "settlements": settlements,
    "cultures": cultures,
    "states": states,
    "routes": routes
}

with open("world_seed.json", "w", encoding="utf-8") as f:
    json.dump(world, f, indent=2)

print(f"Settlements: {len(settlements)}")
print(f"Cultures: {len(cultures)}")
print(f"States: {len(states)}")
print(f"Routes: {len(routes)}")