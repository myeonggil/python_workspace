# Encoding: UTF-8
"""
아래 Unittest 를 완성하시오.
- Python3
"""
import unittest
from unittest import TestCase
from abc import *


class Vegetable:
    def run(self):
        print('Vegetable is running')

class Animal:
    def run(self):
        print('Class Animal is running')

class Cat(Animal):
    def run(self):
        print('Dog is running')

    def get_name(self):
        return 'Mingky'

class Dog(Animal):
    def run(self):
        print('Cat is running')

    def get_name(self):
        return 'Andy'

class Tomato(Vegetable):
    def run(self):
        print('Tomato is running')


class SimpleOOTest(TestCase):

    def test_OOTest(self):
        cat = Cat()
        dog = Dog()
        tomato = Tomato()

        self.assertIsInstance(cat, Animal)
        self.assertIsInstance(dog, Animal)
        self.assertIsInstance(tomato, Vegetable)
        self.assertEqual(self.assertIsInstance(tomato, Animal), False)
        self.assertEqual(cat.get_name(), 'Mingky')
        self.assertEqual(dog.get_name(), 'Andy')


if __name__ == "__main__":
    unittest.main()