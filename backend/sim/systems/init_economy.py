import json
import random

with open("world_seed.json", "r", encoding="utf-8") as f1, open("items.json", "r", encoding="utf-8") as f2:
    world_data = json.load(f1)
    item_data = json.load(f2)

settlements = []
stock_multiplier = {
    "common": 1.0,
    "uncommon": 0.5,
    "rare": 0.1
}

for s in world_data["settlements"]:
    inventory = {}
    if s["tier"] == "city":
        stock = random.randint(1500, 2000)
    elif s["tier"] == "town":
        stock = random.randint(500, 1499)
    else:
        stock = random.randint(100, 499)

    for i in item_data["items"]:
        if s["biome_name"] in i["produced_by"]:
            price = random.randint(int(i["base_price"] * 1.1), int(i["base_price"] * 2.2))
        else:
            price = random.randint(int(i["base_price"] * 1.6), int(i["base_price"] * 5))

        inventory[str(i["id"])] = {
            "stock": max(1, int(stock * stock_multiplier.get(i["rarity"], 1.0))),
            "price": price
            }

    settlements_dict = {
        "id": s["id"],
        "name": s["name"],
        "inventory": inventory
        }
    
    settlements.append(settlements_dict)


with open("economy_state.json", "w", encoding="utf-8") as f:
    json.dump(settlements, f, indent=2)


print(f"Settlements loaded: {len(world_data['settlements'])}")
print(f"First settlement: {world_data['settlements'][0]['name']}")
print(f"Items loaded: {len(item_data['items'])}")