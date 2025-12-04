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


class Appareil:
    def __init__(self, name):
        self.name = name
        self.ingredients = []

    def ajouter_ingredient(self, ingredient):
        self.ingredients.append(ingredient)


class Recipient:
    def __init__(self, name:str, contenu=None):
        self.name = name
        self.contenu = contenu


class BatteurOeufs(Commis, threading.Thread):
    def __init__(self, name: str, recipient: Recipient):
        threading.Thread.__init__(self)
        Commis.__init__(self, name)
        self.recipient = recipient

    def run(self):
        if isinstance(self.recipient.contenu, Oeuf):
            nb_oeufs = self.recipient.contenu.quantity
            nb_tours = nb_oeufs * 8
            for num_tour in range(1, nb_tours + 1):
                print(f"{self.name}: Je bats les {nb_oeufs} oeufs dans : {self.recipient.name}, tour n°{num_tour}")
                time.sleep(0.5)


class FondeurChocolat(Commis, threading.Thread):
    def __init__(self, name: str, recipient: Recipient):
        threading.Thread.__init__(self)
        Commis.__init__(self, name)
        self.recipient = recipient

    def run(self):
        if isinstance(self.recipient.contenu, Chocolat):
            quantity = self.recipient.contenu.quantity
            print(f"{self.name}: Je mets de l'eau à chauffer dans une bouilloire")
            time.sleep(8)
            print(f"{self.name}: Je verse l'eau dans une casserole")
            time.sleep(2)
            print(f"{self.name}: J'y pose le {self.recipient.name} rempli de chocolat")
            time.sleep(1)
            nb_tours = math.ceil(quantity / 10)
            for num_tour in range(1, nb_tours + 1):
                print(f"{self.name}: Je mélange {quantity} de chocolat à fondre dans : {self.recipient.name}, tour n°{num_tour}")
                time.sleep(1)


if __name__ == "__main__":
    # Exemple d'utilisation des classes
    cul_de_poule = Recipient("cul de poule", Oeuf(5))
    casserole = Recipient("casserole", Chocolat(200))

    batteur = BatteurOeufs("Batteur", cul_de_poule)
    fondeur = FondeurChocolat("Fondeur", casserole)
    batteur.start()
    fondeur.start()
    batteur.join()
    fondeur.join()
    print("Toutes les tâches sont terminées.")