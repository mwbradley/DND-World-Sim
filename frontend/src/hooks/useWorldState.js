import { useState, useEffect } from "react"

function useWorldState() {
    const [world, setWorld] = useState(null)

    useEffect(() => {
        fetch("http://localhost:8000/world-state")
            .then(r => r.json())
            .then(data => setWorld(data))
    }, [])

    return world
}

export default useWorldState