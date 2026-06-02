import json

with open("world_seed.json") as f:
    world = json.load(f)

print(json.dumps(world["settlements"][0], indent=2))