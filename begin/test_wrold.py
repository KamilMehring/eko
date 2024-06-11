import unittest
from Position import Position
from Organisms.Sheep import Sheep
from Organisms.Lynx import Lynx
from Organisms.Antelope import Antelope
from Organisms.Grass import Grass
from World import World

class TestWorld(unittest.TestCase):

    def setUp(self):
        # Konfiguracja przed każdym testem - utworzenie obiektu World z wymiarami 5x5
        self.world = World(5, 5)

    def test_activate_plague(self):
        # Test aktywacji plagi
        self.world.activatePlague()
        # Sprawdzenie, czy plaga została aktywowana
        self.assertTrue(self.world._World__plagueActive)
        # Sprawdzenie, czy liczba pozostałych tur plagi wynosi 2
        self.assertEqual(self.world._World__plagueTurnsRemaining, 2)

    def test_apply_plague(self):
        # Dodanie organizmów do świata
        self.world.addOrganism(Sheep(position=Position(xPosition=1, yPosition=1), world=self.world))
        self.world.addOrganism(Lynx(position=Position(xPosition=2, yPosition=2), world=self.world))
        self.world.addOrganism(Antelope(position=Position(xPosition=3, yPosition=3), world=self.world))
        # Aktywowanie plagi
        self.world.activatePlague()
        # Ustawienie początkowej długości życia organizmów
        for organism in self.world.organisms:
            organism.liveLength = 8
        # Zastosowanie plagi
        self.world.applyPlague()
        # Sprawdzenie, czy długość życia każdego organizmu została zmniejszona o połowę
        for organism in self.world.organisms:
            self.assertEqual(organism.liveLength, 4)
        # Sprawdzenie, czy liczba pozostałych tur plagi wynosi 1
        self.assertEqual(self.world._World__plagueTurnsRemaining, 1)

    def test_add_organism_from_user(self):
        # Dodanie organizmów przez użytkownika i sprawdzenie, czy została poprawnie dodana
        self.world.addOrganismFromUser('Sheep', 2, 2)
        self.assertIsInstance(self.world.getOrganismFromPosition(Position(xPosition=2, yPosition=2)), Sheep)
        self.world.addOrganismFromUser('Lynx', 3, 3)
        self.assertIsInstance(self.world.getOrganismFromPosition(Position(xPosition=3, yPosition=3)), Lynx)
        self.world.addOrganismFromUser('Antelope', 4, 4)
        self.assertIsInstance(self.world.getOrganismFromPosition(Position(xPosition=4, yPosition=4)), Antelope)
        self.world.addOrganismFromUser('Grass', 1, 1)
        self.assertIsInstance(self.world.getOrganismFromPosition(Position(xPosition=1, yPosition=1)), Grass)
        self.world.addOrganismFromUser('Sheep', 5, 5)
        self.assertIsNone(self.world.getOrganismFromPosition(Position(xPosition=5, yPosition=5)))

    def test_enforce_nature_protection_rules(self):
        # Dodanie kilku owiec do świata
        for _ in range(3):
            self.world.addOrganism(Sheep(position=self.world.getRandomFreePosition(), world=self.world))
        # Dodanie kilku rysi do świata
        for _ in range(3):
            self.world.addOrganism(Lynx(position=self.world.getRandomFreePosition(), world=self.world))
        # Egzekwowanie zasad ochrony przyrody
        self.world.enforceNatureProtectionRules()
        # Zliczenie liczby owiec
        sheep_count = sum(1 for org in self.world.organisms if isinstance(org, Sheep))
        # Zliczenie liczby rysi
        lynx_count = sum(1 for org in self.world.organisms if isinstance(org, Lynx))
        # Sprawdzenie, czy populacja owiec została zredukowana
        self.assertLessEqual(sheep_count, int(0.5 * len(self.world.organisms)))
        # Sprawdzenie, czy populacja rysi jest zgodna z minimalną populacją
        self.assertGreaterEqual(lynx_count, 2)

    def test_repopulate_species(self):
        # Wymuszenie uzupełnienia populacji rysi do 2
        self.world.repopulateSpecies('Lynx', 2)
        # Zliczenie liczby rysi
        lynx_count = sum(1 for org in self.world.organisms if isinstance(org, Lynx))
        # Sprawdzenie, czy liczba rysi wynosi 2
        self.assertEqual(lynx_count, 2)

    def test_reduce_species(self):
        # Dodanie kilku owiec do świata
        for _ in range(5):
            self.world.addOrganism(Sheep(position=self.world.getRandomFreePosition(), world=self.world))
        # Początkowa liczba owiec
        initial_sheep_count = sum(1 for org in self.world.organisms if isinstance(org, Sheep))
        # Zmniejszenie populacji owiec o 3
        self.world.reduceSpecies('Sheep', 3)
        # Liczba owiec po redukcji
        reduced_sheep_count = sum(1 for org in self.world.organisms if isinstance(org, Sheep))
        # Sprawdzenie, czy liczba owiec została zmniejszona o 3
        self.assertEqual(initial_sheep_count - 3, reduced_sheep_count)

if __name__ == '__main__':
    unittest.main()
