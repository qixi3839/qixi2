import random

class BlackjackGame:
    def __init__(self):
        self.players = {}

    def _create_deck(self):
        deck = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        random.shuffle(deck)
        return deck

    def _deal_card(self):
        if not hasattr(self, 'deck') or not self.deck:
            self.deck = self._create_deck()
        return self.deck.pop()

    def _calculate_points(self, cards):
        total = 0
        aces = 0
        for card in cards:
            if card in ['J', 'Q', 'K']:
                total += 10
            elif card == 'A':
                total += 11
                aces += 1
            else:
                total += int(card)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def _format_cards(self, cards):
        emoji_map = {'A': '🃏A', 'J': '🃏J', 'Q': '🃏Q', 'K': '🃏K'}
        return ' '.join([emoji_map.get(c, f"🃏{c}") for c in cards])

    def add_player(self, user_id, name):
        if user_id not in self.players:
            self.players[user_id] = {
                'name': name,
                'cards': [self._deal_card(), self._deal_card()],
                'stopped': False
            }
            cards = self.players[user_id]['cards']
            return f"{name} 加入了游戏。\n初始牌：{self._format_cards(cards)} 点数：{self._calculate_points(cards)}"
        else:
            return f"{name} 已经在游戏中。"

    def player_hit(self, user_id):
        if user_id in self.players and not self.players[user_id]["stopped"]:
            self.players[user_id]["cards"].append(self._deal_card())
            cards = self.players[user_id]["cards"]
            points = self._calculate_points(cards)
            if points > 21:
                return f"💥 爆牌了！{self.players[user_id]['name']} 的牌：{self._format_cards(cards)} 点数：{points}"
            else:
                return f"{self.players[user_id]['name']} 要了一张牌：{self._format_cards(cards)} 点数：{points}"
        return "你不能再要牌了。"

    def player_stand(self, user_id):
        if user_id in self.players:
            self.players[user_id]["stopped"] = True
            return f"{self.players[user_id]['name']} 选择停牌。"
        return "你还没加入游戏。"
