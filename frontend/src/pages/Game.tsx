import { useParams } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { getGame } from "../api/game";
import type { GameData } from "../types/game";


function Game() {
    const { gameId } = useParams();
    const [game, setGame] = useState<GameData | null>(null);
    const [loading, setLoading] = useState(true);
    const [isMyTurn, setIsMyTurn] = useState(false);
    const [statusMessage, setStatusMessage] = useState("");
    const wsRef = useRef<WebSocket | null>(null);



    useEffect(() => {
        const apiUrl = import.meta.env.VITE_API_URL;

        const ws = new WebSocket(`${apiUrl}/games/game_data?game_id=${gameId}&player_id=1`);
        wsRef.current = ws;

        ws.onopen = () => {
            console.log('Connected to the WebSocket server');
            fetchGame();
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("Data received -> ", data);

            switch (data.type) {
                case "GET_USER_PREFLOP_BET":
                case "GET_USER_FLOP_BET":
                case "GET_USER_TURN_BET":
                case "GET_USER_RIVER_BET":
                    setIsMyTurn(true);
                    setStatusMessage("It's your turn!");
                    fetchGame();
                    break;
                case "BOT_THINKING":
                    setStatusMessage(`${data.player_name || "Bot"} is thinking...`);
                    break;
                case "BOT_ACTION":
                    setStatusMessage(`${data.player_name || "Bot"} acted: ${data.action}`);
                    fetchGame();
                    break;
                case "OPEN_TABLE_CARD":
                    setStatusMessage(`Card revealed: ${data.card}`);
                    fetchGame();
                    break;
                case "WINNER":
                    alert(`Winner: ${data.winner_name} with ${data.amount} chips!`);
                    fetchGame();
                    break;
                case "SPLIT_POT":
                    alert(`Split Pot! Winners: ${data.winners.join(", ")}. Each gets ${data.amount}`);
                    fetchGame();
                    break;
                default:
                    console.log("Unknown message type:", data.type);
            }
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
            switch (data.state) {
                case "PREFLOP":
                    console.log("is preflop state");
            }
        }
    }, [gameId]);

    function sendAction(action: string, amount: number = 0) {
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            setIsMyTurn(false);
            setStatusMessage("Action sent, waiting for others...");
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
        sendAction("Call", game?.call_amt);
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
            <p>Pot: {game.pot}</p>
            <br />
            <div style={{ marginBottom: '10px', fontWeight: 'bold', color: isMyTurn ? 'green' : 'black' }}>
                {statusMessage || (isMyTurn ? "Your turn to act!" : "Waiting for players...")}
            </div>
            <table>
                <thead>
                    <tr>
                        <th colSpan={6} >Players</th>
                    </tr>
                    <tr>
                        <th>Player Name</th>
                        <th>Chips</th>
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
            <div>
                <p><b>Table Cards</b></p>
                {game.table_cards.map((tc) => (
                    <p>{ tc }</p>
                ))}
            </div>
            <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
                <button onClick={handleCall} disabled={!isMyTurn}>Call / Bet</button>
                <button onClick={handleRaise} disabled={!isMyTurn}>Raise</button>
                <button onClick={handleFold} disabled={!isMyTurn}>Fold</button>
                <button onClick={handleAllIn} disabled={!isMyTurn}>All In</button>
            </div>
        </>

    );
}

export default Game;