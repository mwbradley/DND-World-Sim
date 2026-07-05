import sqlite3
from sim.systems.economy import produce_goods, apply_consumption, adjust_prices

conn = sqlite3.connect("matesia.db", check_same_thread=False)
conn.row_factory = sqlite3.Row  # lets you access columns by name like a dict
cursor = conn.cursor()

def tick():
    cursor.execute("SELECT * FROM economy")
    economy_rows = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM items")
    items = {row["id"]: dict(row) for row in cursor.fetchall()}

    cursor.execute("SELECT * FROM settlements")
    settlements = {row["id"]: dict(row) for row in cursor.fetchall()}

    cursor.execute("SELECT item_id, biome_name FROM item_biomes")
    item_biomes = {}
    for row in cursor.fetchall():
        item_biomes.setdefault(row["item_id"], []).append(row["biome_name"])

    for econ_row in economy_rows:
        settlement = settlements[econ_row["settlement_id"]]
        item = items[econ_row["item_id"]]
        produced_by = item_biomes.get(item["id"], [])

        produce_goods(econ_row, item, settlement, produced_by)
        apply_consumption(econ_row, item, settlement)
        adjust_prices(econ_row, item, settlement)

        cursor.execute("""
            UPDATE economy SET stock = ?, price = ?
            WHERE settlement_id = ? AND item_id = ?
        """, (econ_row["stock"], econ_row["price"], econ_row["settlement_id"], econ_row["item_id"]))

    conn.commit()
    return economy_rows