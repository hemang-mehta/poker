export interface CreateGameRequest {
    host_name: string;
    starting_chips: number;
    max_players: number;
}

export interface CreateGameResponse {
    game_id: string;
    status: string;
    player_count: number;
}