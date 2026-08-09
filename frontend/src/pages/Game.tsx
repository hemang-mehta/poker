import { useParams } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { getGame } from "../api/game";
import type { GameData } from "../types/game";


function Game() {
    const { gameId } = useParams();
    const [game, setGame] = useState<GameData | null>(null);
    const [loading, setLoading] = useState(true);
    const wsRef = useRef<WebSocket | null>(null);


    useEffect(() => {
        const apiUrl = import.meta.env.VITE_API_URL;

        const ws = new WebSocket(apiUrl + "/games/game_data");
        wsRef.current = ws;

        ws.onopen = () => {
            console.log('Connected to the WebSocket server');
            fetchGame();
        };

        ws.onmessage = (event) => {
            console.log("data received -> ", event);
        }

        ws.onerror = () => {
            console.log("ws error");
        }

        ws.onclose = () => {
            console.log("ws closed");
        }

        async function fetchGame() {
            try {
                if (gameId == undefined) return;
                const data = await getGame(gameId);
                setGame(data);
            } catch (error) {
                console.error("Error fetching game:", error);
            } finally {
                setLoading(false);
            }
        }
    }, [gameId]);

    function sendMessage() {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({
                message: "ws msg"
            }));
        }
    }


    if (loading) return <p>Loading...</p>;
    if (!game) return <p>Game not found</p>;

    return (
        <>
            <h1> Game Title: {game.guid}</h1>
            <br />
            <p>Small Blind: {game.small_blind}</p>
            <p>Big Blind: {game.big_blind}</p>
            <br />
            <table>
                <thead>
                    <tr>
                        <th colSpan={6} >Players</th>
                    </tr>
                    <tr>
                        <th>Player Name</th>
                        <th>Holding</th>
                        <th>Is Bot?</th>
                        <th>All In?</th>
                        <th>Fold?</th>
                        <th>Eliminated?</th>
                    </tr>
                </thead>

                <tbody>
                    {game.players.map((player) => (
                        <tr key={player.player_name}>
                            <td>{player.player_name}</td>
                            <td>{player.curr_money_left}</td>
                            <td>{player.is_bot ? "Yes" : "No"}</td>
                            <td>{player.all_in ? "Yes" : "No"}</td>
                            <td>{player.fold ? "Yes" : "No"}</td>
                            <td>{player.eliminated ? "Yes" : "No"}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <button onClick={sendMessage}>Bet</button>
        </>
    );
}

export default Game;