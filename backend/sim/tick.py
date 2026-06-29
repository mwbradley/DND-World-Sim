import sqlite3
import json
from sim.systems.economy import produce_goods, apply_consumption, adjust_prices

with open ('economy_state.json', 'r', encoding='utf-8') as file1, open ('items.json', 'r', encoding='utf-8') as file2:
    econ_data = json.load(file1)
    items = json.load(file2)["items"]


def tick():
    for settlement in econ_data:
        produce_goods(settlement, items)
        apply_consumption(settlement, items)
        adjust_prices(settlement, items)

    with open('economy_state.json', 'w', encoding='utf-8') as f:
        json.dump(econ_data, f, indent=2)
    
    return econ_data