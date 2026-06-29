import { useState } from 'react'
function InfoPanel({ selected, world, onClose }) {
    const [selectedItem, setSelectedItem] = useState("1")
    
    if (!selected) return null

    // Build lookup maps
    const cultureMap = world.world.cultures.reduce((acc, c) => {
        acc[c.id] = c.name
        return acc
    }, {})

    const stateMap = world.world.states.reduce((acc, s) => {
        acc[s.id] = s.name
        return acc
    }, {})

    const settlementEconomy = world.economy.filter(
        e => e.settlement_id === selected.id
    )

    const currentItem = settlementEconomy.find(e => String(e.item_id) === selectedItem) ?? settlementEconomy[0]

    return (
        <div className='info-panel'>
            <button onClick={onClose}>X</button>
            <h2>{selected.name}</h2>
            <p>Tier: {selected.tier}</p>
            <p>Population: {selected.population.toLocaleString()}</p>
            <p>State: {stateMap[selected.state_id]}</p>
            <p>Culture: {cultureMap[selected.culture_id]}</p>
            <p>Biome: {selected.biome_name}</p>
            {settlementEconomy && (
                <div>
                    <select
                        value={currentItem ? String(currentItem.item_id) : ""}
                        onChange={e => setSelectedItem(e.target.value)}
                    >
                        {settlementEconomy.map(item => (
                            <option
                                key={item.item_id}
                                value={item.item_id}
                            >
                                {item.name}
                            </option>
                        ))}
                    </select>
                    <p>Item: {currentItem?.name}</p>
                    <p>Stock: {currentItem?.stock}</p>
                    <p>Cost: {currentItem?.price} cp</p>
                </div>
            )}
        </div>
    )
}

export default InfoPanel