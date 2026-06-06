import json
with open("world_seed.json") as f:
    world = json.load(f)
print(len(world["settlements"]))