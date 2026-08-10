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

        const ws = new WebSocket(`${apiUrl}/games/game_data?game_id=${gameId}`);
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
                const data: GameData = await getGame(gameId, 1);
                gameState(data);
                setGame(data);
            } catch (error) {
                console.error("Error fetching game:", error);
            } finally {
                setLoading(false);
            }
        }

        function gameState(data: GameData) {
            switch(data.state)
            {
                case "PREFLOP":
                    console.log("is preflop state");
            }
        }
    }, [gameId]);

    function sendAction(action: string, amount: number = 0) {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({
                type: "PLAYER_ACTION",
                action: action,
                amount: amount,
                gameid: gameId,
                player_id: 1 // Hardcoded for now, should be current user ID
            }));
        } else {
            console.error("WebSocket is not open");
        }
    }

    function handleCall() {
        sendAction("Call");
    }

    function handleRaise() {
        const amount = window.prompt("Enter raise amount:");
        const raiseAmt = Number(amount);
        if (!isNaN(raiseAmt) && raiseAmt > 0) {
            sendAction("Raise", raiseAmt);
        } else {
            alert("Please enter a valid amount");
        }
    }

    function handleFold() {
        sendAction("Fold");
    }

    function handleAllIn() {
        sendAction("All In");
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
            <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
                <button onClick={handleCall}>Call / Bet</button>
                <button onClick={handleRaise}>Raise</button>
                <button onClick={handleFold}>Fold</button>
                <button onClick={handleAllIn}>All In</button>
            </div>
        </>

    );
}

export default Game;