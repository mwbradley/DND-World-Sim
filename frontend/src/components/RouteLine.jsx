function RouteLine({ route, settlementMap }) {
    const from = settlementMap[route.from_id]
    const to = settlementMap[route.to_id]

    if (!from || !to) return null

    let color
    if (route.type === "roads") {
        color = "#740000";
    }
    else if (route.type === "trails") {
        color = "#614c0f";
    }
    else {
        color = "#000000";
    }

    return (
        <line
            x1={from.x}
            y1={from.y}
            x2={to.x}
            y2={to.y}
            stroke={color}
            strokeWidth={2}
            opacity={0.9}
        />
    )
}

export default RouteLine