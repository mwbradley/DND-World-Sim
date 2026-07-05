def produce_goods(econ_row, item, settlement, produced_by):
    if settlement["biome_name"] in produced_by:
        econ_row["stock"] += item["production_rate"]


def adjust_prices(econ_row, item, settlement):
    econ_row["price"] = new_price(econ_row, settlement, item)

def apply_consumption(econ_row, item, settlement):
    if settlement["population"] > 10000:
        consumption_rate = 75
    elif settlement["population"] > 7500:
        consumption_rate = 50
    elif settlement["population"] > 5000:
        consumption_rate = 25
    else:
        consumption_rate = 15

    if item["rarity"] == "common":
        consume = consumption_rate
    elif item["rarity"] == "uncommon":
        consume = consumption_rate // 5
    else:
        consume = 0
    econ_row["stock"] = max(0, econ_row["stock"] - consume)

def new_price(econ_row, settlement, item):
    current_stock = econ_row["stock"]
    if settlement["tier"] == "city":
        ideal_stock = 2000
    elif settlement["tier"] == "town":
        ideal_stock = 1499
    else:
        ideal_stock = 499
    return int(item["base_price"] * (1 + 0.2) ** ((ideal_stock - current_stock) / ideal_stock))