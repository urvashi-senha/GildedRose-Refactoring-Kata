# -*- coding: utf-8 -*-


class GildedRose(object):
    # Item types
    AGED_BRIE = "Aged Brie"
    BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    CONJURED = "Conjured Mana Cake"

    # Business rules
    MAX_QUALITY = 50
    MIN_QUALITY = 0
    BACKSTAGE_10_DAYS = 10
    BACKSTAGE_5_DAYS = 5
    SULFURAS_QUALITY = 80

    def __init__(self, items):
        self.items = items

    def is_aged_brie(self, item):
        return item.name == self.AGED_BRIE

    def is_backstage_pass(self, item):
        return item.name == self.BACKSTAGE

    def is_sulfuras(self, item):
        return item.name == self.SULFURAS

    def is_conjured(self, item):
        return item.name == self.CONJURED

    def decrease_quality(self, item, amount=1):
        item.quality = max(self.MIN_QUALITY, item.quality - amount)

    def increase_quality(self, item, amount=1):
        item.quality = min(self.MAX_QUALITY, item.quality + amount)

    def decrease_sell_in(self, item):
        if not self.is_sulfuras(item):
            item.sell_in -= 1

    def update_normal(self, item):
        self.decrease_quality(item)

    def update_aged_brie(self, item):
        self.increase_quality(item)

    def update_backstage(self, item):
        self.increase_quality(item)

        if item.sell_in <= self.BACKSTAGE_10_DAYS:
            self.increase_quality(item)

        if item.sell_in <= self.BACKSTAGE_5_DAYS:
            self.increase_quality(item)

    def update_conjured(self, item):
        self.decrease_quality(item, amount=2)

    def update_expired_item(self, item):
        if self.is_aged_brie(item):
            self.increase_quality(item)
        elif self.is_backstage_pass(item):
            item.quality = self.MIN_QUALITY
        elif self.is_conjured(item):
            self.decrease_quality(item, amount=2)
        else:
            self.decrease_quality(item)

    # Design note:
    # Item behavior is currently dispatched with conditionals for simplicity and readability.
    # In a larger system with many item types, this could be refactored into a factory that
    # returns a dedicated updater per item (Strategy pattern), allowing new item behaviors
    # to be added without modifying GildedRose.
    def update_item(self, item):
        if self.is_sulfuras(item):
            # Sulfuras is a legendary item:
            # quality always 80 and sell_in never changes
            item.quality = self.SULFURAS_QUALITY
            return

        if self.is_aged_brie(item):
            self.update_aged_brie(item)
        elif self.is_backstage_pass(item):
            self.update_backstage(item)
        elif self.is_conjured(item):
            self.update_conjured(item)
        else:
            self.update_normal(item)

        self.decrease_sell_in(item)

        if item.sell_in < 0:
            self.update_expired_item(item)

    def update_quality(self):
        for item in self.items:
            self.update_item(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)