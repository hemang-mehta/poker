from itertools import combinations
from collections import Counter
from poker.player import Player
from poker.game import PokerGame

class Evaluator:
    """
    Evaluates each remaining player's best 5-card hand out of their 2 hole
    cards + the community cards, and returns the winner (or a list of
    winners in the case of a tie / split pot).

    Card format: "suit_rank" strings, e.g. "1_1" = Ace of Spades.
    Suits: 1=Spade, 2=Diamond, 3=Club, 4=Heart
    Ranks: 1-13 (Ace=1, Jack=11, Queen=12, King=13)
    """

    HAND_NAMES = {
        8: "Straight Flush",
        7: "Four of a Kind",
        6: "Full House",
        5: "Flush",
        4: "Straight",
        3: "Three of a Kind",
        2: "Two Pair",
        1: "Pair",
        0: "High Card",
    }

    def __init__(self, game):
        self.game: PokerGame = game

    def evaluate_hands(self):
        contenders: list[Player] = [p for p in self.game.players if not p.fold and not p.eliminated]

        if not contenders:
            return None
        if len(contenders) == 1:
            return contenders[0]

        best_score = None
        winners: list[Player] = []

        for player in contenders:
            all_cards = player.cards + self.game.table_cards
            score, best_five = self._best_hand(all_cards)
            player.hand_rank = score[0]
            player.hand = best_five

            if best_score is None or score > best_score:
                best_score = score
                winners = [player]
            elif score == best_score:
                winners.append(player)

        return winners

    def _best_hand(self, cards):
        """Returns (score_tuple, best_5_cards) - the best 5-card hand out of all cards."""
        best_score = None
        best_combo = None
        for combo in combinations(cards, 5):
            score = self._score_five(combo)
            if best_score is None or score > best_score:
                best_score = score
                best_combo = combo
        return best_score, list(best_combo)

    def _score_five(self, five_cards):
        """
        Scores exactly 5 cards as a comparable tuple:
        (hand_category, tiebreaker_1, tiebreaker_2, ...)
        Higher tuples (compared lexicographically) win.
        """
        ranks = sorted((self._rank(c) for c in five_cards), reverse=True)
        suits = [self._suit(c) for c in five_cards]

        rank_counts = Counter(ranks)
        # Groups sorted by (count desc, rank desc) - naturally orders kickers correctly
        groups = sorted(rank_counts.items(), key=lambda item: (item[1], item[0]), reverse=True)
        ordered_ranks = [rank for rank, _count in groups]
        counts = sorted(rank_counts.values(), reverse=True)

        is_flush = len(set(suits)) == 1
        straight_high = self._straight_high(ranks)
        is_straight = straight_high is not None

        if is_straight and is_flush:
            return (8, straight_high)
        if counts == [4, 1]:
            return (7, *ordered_ranks)
        if counts == [3, 2]:
            return (6, *ordered_ranks)
        if is_flush:
            return (5, *ranks)
        if is_straight:
            return (4, straight_high)
        if counts == [3, 1, 1]:
            return (3, *ordered_ranks)
        if counts == [2, 2, 1]:
            return (2, *ordered_ranks)
        if counts == [2, 1, 1, 1]:
            return (1, *ordered_ranks)
        return (0, *ranks)

    def _straight_high(self, ranks):
        """
        ranks: list of 5 ints (1-13, Ace=1).
        Returns the high card of the straight (14 for an Ace-high "Broadway"
        straight), or None if the 5 ranks don't form a straight.
        """
        unique = set(ranks)
        if len(unique) != 5:
            return None  # a pair/trips among the 5 rules out a straight

        values = sorted(unique)

        # Standard consecutive run, e.g. 3-4-5-6-7, or the wheel 1-2-3-4-5 (Ace-low)
        if values[-1] - values[0] == 4:
            return values[-1]

        # Ace-high straight: 10, J, Q, K, A (Ace stored as 1)
        if 1 in unique and {10, 11, 12, 13}.issubset(unique):
            return 14

        return None

    @staticmethod
    def _rank(card):
        return int(card.split('_')[1])

    @staticmethod
    def _suit(card):
        return int(card.split('_')[0])