import { useState, useEffect, useRef } from 'react'
import useWorldState from '../hooks/useWorldState'
import SettlementPin from './SettlementPin'
import InfoPanel from './InfoPanel'
import RouteLine from './RouteLine'

const THRESHOLD = 15

function MapCanvas() {
    const [svgContent, setSvgContent] = useState(null)
    const [selected, setSelected] = useState(null)
    const [transform, setTransform] = useState({ x: 0, y: 0, scale: 1 })
    const isDragging = useRef(false)
    const dragStart = useRef({ x: 0, y: 0 })
    const didDrag = useRef(false)
    const transformRef = useRef({ x: 0, y: 0, scale: 1 })
    const containerRef = useRef(null)
    const world = useWorldState()
    const mousePos = useRef({ x: 0, y: 0 })

    useEffect(() => {
        fetch("/maps/Matesia.svg")
            .then(r => r.text())
            .then(text => {
                const cleaned = text.replace(
                    /<svg([^>]*)width="1920"([^>]*)height="1006"/,
                    '<svg$1$2 viewBox="0 0 1920 1006"'
                )
                setSvgContent(cleaned)
            })
    }, [])

    // Non-passive wheel listener
    useEffect(() => {
        const el = containerRef.current
        if (!el) return

        const onWheel = (e) => {
            e.preventDefault()
            const scaleAmount = e.deltaY > 0 ? 0.9 : 1.1
            const t = transformRef.current
            const newScale = Math.min(Math.max(t.scale * scaleAmount, 0.3), 8)
            const mouseX = e.clientX
            const mouseY = e.clientY
            const newX = mouseX - (mouseX - t.x) * (newScale / t.scale)
            const newY = mouseY - (mouseY - t.y) * (newScale / t.scale)
            const newT = { x: newX, y: newY, scale: newScale }
            transformRef.current = newT
            setTransform({ ...newT })
        }

        el.addEventListener("wheel", onWheel, { passive: false })
        return () => el.removeEventListener("wheel", onWheel)
    }, [svgContent])

    const onMouseDown = (e) => {
        isDragging.current = true
        didDrag.current = false
        dragStart.current = {
            x: e.clientX - transformRef.current.x,
            y: e.clientY - transformRef.current.y
        }
        // Store the original click position for drag detection
        mousePos.current = { x: e.clientX, y: e.clientY }
    }

    const onMouseMove = (e) => {
        if (!isDragging.current) return
        // Only count as drag if moved more than 5px
        const dx = Math.abs(e.clientX - mousePos.current.x)
        const dy = Math.abs(e.clientY - mousePos.current.y)
        if (dx > 5 || dy > 5) didDrag.current = true
        
        const newT = {
            ...transformRef.current,
            x: e.clientX - dragStart.current.x,
            y: e.clientY - dragStart.current.y
        }
        transformRef.current = newT
        setTransform({ ...newT })
    }

    const onMouseUp = (e) => {
        isDragging.current = false
        if (!didDrag.current) {
            const t = transformRef.current
            const rect = containerRef.current.getBoundingClientRect()
            
            // Subtract container offset from click position
            const svgX = (e.clientX - rect.left - t.x) / t.scale
            const svgY = (e.clientY - rect.top - t.y) / t.scale

            let closest = null
            let closestDist = Infinity

            world?.settlements.forEach(s => {
                const dist = Math.sqrt(
                    Math.pow(s.x - svgX, 2) +
                    Math.pow(s.y - svgY, 2)
                )
                if (dist < closestDist) {
                    closestDist = dist
                    closest = s
                }
            })

            const dynamicThreshold = 15 / t.scale
            if (closestDist < dynamicThreshold) setSelected(closest)
            else setSelected(null)
        }
    }

    if (!svgContent || !world) return <div style={{color:"white"}}>Loading map...</div>

    const settlementMap = world.settlements.reduce((acc, s) => {
        acc[s.id] = { x: s.x, y: s.y }
        return acc
    }, {})

    return (
        <>
            <div className='map-wrapper'>
                <div
                    ref={containerRef}
                    className='map-container'
                    onMouseDown={onMouseDown}
                    onMouseMove={onMouseMove}
                    onMouseUp={onMouseUp}
                    style={{
                        width: "100vw",
                        height: "80vh",
                        overflow: "hidden",
                        cursor: isDragging.current ? "grabbing" : "grab",
                        background: "#1a1a2e"
                    }}
                >
                    <svg
                        width="1920"
                        height="1006"
                        style={{
                            transform: `translate(${transform.x}px, ${transform.y}px) scale(${transform.scale})`,
                            transformOrigin: "0 0",
                            display: "block"
                        }}
                    >
                        <image href="/maps/Matesia.svg" width={1920} height={1006} />
                        {world.routes.map(r => (
                            <RouteLine key={r.id} route={r} settlementMap={settlementMap} />
                        ))}
                        {world.settlements.map(s => (
                            <SettlementPin key={s.id} settlement={s} />
                        ))}
                    </svg>
                </div>
            </div>
            <InfoPanel selected={selected} world={world} onClose={() => setSelected(null)} />
        </>
    )
}

export default MapCanvas