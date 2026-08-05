import client from "./client";

export async function createGame(data: {
    host_name: string;
    starting_money: number;
    max_players: number;
}) {
    const response = await client.post("/games/creategame", data);

    return response.data;
}