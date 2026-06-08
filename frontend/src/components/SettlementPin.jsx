import { useState } from 'react'
function SettlementPin({ settlement, onClick }) {
    const color = settlement.tier === "city" ? "#ffd700" : 
                  settlement.tier === "town" ? "#c0c0c0" : "#8B7355"
    const size = settlement.tier === "city" ? 12 : 
                 settlement.tier === "town" ? 8 : 5

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