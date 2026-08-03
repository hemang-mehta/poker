class BettingLogic:
    """
    Handles a single betting round (pre-flop, flop, turn, or river) for one hand.

    Assumes each Player object has:
        fold (bool), eliminated (bool), all_in (bool),
        curr_money_left (number), curr_round_bet (number)

    Assumes the Game object has:
        players (list), num_players (int), pot (number), big_blind (number)

    NOTE: Blind posting and dealer-button tracking aren't implemented here
    because those attributes weren't present on the Game/Player classes I
    was shown. Hook them in where marked below.
    """

    def __init__(self, game):
        self.game = game
        self.current_bet = 0        # highest total bet any player has put in this round
        self.min_raise = 0          # smallest legal raise increment
        self.player_ind = 0
        self.players_to_act = set()  # indices of players who still need to act this round

    def betting_round(self, preFlop, start_ind=0):
        """
        start_ind: index of the player who should act first this round
                   (left of big blind pre-flop, left of dealer post-flop).
        """
        print("\n\nPre-flop betting round ->" if preFlop else "\n\nBetting round ->")

        self.min_raise = self.game.big_blind

        if preFlop:
            # TODO: post blinds here (or before calling this method), e.g.:
            #   self._post_blind(sb_ind, self.game.small_blind)
            #   self._post_blind(bb_ind, self.game.big_blind)
            # Once blinds are posted, curr_round_bet for those two players
            # should already reflect what they've put in.
            self.current_bet = self.game.big_blind
        else:
            self.current_bet = 0
            for p in self.game.players:
                p.curr_round_bet = 0

        # Every player still in the hand and not already all-in must act
        # at least once this round.
        self.players_to_act = {
            i for i, p in enumerate(self.game.players)
            if not p.fold and not p.eliminated and not p.all_in
        }

        ind = start_ind

        while self.players_to_act and self._active_player_count() > 1:
            self.player_ind = ind % self.game.num_players
            player = self.game.players[self.player_ind]

            if player.fold:
                print(f"Player {self.player_ind + 1} is folded...")
                ind += 1
                continue

            if player.eliminated:
                print(f"Player {self.player_ind + 1} is already eliminated...")
                ind += 1
                continue

            if player.all_in:
                print(f"Player {self.player_ind + 1} is all in!")
                ind += 1
                continue

            player_money_left = player.curr_money_left
            player_decision, bet_amt = self.get_action(player_money_left)

            try:
                self.bet_chosen(player_decision, bet_amt)
            except ValueError as e:
                print(f"Invalid action: {e}")
                continue  # let the same player retry, don't advance ind

            self.players_to_act.discard(self.player_ind)
            ind += 1

        print("All bets accounted for! Let's play!")

    def _active_player_count(self):
        """Players still in the hand (not folded, not eliminated)."""
        return sum(
            1 for p in self.game.players
            if not p.fold and not p.eliminated
        )

    def get_action(self, player_money_left):
        print(f"Player {self.player_ind + 1} (Current Balance = {player_money_left}): ")
        print("Choose 1 of the following:\n1) Call\n2) Raise\n3) Fold\n4) All In")

        while True:
            try:
                player_decision = int(input("Your choice: "))
                if player_decision not in (1, 2, 3, 4):
                    print("Enter 1, 2, 3, or 4.")
                    continue
                break
            except ValueError:
                print("Enter a valid input.")

        bet_amt = 0
        curr_round_bet = self.game.players[self.player_ind].curr_round_bet

        if player_decision == 2:
            # bet_amt is the player's new TOTAL bet for the round, not just the increment
            min_total = self.current_bet + self.min_raise
            while True:
                try:
                    bet_amt = int(input(f"Enter your total bet (raise to at least {min_total}): "))
                    if bet_amt < min_total:
                        print(f"Raise must bring your total bet to at least {min_total}.")
                        continue
                    if bet_amt - curr_round_bet > player_money_left:
                        print("You don't have enough chips for that raise. Try All In instead.")
                        continue
                    break
                except ValueError:
                    print("Enter a valid input.")
        elif player_decision == 4:
            bet_amt = player_money_left + curr_round_bet

        return player_decision, bet_amt

    def bet_chosen(self, player_decision, bet_amt):
        player = self.game.players[self.player_ind]

        # Call
        if player_decision == 1:
            amt = self.current_bet - player.curr_round_bet
            if amt < 0:
                amt = 0
            if amt >= player.curr_money_left:
                amt = player.curr_money_left  # calling all-in for less than the full bet
                player.all_in = True

            self.game.pot += amt
            player.curr_money_left -= amt
            player.curr_round_bet += amt
            return

        # Raise
        elif player_decision == 2:
            amt = bet_amt - player.curr_round_bet
            if amt > player.curr_money_left:
                raise ValueError("Raise exceeds available chips.")

            self.min_raise = max(self.min_raise, bet_amt - self.current_bet)
            self.current_bet = bet_amt

            self.game.pot += amt
            player.curr_money_left -= amt
            player.curr_round_bet = bet_amt

            if player.curr_money_left == 0:
                player.all_in = True

            # A raise reopens the action for everyone else still in the hand
            self.players_to_act = {
                i for i, p in enumerate(self.game.players)
                if not p.fold and not p.eliminated and not p.all_in
            } - {self.player_ind}
            return

        # Fold
        elif player_decision == 3:
            player.fold = True
            # curr_round_bet is intentionally left as-is: that money is
            # already committed to the pot.
            return

        # All In
        elif player_decision == 4:
            amt = bet_amt - player.curr_round_bet
            if amt > player.curr_money_left:
                raise ValueError("All-in amount exceeds available chips.")

            player.all_in = True
            self.game.pot += amt
            player.curr_money_left -= amt
            player.curr_round_bet = bet_amt

            if bet_amt > self.current_bet:
                self.min_raise = max(self.min_raise, bet_amt - self.current_bet)
                self.current_bet = bet_amt
                # Reopens action, same as a raise
                self.players_to_act = {
                    i for i, p in enumerate(self.game.players)
                    if not p.fold and not p.eliminated and not p.all_in
                } - {self.player_ind}
            return

        raise ValueError("Unknown player decision.")