import unittest
from page import *


class TestHero(unittest.TestCase):
    hero = None

    def test_01_hero_init(self):
        TestHero.hero = Hero(name="Test_name")

        self.assertEqual(self.hero.name, "Test_name")
        self.assertIsInstance(self.hero, Hero)
        self.assertIsNotNone(self.hero.stats)
        self.assertIsNotNone(self.hero.HP)
        self.assertIsNotNone(self.hero.stat_points)
        self.assertIsNotNone(self.hero.attack_range)
        self.assertIsNotNone(self.hero.id_counter)
        self.assertEqual(self.hero.dead, False)

    def getAttack(self, monster_attacking):
        return 10 + randrange(self.attack_range) + self.stats.getByName(hero_modifier[monster_attacking.type])

    def test_02_add_item(self):
        item_str = "Broken Umbrella"
        TestHero.hero.addItem(item_str)

        self.assertIn(item_str, self.hero.items)

    def test_03_upgrade(self):
        previous_value = self.hero.stats.constitution
        skill_dict = {"dexterity": 0, "constitution": 5, "charisma": 0}

        self.hero.upgrade(skill_dict)

        self.assertGreater(skill_dict['constitution'], previous_value)

    def test_04_attack(self):
        monster = Monster(MonsterType.Ghost)
        attack_value = self.hero.getAttack(monster)

        self.assertGreater(attack_value, 0)


if __name__ == "__main__":
    unittest.main()
