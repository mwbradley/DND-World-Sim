import { useState, useEffect } from "react"

function useWorldState() {
    const [world, setWorld] = useState(null)

    const fetchWorld = () => {
        fetch("http://localhost:8000/world-state")
            .then(r => r.json())
            .then(data => setWorld(data))
    }

    useEffect(() => {
        fetchWorld()
    }, [])

    return { world, refresh: fetchWorld }
}

export default useWorldState