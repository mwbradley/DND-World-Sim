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

    const econSettlement = world.economy.find(e => e.id === selected.id)
    const itemIds = econSettlement ? Object.keys(econSettlement.inventory) : []

    return (
        <div className='info-panel'>
            <button onClick={onClose}>X</button>
            <h2>{selected.name}</h2>
            <p>Tier: {selected.tier}</p>
            <p>Population: {selected.population.toLocaleString()}</p>
            <p>State: {stateMap[selected.state]}</p>
            <p>Culture: {cultureMap[selected.culture]}</p>
            <p>Biome: {selected.biome_name}</p>
            {econSettlement && (
                <div>
                    <select 
                        value={selectedItem} 
                        onChange={e => setSelectedItem(e.target.value)}
                    >
                        {itemIds.map(id => (
                            <option key={id} value={id}>
                                {econSettlement.inventory[id].name}
                            </option>
                        ))}
                    </select>
                    <p>Item: {econSettlement.inventory[selectedItem]?.name}</p>
                    <p>Stock: {econSettlement.inventory[selectedItem]?.stock}</p>
                    <p>Cost: {econSettlement.inventory[selectedItem]?.price}cp</p>
                </div>
            )}
        </div>
    )
}

export default InfoPanel