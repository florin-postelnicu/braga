import unittest

from braga.models import Entity, Component, Assemblage


class Alive(Component):

    def __init__(self, alive=True):
        self._alive = alive

    @property
    def alive(self):
        return self._alive

    def die(self):
        self._alive = False

    def resurrect(self):
        self._alive = True


class Portable(Component):

    @property
    def is_portable(self):
        return True


class Container(Component):

    def __init__(self, inventory=None):
        self._inventory = set()
        if inventory:
            self._inventory |= inventory

    @property
    def inventory(self):
        return self._inventory

    def pick_up(self, thing):
<<<<<<< HEAD
        if hasattr(thing, 'is_portable'):
=======
        if hasattr(thing, 'portable'):
>>>>>>> 0a269f3d52d73535e3ae9370389d997f35a35264
            self._inventory.add(thing)

    def put_down(self, thing):
        self._inventory.remove(thing)


class TestAssemblage(unittest.TestCase):

    def setUp(self):
        self.human = Entity()
        self.human.components.add(Container())

        self.food = Entity()
        self.food.components.add(Portable())

    def test_assemblage_makes_entity(self):
        cat_factory = Assemblage()
        cat_factory.add_component(Alive)
        cat_factory.add_component(Portable)

        cat = cat_factory.make()

        self.assertTrue(isinstance(cat, Entity))
        self.assertTrue(cat.alive)
        self.assertTrue(cat.is_portable)

    def test_assembled_entity_interacts_normally(self):
        cat_factory = Assemblage()
        cat_factory.add_component(Alive)
        cat_factory.add_component(Portable)
        cat_factory.add_component(Container)

        cat = cat_factory.make()

        # pick up cat
        self.human.pick_up(cat)
        self.assertIn(cat, self.human.inventory)

        # feed cat
        cat.pick_up(self.food)
        self.assertIn(self.food, cat.inventory)

    def test_assembling_entity_with_initial_conditions(self):
        zombie_cat_factory = Assemblage()
        zombie_cat_factory.add_component(Alive, init_args=False)

        zombie_cat = zombie_cat_factory.make()
        self.assertFalse(zombie_cat.alive)
        zombie_cat.resurrect()
        self.assertTrue(zombie_cat.alive)

        fed_cat_factory = Assemblage()
        fed_cat_factory.add_component(Container, init_args=set([self.food]))

        fed_cat = fed_cat_factory.make()
        self.assertIn(self.food, fed_cat.inventory)

    def test_assembled_cats_are_independent(self):
        cat_factory = Assemblage()
        cat_factory.add_component(Alive)
        cat_factory.add_component(Portable)

        my_cat = cat_factory.make()
        stray_cat = cat_factory.make()
        self.human.pick_up(my_cat)

        self.assertIn(my_cat, self.human.inventory)
        self.assertNotIn(stray_cat, self.human.inventory)