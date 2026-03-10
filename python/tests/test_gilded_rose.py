# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def update_one_item(self, name, sell_in, quality):
        item = Item(name, sell_in, quality)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        return item

    # Normal items
    def test_normal_item_degrades_by_1_before_sell_date(self):
        item = self.update_one_item("foo", 10, 20)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(19, item.quality)

    def test_normal_item_degrades_by_2_after_sell_date(self):
        item = self.update_one_item("foo", 0, 20)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(18, item.quality)

    def test_normal_item_quality_never_negative(self):
        item = self.update_one_item("foo", 5, 0)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(0, item.quality)

    # Aged Brie
    def test_aged_brie_increases_by_1_before_sell_date(self):
        item = self.update_one_item("Aged Brie", 10, 20)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(21, item.quality)

    def test_aged_brie_increases_by_2_after_sell_date(self):
        item = self.update_one_item("Aged Brie", 0, 20)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(22, item.quality)

    def test_aged_brie_never_above_50(self):
        item = self.update_one_item("Aged Brie", 5, 50)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(50, item.quality)
    
    def test_aged_brie_at_49_after_sell_date_caps_at_50(self):
        item = self.update_one_item("Aged Brie", 0, 49)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(50, item.quality)

    # Backstage passes
    def test_backstage_passes_increase_by_1_when_sell_in_greater_than_10(self):
        item = self.update_one_item("Backstage passes to a TAFKAL80ETC concert", 11, 20)
        self.assertEqual(10, item.sell_in)
        self.assertEqual(21, item.quality)

    def test_backstage_passes_increase_by_2_when_sell_in_10_or_less(self):
        item = self.update_one_item("Backstage passes to a TAFKAL80ETC concert", 10, 20)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(22, item.quality)

    def test_backstage_passes_increase_by_3_when_sell_in_5_or_less(self):
        item = self.update_one_item("Backstage passes to a TAFKAL80ETC concert", 5, 20)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(23, item.quality)

    def test_backstage_passes_drop_to_0_after_concert(self):
        item = self.update_one_item("Backstage passes to a TAFKAL80ETC concert", 0, 20)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_backstage_passes_never_above_50(self):
        item = self.update_one_item("Backstage passes to a TAFKAL80ETC concert", 5, 49)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(50, item.quality)
    
    def test_backstage_passes_at_50_do_not_exceed_50_when_sell_in_10(self):
        item = self.update_one_item("Backstage passes to a TAFKAL80ETC concert", 10, 50)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_backstage_passes_at_49_with_sell_in_10_caps_at_50_not_51(self):
        item = self.update_one_item("Backstage passes to a TAFKAL80ETC concert", 10, 49)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(50, item.quality)

    def test_backstage_passes_increase_by_3_when_sell_in_is_1_caps_at_50(self):
        item = self.update_one_item("Backstage passes to a TAFKAL80ETC concert", 1, 49)
        self.assertEqual(0, item.sell_in)
        self.assertEqual(50, item.quality)

    # Sulfuras
    def test_sulfuras_never_changes(self):
        item = self.update_one_item("Sulfuras, Hand of Ragnaros", 0, 80)
        self.assertEqual(0, item.sell_in)
        self.assertEqual(80, item.quality)

    # Conjured
    def test_conjured_degrades_by_2_before_sell_date(self):
        item = self.update_one_item("Conjured Mana Cake", 10, 20)
        self.assertEqual(9, item.sell_in)
        self.assertEqual(18, item.quality)

    def test_conjured_degrades_by_4_after_sell_date(self):
        item = self.update_one_item("Conjured Mana Cake", 0, 20)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(16, item.quality)

    def test_conjured_quality_never_negative(self):
        item = self.update_one_item("Conjured Mana Cake", 0, 3)
        self.assertEqual(-1, item.sell_in)
        self.assertEqual(0, item.quality)

    def test_conjured_degrades_by_2_before_sell_date_but_not_below_zero(self):
        item = self.update_one_item("Conjured Mana Cake", 5, 1)
        self.assertEqual(4, item.sell_in)
        self.assertEqual(0, item.quality)

if __name__ == '__main__':
    unittest.main()