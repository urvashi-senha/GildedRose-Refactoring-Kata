# -*- coding: utf-8 -*-

class ItemUpdator:
    MAX_QUALITY = 50
    MIN_QUALITY = 0

    def update(self, item):
        raise NotImplementedError("to be defined in sub classes")

    def decrease_quality(self, item, amount=1):
        item.quality = max(self.MIN_QUALITY, item.quality - amount)

    def increase_quality(self, item, amount=1):
        item.quality = min(self.MAX_QUALITY, item.quality + amount)

    def decrease_sell_in(self, item):
            item.sell_in -= 1

class AgedBrieUpdator(ItemUpdator):

    def update(self, item):
         self.decrease_sell_in(item)
         self.increase_quality(item)
         if item.sell_in < 0:
            self.increase_quality(item)


class BackstagePassUpdator(ItemUpdator):

    BACKSTAGE_10_DAYS = 10
    BACKSTAGE_5_DAYS = 5

    def update(self, item):
        if item.sell_in <= 0:
            item.quality = self.MIN_QUALITY
        else:
            self.increase_quality(item)
            if item.sell_in <= self.BACKSTAGE_10_DAYS:
                self.increase_quality(item)
            if item.sell_in <= self.BACKSTAGE_5_DAYS:
                self.increase_quality(item)

        self.decrease_sell_in(item)

class NormalItemUpdator(ItemUpdator):
    def update(self, item):
        self.decrease_sell_in(item)
        self.decrease_quality(item)
        if item.sell_in < 0:
            self.decrease_quality(item)


class ConjuredItemUpdator(ItemUpdator):
    def update(self, item):
        self.decrease_sell_in(item)
        self.decrease_quality(item, amount=2)
        if item.sell_in < 0:
            self.decrease_quality(item, amount=2)

class SulphurasItemUpdator(ItemUpdator):
    SULFURAS_QUALITY = 80
    def update(self, item):
        self.quality = self.SULFURAS_QUALITY

class ItemUpdatorFactory:
    
    AGED_BRIE = "Aged Brie"
    BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    CONJURED = "Conjured Mana Cake"

    @staticmethod
    def get_updator(item):
        if item.name == ItemUpdatorFactory.AGED_BRIE:
            return AgedBrieUpdator()
        elif item.name == ItemUpdatorFactory.BACKSTAGE:
            return BackstagePassUpdator()
        elif  item.name == ItemUpdatorFactory.CONJURED:
            return ConjuredItemUpdator()
        elif item.name == ItemUpdatorFactory.SULFURAS:
            return SulphurasItemUpdator()
        else:
            return NormalItemUpdator()



class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updator = ItemUpdatorFactory.get_updator(item)
            updator.update(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)