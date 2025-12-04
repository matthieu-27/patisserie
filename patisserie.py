import threading
import time
import math
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Commis(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self):
        pass


class Ingredient(ABC):
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit


class Oeuf(Ingredient):
    def __init__(self, quantity):
        super().__init__("Oeuf", quantity, "unité")


class Chocolat(Ingredient):
    def __init__(self, quantity):
        super().__init__("Chocolat", quantity, "grammes")


@dataclass
class Appareil:
    name: str

    def __init__(self, name):
        self.name = name
        self.ingredients = []

    def __str__(self):
        print(f"Je lance la préparation de {self.name}")

    def ajouter_ingredient(self, ingredient):
        self.ingredients.append(ingredient)


class BatteurOeufs(Commis, threading.Thread):
    def __init__(self, name, nb_oeufs):
        threading.Thread.__init__(self)
        Commis.__init__(self, name)
        self.nb_oeufs = nb_oeufs

    def run(self):
        nb_tours = self.nb_oeufs * 8
        for no_tour in range(1, nb_tours + 1):
            print(f"{self.name}: Je bats les {self.nb_oeufs} oeufs, tour n°{no_tour}")
            time.sleep(0.5)


class FondeurChocolat(Commis, threading.Thread):
    def __init__(self, name, quantite):
        threading.Thread.__init__(self)
        Commis.__init__(self, name)
        self.quantite = quantite

    def run(self):
        print(f"{self.name}: Je mets de l'eau à chauffer dans une bouilloire")
        time.sleep(8)
        print(f"{self.name}: Je verse l'eau dans une casserole")
        time.sleep(2)
        print(f"{self.name}: J'y pose le bol rempli de chocolat")
        time.sleep(1)
        nb_tours = math.ceil(self.quantite / 10)
        for no_tour in range(1, nb_tours + 1):
            print(f"{self.name}: Je mélange {self.quantite} de chocolat à fondre, tour n°{no_tour}")
            time.sleep(1)


if __name__ == "__main__":
    # Exemple d'utilisation de la classe Appareil
    appareil = Appareil("Pâte à gâteau")
    appareil.__str__()
    appareil.ajouter_ingredient(Oeuf(5))
    appareil.ajouter_ingredient(Chocolat(200))

    batteur = BatteurOeufs("Batteur", 5)
    fondeur = FondeurChocolat("Fondeur", 200)
    batteur.start()
    fondeur.start()
    batteur.join()
    fondeur.join()
    print("Toutes les tâches sont terminées.")
