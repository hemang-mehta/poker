import poker.deck as deck
from poker.player import Player, Bot
from poker.dealer import Dealer
from poker.betting_logic import BettingLogic
from poker.hand_evaluator import Evaluator
import asyncio
from core.connection_manager import manager as connection_manager
class PokerGame:

    def __init__(self, guid, host_name, starting_money, max_players):
        
        self.guid = guid
        
        # Full Deck
        self.deck = deck.Deck()
        self.full_deck = self.deck.create_full_deck()

        self.table_cards = []
        
        self.num_players = 1
        self.max_players = max_players
        self.players: list[Player] = []
        
        self.pot = 0
        self.small_blind = 100
        self.big_blind = 200
        self.call_amt = self.big_blind
        
        self.main_dealer = Dealer(self)
        self.dealer_ind = 0  # NEW: tracks the button/dealer seat+
        
        self.state = "PREFLOP"
        self.current_turn_index = None

        self.create_players(host_name, starting_money)
        
        self.bet_logic = BettingLogic(self)
        self.evaluator = Evaluator(self)
    
    async def action(self):
        # Deal cards and get the blind values
        if self.state == "PREFLOP":
            self._initialize_hands()
            self.post_blinds()
        # Get the preflop bets
        elif self.state == "PREFLOP_BETTING":
            sb_ind = self._next_active_index(self.dealer_ind)
            bb_ind = self._next_active_index(sb_ind)
            await self._process_betting_round(last_ind=bb_ind, user_event_type="GET_USER_PREFLOP_BET")
        # Open 3 cards for the table for all to see
        elif self.state == "OPEN_3_TABLE_CARDS":
            await self._open_table_cards(3)
            self.state = "FLOP_BETTING"
        # Get bets
        elif self.state == "FLOP_BETTING":
            await self._process_betting_round(last_ind=self.dealer_ind, user_event_type="GET_USER_FLOP_BET")
        # Open 4th table card
        elif self.state == "OPEN_TURN_CARD":
            await self._open_table_cards(1)
            self.state = "TURN_BETTING"
        # When the 4th table card is opened
        elif self.state == "TURN_BETTING":
            await self._process_betting_round(last_ind=self.dealer_ind, user_event_type="GET_USER_TURN_BET")
        # Open 5th table card
        elif self.state == "OPEN_RIVER_CARD":
            await self._open_table_cards(1)
            self.state = "RIVER_BETTING"
        # When all table cards are opened
        elif self.state == "RIVER_BETTING":
            await self._process_betting_round(last_ind=self.dealer_ind, user_event_type="GET_USER_RIVER_BET")
        # Evaluate hands
        elif self.state == "EVAL_HANDS":
            await self.showdown()
    
    def send_state(self, state):
        # We use create_task to send the state asynchronously without blocking the game logic
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(connection_manager.broadcast_to_game(self.guid, state))
        except RuntimeError:
            # This might happen during initialization or tests where no loop is running
            print(f"No event loop running, could not send state: {state}")

    #########################################
    #   Game State Functions
    #########################################
    
    async def _process_betting_round(self, last_ind, user_event_type, curr_player_ind=-1):
        while not self._is_betting_round_complete():
            next_ind = self._next_active_index(last_ind)
            self.current_turn_index = next_ind
            player: Player = self.players[next_ind]

            # Check if it's the human player's turn
            # We assume the human player is not a Bot (doesn't have decide_action)
            # or matches the provided curr_player_ind
            is_human = not player.is_bot
            if (curr_player_ind != -1 and next_ind == curr_player_ind) or (curr_player_ind == -1 and is_human):
                # It's the user's turn: notify via websocket and STOP to wait for input.
                self.send_state({
                    "type": user_event_type,
                    "player_id": player.player_ind,
                    "game_id": self.guid
                })
                return

            # It's a bot's turn: simulate thinking and then act.
            # 1. Notify frontend that bot is thinking
            self.send_state({
                "type": "BOT_THINKING",
                "player_id": next_ind,
                "player_name": player.player_name,
                "game_id": self.guid
            })

            # 2. Simulate "thinking" delay
            await asyncio.sleep(1.5)

            # 3. Process their action
            action_result = player.decide_action(self) if hasattr(player, 'decide_action') else None

            if action_result is None:
                # Default action for bots if logic is not yet implemented
                self.handle_player_action(next_ind, "Call", 0)
                action_type, amount = "Call", 0
            else:
                action_type, amount = action_result
                self.handle_player_action(next_ind, action_type, amount)

            # 4. Notify frontend of the actual action
            self.send_state({
                "type": "BOT_ACTION",
                "player_id": next_ind,
                "action": action_type,
                "amount": amount,
                "game_id": self.guid
            })

            last_ind = next_ind

    async def _open_table_cards(self, num_cards):
        for i in range(num_cards):
            card = self.main_dealer.open_table_card()
            
            # Simulate opening
            await asyncio.sleep(1.5)
            
            self.table_cards.append(card)
            
            self.send_state({
                "type": "OPEN_TABLE_CARD",
                "card": card,
                "game_id": self.guid
            })
    
    async def showdown(self):
        # 1. Evaluate winners
        winners: list[Player] = self.evaluator.evaluate_hands()

        # 2. Calculate distribution
        win_amount = self.pot // len(winners)

        # 3. Pay the winners
        for player in winners:
            player.curr_money_left += win_amount

        # 4. Notify Frontend
        if len(winners) == 1:
            winner = winners[0]
            self.send_state({
                "type": "WINNER",
                "winner_name": winner.name,
                "amount": self.pot,
                "game_id": self.guid
            })
        else:
            self.send_state({
                "type": "SPLIT_POT",
                "winners": [p.name for p in winners],
                "amount": win_amount,
                "game_id": self.guid
            })

        # 5. Cleanup
        self.pot = 0
        self.state = "GAME_OVER"            
    
    #########################################
    #   Helper functions
    #########################################
    
    def _initialize_hands(self):        
        # Deal Cards
        self.main_dealer.deal_cards()        
    
    # Deducts small and big blinds from the respective players and adds them to the pot.
    def post_blinds(self):
        sb_ind = self._next_active_index(self.dealer_ind)
        bb_ind = self._next_active_index(sb_ind)

        sb_player = self.players[sb_ind]
        bb_player = self.players[bb_ind]

        sb_amt = min(self.small_blind, sb_player.curr_money_left)
        bb_amt = min(self.big_blind, bb_player.curr_money_left)

        sb_player.curr_money_left -= sb_amt
        sb_player.curr_round_bet += sb_amt
        if sb_player.curr_money_left == 0:
            sb_player.all_in = True

        bb_player.curr_money_left -= bb_amt
        bb_player.curr_round_bet += bb_amt
        if bb_player.curr_money_left == 0:
            bb_player.all_in = True

        self.pot += sb_amt + bb_amt
        
        self.state = "PREFLOP_BETTING"

    def is_players_turn(self, player_id):
        return self.current_turn_index == player_id

    def handle_player_action(self, player_id, action_type, amount=0):

        # 1. Verify it is actually this player's turn
        if not self.is_players_turn(player_id):
            return {"error": "Not your turn"}

        # 2. Delegate all action logic to BettingLogic
        result = self.bet_logic.handle_bet(player_id, action_type, amount)

        # 3. Check if the betting round is over
        if self._is_betting_round_complete():
            self._advance_game_state()

        return result

    """First seat after from_ind that hasn't folded or been eliminated."""
    def _next_active_index(self, from_ind):
        for step in range(1, self.num_players + 1):
            candidate = (from_ind + step) % self.num_players
            p: Player = self.players[candidate]
            if not p.fold and not p.eliminated:
                return candidate
        return from_ind

    """Check is betting round is completed"""
    def _is_betting_round_complete(self):
        for i in range(len(self.players)):
            player: Player = self.players[i]
            if player.fold or player.all_in:
                continue
            elif player.curr_round_bet == self.call_amt:
                continue
            else:
                return False
        return True

    """If only one player remains un-folded, award them the pot and end the hand."""
    def _hand_over(self):
        remaining = [p for p in self.players if not p.fold and not p.eliminated]
        if len(remaining) == 1:
            self._award_pot(remaining)
            return True
        return False

    """
    Splits the pot evenly among winners.
    NOTE: this does not implement side pots. If players went all-in for
    different amounts this round, a proper side-pot calculation is needed
    instead of a flat even split.
    """
    def _award_pot(self, winners):
        if not winners:
            return
        share = self.pot // len(winners)
        for w in winners:
            w.curr_money_left += share
            print(f"Player {self.players.index(w) + 1} wins {share} chips!")
        self.pot = 0

    """Transitions the game to the next phase after a betting round completes."""
    def _advance_game_state(self):
        if self.state == "PREFLOP_BETTING":
            self.state = "OPEN_3_TABLE_CARDS"
        elif self.state == "FLOP_BETTING":
            self.state = "OPEN_TURN_CARD"
        elif self.state == "TURN_BETTING":
            self.state = "OPEN_RIVER_CARD"
        elif self.state == "RIVER_BETTING":
            self.state = "SHOWDOWN"
        else:
            print(f"Warning: No advance state defined for {self.state}")

    """Create the user as player 1 and the rest are bots"""
    def create_players(self, host_name, host_money):
        # Creating Players
        self.players = []
        
        self.players.append(Player(id=1, name=host_name, money=host_money))
        for i in range(self.max_players - 1):
            self.players.append(Bot(id=i+2, name=f"Bot_{i+1}", is_bot=True))
        return

