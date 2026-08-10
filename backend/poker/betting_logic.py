from __future__ import annotations
from poker.player import Player
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from poker.game import PokerGame

class BettingLogic:
    """
    Handles a single betting round (pre-flop, flop, turn, or river) for one hand.

    Assumes each Player object has:
        fold (bool), eliminated (bool), all_in (bool),
        curr_money_left (number), curr_round_bet (number)

    Assumes the Game object has:
        players (list), num_players (int), pot (number), big_blind (number), call_amt (number)
    """

    def __init__(self, game):
        self.game: PokerGame = game
        self.player = None

    def is_valid_player(self):
        if self.player is not None and (self.player.eliminated or self.player.fold):
            return False
        return True

    def handle_bet(self, player, action, amount):
        self.player: Player = player

        if not self.is_valid_player():
            return False

        if action == "Call":
            return self.handle_call(amount)
        elif action == "Raise":
            return self.handle_raise(amount)
        elif action == "Fold":
            return self.handle_fold()
        elif action == "All In":
            return self.handle_all_in()
        return False

    def handle_call(self, call_amount):
        # amount needed to match the current bet
        amount_needed = call_amount - self.player.curr_round_bet

        if amount_needed <= 0:
            return True # Already called or bet more

        if self.player.curr_money_left < amount_needed:
            return self.handle_all_in()

        # Process call
        self.game.pot += amount_needed
        self.player.curr_money_left -= amount_needed
        self.player.curr_round_bet += amount_needed
        return True

    def handle_raise(self, raise_amount):
        # New total bet for the round = current_call_amt + raise_amount
        new_total_bet = self.game.call_amt + raise_amount
        amount_to_add = new_total_bet - self.player.curr_round_bet

        if amount_to_add <= 0:
            return True

        if self.player.curr_money_left < amount_to_add:
            return self.handle_all_in()

        # Process raise
        self.game.pot += amount_to_add
        self.player.curr_money_left -= amount_to_add
        self.player.curr_round_bet += amount_to_add
        self.game.call_amt = new_total_bet
        return True

    def handle_fold(self):
        self.player.fold = True
        return True

    def handle_all_in(self):
        amount_added = self.player.curr_money_left

        if amount_added <= 0:
            self.player.all_in = True
            return True

        self.game.pot += amount_added
        self.player.curr_round_bet += amount_added
        self.player.curr_money_left = 0
        self.player.all_in = True

        # The round's calling amount is the highest bet placed
        self.game.call_amt = max(self.game.call_amt, self.player.curr_round_bet)
        return True
