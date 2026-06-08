import { useState, useEffect } from "react"

function useTick(onTickComplete) {
    const [world, setWorld] = useState(null)

    const tick =() => {
        fetch("http://localhost:8000/tick", {
            method: "POST"
        })
            .then(r => r.json())
            .then(data => {
                console.log("Tick complete", data)
                if (onTickComplete) onTickComplete()
            })
    }

    return { tick }
}

export default useTick