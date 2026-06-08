def produce_goods(settlement, items):
    for i in items:
        if settlement["biome_name"] in i["produced_by"]:
            settlement["inventory"][str(i["id"])]["stock"] += i["production_rate"]


def adjust_prices(settlement, items):
    for i in items:
        settlement["inventory"][str(i["id"])]["price"] = new_price(settlement, i)


def apply_consumption(settlement, items):
    if settlement["population"] > 10000:
            consumption_rate = 75
    elif settlement["population"] > 7500:
        consumption_rate = 50
    elif settlement["population"] > 5000:
        consumption_rate = 25
    else:
        consumption_rate = 15
    for i in items:
        if i["rarity"] == "common":
            consume = consumption_rate
        elif i["rarity"] == "uncommon":
            consume = consumption_rate // 5
        else:
            consume = 0
        settlement["inventory"][str(i["id"])]["stock"] = max(0, settlement["inventory"][str(i["id"])]["stock"] - consume)



def new_price(settlement, item):
    current_stock = settlement["inventory"][str(item["id"])]["stock"]
    if settlement["tier"] == "city":
        ideal_stock = 2000
    elif settlement["tier"] == "town":
        ideal_stock = 1499
    else:
        ideal_stock = 499
    return int(item["base_price"] * (1 + 0.2) ** ((ideal_stock - current_stock) / ideal_stock))