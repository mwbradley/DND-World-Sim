import { useState, useEffect } from "react"

function useWorldState() {
    const [world, setWorld] = useState(null)

    useEffect(() => {
        fetch("/world_seed.json")
            .then(r => r.json())
            .then(data => setWorld(data))
    }, [])

    return world
}

export default useWorldState