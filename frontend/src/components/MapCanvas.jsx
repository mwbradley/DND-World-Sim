import { useState, useEffect, useRef } from 'react'
import useWorldState from '../hooks/useWorldState'
import SettlementPin from './SettlementPin'

const THRESHOLD = 5

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
    }

    const onMouseMove = (e) => {
        if (!isDragging.current) return
        didDrag.current = true
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
            const svgX = (e.clientX - t.x) / t.scale
            const svgY = (e.clientY - t.y) / t.scale
            console.log("Click SVG coords:", svgX, svgY)

            const hit = world?.settlements.find(s =>
                Math.abs(s.x - svgX) < THRESHOLD &&
                Math.abs(s.y - svgY) < THRESHOLD
            )
            if (hit) setSelected(hit)
            else setSelected(null)
        }
    }

    if (!svgContent || !world) return <div style={{color:"white"}}>Loading map...</div>

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
                        {world.settlements.map(s => (
                            <SettlementPin key={s.id} settlement={s} />
                        ))}
                    </svg>
                </div>
            </div>
            {selected && (
                <div className='info-panel'>
                    <button onClick={() => setSelected(null)}>X</button>
                    <h2>{selected.name}</h2>
                    <p>Tier: {selected.tier}</p>
                    <p>Population: {selected.population.toLocaleString()}</p>
                    <p>State: {selected.state}</p>
                    <p>Culture: {selected.culture}</p>
                </div>
            )}
        </>
    )
}

export default MapCanvas