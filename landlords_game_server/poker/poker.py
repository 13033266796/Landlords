import random


class PokerManager(object):
    def __init__(self):
        self.pokers = []
        all_card_type = "xtmf"
        all_card_text = ["2", "A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3"]
        all_card_value = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        for card_type in all_card_type:
            for index, card_text in enumerate(all_card_text):
                self.pokers.append(card_text + " " + card_type + " " + str(all_card_value[index]))
        # 大王
        self.pokers.append("B _ 14")
        # 小王
        self.pokers.append("S _ 13")
        random.shuffle(self.pokers)

    def send_card(self, gamer, num=17):
        for i in range(num):
            gamer.pokers.append(self.pokers.pop())

    def get_three_cards(self):
        if len(self.pokers) == 3:
            return self.pokers


class PokerUtil:
    @classmethod
    def encoder_poker(cls, pokers):
        return ",".join(pokers)

    @classmethod
    def get_pokers_from_data(cls, data):
        return data.split(",")


if __name__ == "__main__":
    poker_manager = PokerManager()
    pass
