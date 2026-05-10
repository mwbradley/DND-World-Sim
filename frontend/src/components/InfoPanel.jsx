function InfoPanel({ selected, world, onClose }) {
    if (!selected) return null

    // Build lookup maps
    const cultureMap = world.cultures.reduce((acc, c) => {
        acc[c.id] = c.name
        return acc
    }, {})

    const stateMap = world.states.reduce((acc, s) => {
        acc[s.id] = s.name
        return acc
    }, {})

    return (
        <div className='info-panel'>
            <button onClick={onClose}>X</button>
            <h2>{selected.name}</h2>
            <p>Tier: {selected.tier}</p>
            <p>Population: {selected.population.toLocaleString()}</p>
            <p>State: {stateMap[selected.state]}</p>
            <p>Culture: {cultureMap[selected.culture]}</p>
        </div>
    )
}

export default InfoPanel