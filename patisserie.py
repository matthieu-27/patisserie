import threading
import time
import math

from abc import ABC, abstractmethod
from typing import ClassVar
from dataclasses import dataclass


class CommisHandler(ABC):
    @abstractmethod
    def startup(self) -> None:
        """
        Method that is called before the thread starts.
        Initialize all necessary resources here.
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def shutdown(self) -> None:
        """
        Method that is called shortly after stop() method was called.
        Use it to clean up all resources before thread stops.
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def handle(self) -> None:
        """
        Method that should contain business logic of the thread.
        Will be executed in the loop until stop() method is called.
        Must not block for a long time.
        :return: None
        """
        raise NotImplementedError()


@dataclass
class Ingredient(ABC):
    name: str
    quantity: int
    unit: str

    def _init__(self, _name, _quantity, _unit):
      self.name = _name
      self.quantity = _quantity
      self.unit = _unit


@dataclass
class Appareil(ABC):
    name: str
    ingredients: list[Ingredient]
    result: str

    def _init__(self, _name: str, _ingredients: list[Ingredient], _result: str):
      self.name = _name
      self.ingredients = _ingredients
      self.result = _result


@dataclass
class Recipient:
    name: str
    item: Ingredient | Appareil

    def _init__(self, _name: str, _item: Ingredient | Appareil):
      self.name = _name
      self.item = _item


class Egg(Ingredient):
    def __init__(self, name: str, quantity: int, unit: str):
        super().__init__(name, quantity, unit)

    def process(self):
        ...


class Chocolate(Ingredient):
    def __init__(self, name: str, quantity: int, unit: str):
        super().__init__(name, quantity, unit)

    def process(self):
        ...


class BatteurOeufs(threading.Thread):
    def __init__(self, handler: CommisHandler):
        super().__init__()
        self._handler = handler
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def _stopped(self) -> bool:
        return self._stop_event.is_set()

    def run(self):
        # on suppose qu'il faut 8 tours de batteur par œuf présent dans le bol
        nb_tours = self.nb_oeufs * 8
        for no_tour in range(1, nb_tours + 1):
            print(f"\tJe bats les {self.nb_oeufs} oeufs, tour n°{no_tour}")
            time.sleep(0.5)  # temps supposé d'un tour de batteur



class FondeurChocolat(threading.Thread):
    def __init__(self, handler: CommisHandler):
        super().__init__()
        self._handler = handler
        self._stop_event = threading.Event()

    def run(self):
        print("Je mets de l'eau à chauffer dans une bouilloire")
        time.sleep(8)
        print("Je verse l'eau dans une casserole")
        time.sleep(2)
        print("J'y pose le bol rempli de chocolat")
        time.sleep(1)
        # on suppose qu'il faut 1 tour de spatule par 10 g. de chocolat
        # présent dans le bol pour faire fondre le chocolat
        nb_tours = math.ceil(self.quantite / 10)
        for no_tour in range(1, nb_tours + 1):
            print(f"Je mélange {self.quantite} de chocolat à fondre, tour n°{no_tour}")
            time.sleep(1)  # temps supposé d'un tour de spatule




if __name__ == "__main__":
    batteur = BatteurOeufs(6)
    fondeur = FondeurChocolat(200)
    batteur.start()
    fondeur.start()
    batteur.join()
    fondeur.join()
    print("\nJe peux à présent incorporer le chocolat aux oeufs")
