import backend.poker.card as card
import backend.poker.deck as deck

class PokerGame:

    def __init__(self, host_name, host_money, max_players):
        
        # Full Deck
        self.deck = deck.Deck()
        self.deck.create_full_deck()

        self.num_players = 1
        self.max_players = max_players
        self.table_cards = []
        self.players = []
        self.pot = 0
        self.small_blind = 100
        self.big_blind = 200
        self.dealer_ind = 0  # NEW: tracks the button/dealer seat

    def play(self):
        import backend.poker.betting_logic as betting_logic
        import backend.poker.dealer as dealer
        import backend.poker.hand_evaluator as hand_evaluator

        # Shuffle Deck
        self.cards.shuffle_cards(self.full_deck)

        # Get Players
        self.create_players()

        main_dealer = dealer.Dealer(self)

        # Deal Cards
        main_dealer.deal_cards()

        for i in range(self.num_players):
            print(f"Player {i + 1}: ")
            print("Your cards are -> ")
            print(self.cards.print_cards(self.players[i].cards))

        bets = betting_logic.BettingLogic(self)

        # Post blinds before any action happens
        self.post_blinds()

        # Pre-Flop: action starts left of the big blind
        bb_ind = self._next_active_index(self._next_active_index(self.dealer_ind))
        preflop_start = self._next_active_index(bb_ind)
        bets.betting_round(preFlop=True, start_ind=preflop_start)
        if self._hand_over():
            return

        # Flop
        main_dealer.open_table_cards(isPreFlop=True)
        bets.betting_round(preFlop=False, start_ind=self._next_active_index(self.dealer_ind))
        if self._hand_over():
            return

        # Turn
        main_dealer.open_table_cards(isPreFlop=False)
        bets.betting_round(preFlop=False, start_ind=self._next_active_index(self.dealer_ind))
        if self._hand_over():
            return

        # River  (previously missing entirely)
        main_dealer.open_table_cards(isPreFlop=False)
        bets.betting_round(preFlop=False, start_ind=self._next_active_index(self.dealer_ind))
        if self._hand_over():
            return

        # Showdown
        he = hand_evaluator.Evaluator(self)
        winner = he.evaluate_hands()
        self._award_pot([winner])

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

    def _next_active_index(self, from_ind):
        """First seat after from_ind that hasn't folded or been eliminated."""
        for step in range(1, self.num_players + 1):
            candidate = (from_ind + step) % self.num_players
            p = self.players[candidate]
            if not p.fold and not p.eliminated:
                return candidate
        return from_ind

    def _hand_over(self):
        """If only one player remains un-folded, award them the pot and end the hand."""
        remaining = [p for p in self.players if not p.fold and not p.eliminated]
        if len(remaining) == 1:
            self._award_pot(remaining)
            return True
        return False

    def _award_pot(self, winners):
        """
        Splits the pot evenly among winners.
        NOTE: this does not implement side pots. If players went all-in for
        different amounts this round, a proper side-pot calculation is needed
        instead of a flat even split.
        """
        if not winners:
            return
        share = self.pot // len(winners)
        for w in winners:
            w.curr_money_left += share
            print(f"Player {self.players.index(w) + 1} wins {share} chips!")
        self.pot = 0

    def create_players(self):
        import backend.poker.player as player

        # Creating Players
        self.players = []
        for i in range(self.num_players):
            self.players.append(player.Player())

        return self.players