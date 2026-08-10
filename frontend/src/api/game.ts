import client from "./client";
import type { AxiosResponse } from "axios";
import type { CreateGameResponse } from "../types/game";

export async function createGame(data: {
    host_name: string;
    starting_money: number;
    max_players: number;
}): Promise<AxiosResponse<CreateGameResponse>> {
    return await client.post("/games/creategame", data);
}

export async function getGame(gameID: string, playerId?: number) {
    const response = await client.get("/games/" + gameID, {
        params: {
            player_id: playerId
        }
    });
    return response.data;
}