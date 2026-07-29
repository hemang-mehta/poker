class Evaluator:
    def __init__(self, game):
        self.game = game
        self.ranks = [_ for _ in range(10)]
        
    def evaluate_hands(self):
        pass
    
        # player_cards = [int(c.split('_')[0]) for c in player_cards]
        # table_cards = [int(c.split('_')[0]) for c in table_cards]
        
        # all_cards = []
        # all_cards.extend(player_cards)
        # all_cards.extend(table_cards)
        # all_cards.sort()
    
    # Card structure -> "1_1" == "1 of Spade"
    def is_straight(all_cards):
        for c in range(3):
            temp_count = c
            count = 0
            numbers = []
            while (all_cards[temp_count+1] - all_cards[temp_count]) == 1:
                count += 1
                numbers.append(all_cards[temp_count])
                if count == 5:
                    return 'straight', numbers.sort(reverse=True)
                temp_count += 1
                if temp_count > (len(all_cards) - 1):
                    break
            if count == 5:
                return 'straight', numbers.sort(reverse=True)
        return '', []
            
    def is_flush(all_cards):
        card_suites = [i.split('_')[-1] for i in all_cards]
        
        suite_count = {}
        for s in card_suites:
            if s not in suite_count.keys():
                suite_count[s] = 1
            else:
                suite_count[s] += 1
                if suite_count[s] == 5:
                    return True
        return False

    # Check for 4 of a kind, 3 of kind, 2 pair, full house, 1 pair
    def is_any_kind(all_cards):
        card_count = {}
        for c in all_cards:
            if c not in card_count.keys():
                card_count[c] = 1
            else:
                card_count[c] += 1
        
        type = ""
        numbers = []
        is_three_of_kind_already = False
        is_pair_already = False
        
        for k,v in card_count.items():
            if v == 4:
                type = "4 of a kind"
                numbers = [k]
                break
            elif v == 3:
                if is_pair_already:
                    type = "full house"
                    t = numbers.pop(0)
                    numbers = [v, t]
                    break
                else:
                    type = "3 of a kind"
                    numbers = [k]
                    is_three_of_kind_already = True
            elif v == 2:
                if is_three_of_kind_already:
                    type = "full house"
                    numbers.append(v)
                    break
                elif is_pair_already:
                    type = "2 pair"
                    if v > numbers[0]:
                        numbers.insert(0, v)
                    else:
                        numbers.append(v)
                else:
                    type = "1 pair"
                    numbers = [v]
        
        return type, numbers
        