# -*- coding: utf-8 -*-

class GildedRose(object):

    AGED_BRIE = "Aged Brie"
    BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    CONJURED = "Conjured Mana Cake"

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
        item.quality = max(0, item.quality - amount)

    def increase_quality(self, item, amount=1):
        item.quality = min(50, item.quality + amount)

    def decrease_sell_in(self, item):
        if not self.is_sulfuras(item):
            item.sell_in -= 1

    def update_quality(self):
        for item in self.items:
            if not self.is_aged_brie(item) and not self.is_backstage_pass(item):
                if item.quality > 0:
                    if not self.is_sulfuras(item):
                        self.decrease_quality(item)
            else:
                if item.quality < 50:
                    self.increase_quality(item)
                    if self.is_backstage_pass(item):
                        if item.sell_in < 11:
                            if item.quality < 50:
                                self.increase_quality(item)
                        if item.sell_in < 6:
                            if item.quality < 50:
                                self.increase_quality(item)
         
            self.decrease_sell_in(item)
            
            if item.sell_in < 0:
                if not self.is_aged_brie(item):
                    if not self.is_backstage_pass(item):
                        if item.quality > 0:
                            if not self.is_sulfuras(item):
                                self.decrease_quality(item)
                    else:
                        item.quality = 0
                else:
                    if item.quality < 50:
                        self.increase_quality(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
