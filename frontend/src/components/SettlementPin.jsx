function SettlementPin({ settlement, onClick }) {
    const color = settlement.tier === "city" ? "#ffd700" : "#c0c0c0"
    const size = settlement.tier === "city" ? 8 : 5

    return (
        <circle
            cx={settlement.x}
            cy={settlement.y}
            r={size}
            fill={color}
            stroke="#000"
            strokeWidth={2}
            opacity={0.9}
        />
    )
}

export default SettlementPin