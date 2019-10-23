class Gamer:
    def __init__(self):
        self.pokers = []
        self.rule = None

    def set_rule(self, rule):
        self.rule = rule

    def remove_pokers(self, pokers):
        for poker in pokers:
            self.pokers.remove(poker)
