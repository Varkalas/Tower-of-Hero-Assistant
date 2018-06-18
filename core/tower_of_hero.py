from core.constants import GAME_ITEMS, CUMULATIVE_STATS, MATH_NOTATION


class Item:
    def __init__(self, name, image, tier, importance, level=0):
        self.name = name
        self.image = image
        self.tier = tier
        self.importance = importance
        self.level = level

    def set_name(self, name):
        self.name = name

    def set_level(self, level):
        self.level = level


class Records:
    def __init__(self, name):
        self.name = name
        # self.cumulative_coins =
        self.items = list()

    def initialize_default_items(self):
        for an_item in GAME_ITEMS:
            self.items.append(Item(an_item[0], an_item[1], an_item[2], an_item[3]))

    def set_item_level(self, name, level):
        for an_item in self.items:
            if name == an_item.name:
                an_item.level = level
