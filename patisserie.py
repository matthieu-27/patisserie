import threading
import time
import math
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

class Commis(ABC):
    name: str
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self):
        ...

class ThreadHandler(ABC):
    @abstractmethod
    def startup(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def shutdown(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def handle(self) -> None:
        raise NotImplementedError()

@dataclass
class Ingredient(ABC):
    name: str
    quantity: int
    unit: str

    def __init__(self, _name: str, _quantity: int, _unit: str):
        self.name = _name
        self.quantity = _quantity
        self.unit = _unit

@dataclass
class Appareil(ABC):
    name: str
    ingredients: list[Ingredient]
    result: str

    def __init__(self, _name: str, _ingredients: list[Ingredient], _result: str):
        self.name = _name
        self.ingredients = _ingredients
        self.result = _result

@dataclass
class Recipient:
    name: str
    item: Optional[Ingredient | Appareil] = None

    def __post_init__(self) -> None:
        if self.item is None:
            self.item = None

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

class FondeurChocolat(threading.Thread):
    def __init__(self, name: str, quantite: int):
        super().__init__()
        self.name = name
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

class CookingThread(threading.Thread):
    def __init__(self, handler: ThreadHandler):
        threading.Thread.__init__(self)
        self._handler = handler
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def _stopped(self) -> bool:
        return self._stop_event.is_set()

    def run(self) -> None:
        self._handler.startup()
        while not self._stopped():
            self._handler.handle()
        self._handler.shutdown()

@dataclass
class BatteurOeufs(ThreadHandler):
    name: str
    _eggs: int

    def __init__(self, name: str, eggs: int):
        self.name = name
        self._eggs = eggs

    def startup(self) -> None:
        logging.info("BatteurOeufs started")

    def shutdown(self) -> None:
        logging.info("BatteurOeufs stopped")

    def handle(self) -> None:
        nb_tours = self._eggs * 8
        for no_tour in range(1, nb_tours + 1):
            print(f"{self.name}: Je bats les {self._eggs} oeufs, tour n°{no_tour}")
            time.sleep(0.5)

if __name__ == "__main__":
    batteur = BatteurOeufs("Batteur", 5)
    commis_thread = CookingThread(batteur)
    commis_thread.start()
    commis_thread.join()
