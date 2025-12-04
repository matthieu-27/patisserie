#!/usr/bin/env python
#  -*- coding: utf-8 -*-

# la grille de jeu virtuelle est composée de 10 x 10 cases
# une case est identifiée par ses coordonnées, un tuple (no_ligne, no_colonne)
# un no_ligne ou no_colonne est compris dans le programme entre 1 et 10,
# mais pour le joueur une colonne sera identifiée par une lettre (de 'A' à 'J')

GRID_SIZE = 10

# détermination de la liste des lettres utilisées pour identifier les colonnes :
LETTERS = "ABCDEFGHIJ"

# différents états possibles pour une case de la grille de jeu
SEA, MISSED_SHOT, HIT_SHOT, SUNK_SHOT = 0, 1, 2, 3
# représentation du contenu de ces différents états possible pour une case
# (tableau indexé par chacun de ces états)
SQUARE_STATE_REPR = [' ', 'X', '#', '-']

# chaque navire est constitué d'un dictionnaire dont les clés sont les
# coordonnées de chaque case le composant, et les valeurs correspondantes
# l'état de la partie du navire correspondant à la case
# (True : intact ; False : touché)

# les navires suivants sont disposés de façon fixe dans la grille :
#      +---+---+---+---+---+---+---+---+---+---+
#      | A | B | C | D | E | F | G | H | I | J |
#      +---+---+---+---+---+---+---+---+---+---+
#      | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10|
# +----+---+---+---+---+---+---+---+---+---+---+
# |  1 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  2 |   | o | o | o | o | o |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  3 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  4 | o |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  5 | o |   | o |   |   |   |   | o | o | o |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  6 | o |   | o |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  7 | o |   | o |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  8 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# |  9 |   |   |   |   | o | o |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
# | 10 |   |   |   |   |   |   |   |   |   |   |
# +----+---+---+---+---+---+---+---+---+---+---+
aircraft_carrier = {(2, 2): True, (2, 3): True, (2, 4): True, (2, 5): True, (2, 6): True}
cruiser          = {(4, 1): True, (5, 1): True, (6, 1): True, (7, 1): True}
destroyer        = {(5, 3): True, (6, 3): True, (7, 3): True}
submarine        = {(5, 8): True, (5, 9): True, (5, 10): True}
torpedo_boat     = {(9, 5): True, (9, 6): True}
ships_list = [aircraft_carrier, cruiser, destroyer, submarine, torpedo_boat]


def ask_coord():
    """Demande au joueur des coordonnées de la grille de la forme 'A1' ou 'a1' et
       la retourne sous la forme de coordonnées au format du programme :
       ex. : (5, 3) pour 'C5'

    :return: coordonnées au format du programme
    """

    # on demande des coordonnées au joueur tant qu'il n'en fournit pas de valides
    # (ex. : 'A1', 'H8'), puis on les transforme en des coordonnées du programme :
    # tuple (no_ligne, no_colonne)
    valid_coord = False
    shot_coord = None  # pour éviter un avertissement ("can be undefined")

    # ex. d'entrée attendue : 'A1'
    player_coord = input("Entrez les coordonnées de votre tir (ex. : 'A1', 'H8') : ")

    if 2 <= len(player_coord) <= 3:
        letter, number = player_coord[0], player_coord[1:]
        letter = letter.upper()
        try:
            # détermination de line_no et column_no (comptés à partir de 1)
            line_no = int(number)
            column_no = ord(letter) - ord('A') + 1
            if 1 <= line_no <= GRID_SIZE and letter in LETTERS:
                valid_coord = True
                shot_coord = (line_no, column_no)
        except ValueError:
            pass

    if not valid_coord:
        shot_coord = ask_coord()

    return shot_coord


def ship_is_hit(ship, shot_coord):
    """Indique si un navire est touché par un tir aux coordonnées indiquées."""
    return shot_coord in ship


def ship_is_sunk(ship):
    """Indique si un navire est coulé."""
    return not any(ship.values())


def analyze_shot(ship, shot_coord):
    """Analyse les conséquences d'un tir sur un navire :

    - teste si le navire est touché par le tir, le signale et le mémorise alors
    - teste si le navire est ainsi coulé, le signale dans ce cas,
      et le supprime de la flotte

    :param ship: pour lequel on regarde si le tir le concerne
    :param shot_coord:
    :return: booléen indiquant si le navire a été touché par le tir
    """
    is_hit = ship_is_hit(ship, shot_coord)
    if is_hit:
        print('Un navire a été touché par votre tir !')
        ship[shot_coord] = False
        if ship_is_sunk(ship):
            print('Le navire touché est coulé !!')
            # le navire est supprimé de la flotte
            ships_list.remove(ship)

    return is_hit


def grid_square_state(coord):
    """Retourne l'état de la case coord de la grille
       (cf. constantes SEA, MISSED_SHOT, HIT_SHOT, SUNK_SHOT)."""

    if coord in played_shots:
        square_ships = [ship for ship in ships_list if ship_is_hit(ship, coord)]
        if square_ships:
            square_ship = square_ships[0]
            square_state = SUNK_SHOT if ship_is_sunk(square_ship) else HIT_SHOT
        else:
            square_state = MISSED_SHOT
    else:
        square_state = SEA

    return square_state


def display_grid():
    """Affichage de la grille de jeu."""

    print('    ', end='')
    for x in range(GRID_SIZE):
        letter = LETTERS[x]
        print(' {}  '.format(letter), end='')
    print()
    print('  ', '+---' * GRID_SIZE + '+')
    for line_no in range(1, GRID_SIZE + 1):
        print('{:>2} |'.format(line_no), end='')
        for column_no in range(1, GRID_SIZE + 1):
            coord = (line_no, column_no)
            square_state = grid_square_state(coord)
            state_str = SQUARE_STATE_REPR[square_state]
            print(' {} |'.format(state_str), end='')
        print()
        print('  ', '+---' * GRID_SIZE + '+')

# -------------------------------------------------------------------------- #
# programme principal :                                                      #
# tant que tous les navires ne sont pas coulés, on demande au joueur         #
# d'indiquer une case où il souhaite effectuer un tir                        #
# -------------------------------------------------------------------------- #


played_shots = set()  # ensemble des coordonnées des tirs des joueurs
while ships_list:
    display_grid()
    next_shot_coord = ask_coord()
    played_shots.add(next_shot_coord)
    if not any([analyze_shot(ship, next_shot_coord) for ship in ships_list]):
        print("Votre tir est tombé dans l'eau")
    print()

display_grid()
print('Bravo, vous avez coulé tous les navires')
