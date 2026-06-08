import useTick from "../hooks/useTick"
function ControlBar({ world, onTickComplete }) {

    const { tick } = useTick(onTickComplete)

    return (
        <div className='control-bar'>
            <button onClick={tick}>Next Tick</button>
        </div>
    )
}

export default ControlBar