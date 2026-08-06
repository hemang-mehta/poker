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

export type GameData = {
    guid: string;
    small_blind: number,
    big_blind: number,
    players: Player[],
    max_players: number,
    num_players: number,
    pot: number,
    table_cards: string[]
};

type Player = {
    all_in: boolean,
    cards: string[],
    curr_money_left: number,
    curr_round_bet: number,
    eliminated: boolean,
    fold: boolean,
    hand: string[],
    hand_rank: number,
    is_bot: boolean,
    player_name: string,
    total_bet: number,
}