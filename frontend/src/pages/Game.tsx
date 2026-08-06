import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { getGame } from "../api/game";
import type { GameData } from "../types/game";

function Game() {
    const { gameId } = useParams();
    const [game, setGame] = useState<GameData | null>(null);
    const [loading, setLoading] = useState(true);

    // const socket = new WebSocket("ws://localhost:8080/ws");

    useEffect(() => {
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
        fetchGame();
    }, [gameId]);

    if (loading) return <p>Loading...</p>;
    if (!game) return <p>Game not found</p>;

    return (
        <>
            <h1> Game Title: {game.guid}</h1>
            <br/>
            <p>Small Blind: {game.small_blind}</p>
            <p>Big Blind: {game.big_blind}</p>
            <br/>
        </>
    );
}

export default Game;