import { useState } from "react";
import { createGame } from "../api/game";
import { useNavigate } from "react-router-dom";

function CreateGame() {
    const navigate = useNavigate();

    const [hostName, setHostName] = useState("");
    const [chips, setChips] = useState(1000);
    const [maxPlayers, setMaxPlayers] = useState(6);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleSubmit() {
        setLoading(true);
        setError("");

        try {
            const response = await createGame({
                host_name: hostName,
                starting_money: chips,
                max_players: maxPlayers,
            });

            console.log(response);
            
            navigate(`/games/${response}`);

        } catch (err) {
            setError("Failed to create game.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    }

    return (
        <>
            <div>
                <label>Host Name</label>
                <input
                    type="text"
                    value={hostName}
                    onChange={(e) => setHostName(e.target.value)}
                />
            </div>

            <div>
                <label>Starting Chips</label>
                <input
                    type="number"
                    value={chips}
                    onChange={(e) => setChips(Number(e.target.value))}
                />
            </div>

            <div>
                <label>Maximum Players</label>
                <input
                    type="number"
                    value={maxPlayers}
                    onChange={(e) => setMaxPlayers(Number(e.target.value))}
                />
            </div>

            <button onClick={handleSubmit} disabled={loading}>
                {loading ? "Creating..." : "Create Game"}
            </button>

            {error && <p>{error}</p>}
        </>
    );
}

export default CreateGame;