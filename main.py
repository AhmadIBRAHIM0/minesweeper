"""Module providingFunction printing python version."""
import sys
from abc import ABC
import random


class Grid:
    """Class grid"""

    def __init__(self, height, width, excluded_tile=None):
        self.width = width
        self.height = height
        self.excluded_tile = excluded_tile
        self.remaining = height * width
        self._tiles = [[TileHint(self, i, j) for j in range(width)] for i in range(height)]

    def _mines_coord(self):
        coord = [(i, j) for i in range(self.height) for j in range(self.width)]
        if self.excluded_tile is not None:
            coord.remove(self.excluded_tile)
        mines_count = int(len(coord) * 0.1)
        return random.sample(coord, mines_count)

    def place_mines(self):
        """def place_mines"""
        mines_coord = self._mines_coord()
        for coord in mines_coord:
            self.remaining -= 1
            i, j = coord
            self._tiles[i][j] = TileMine(self, i, j)

    def get_tile(self, i, j):
        """"Get tile exo3"""
        if i < 0 or i >= self.width or j < 0 or j >= self.height:
            return None
        return self._tiles[i][j]

    def __str__(self):
        _s = ""
        for row in self._tiles:
            _s += " ".join(str(t) for t in row)
            _s += "\n"
        return _s

    def open(self, _i, _j):
        """def open"""
        if _i < 0 or _i >= self.width or _j < 0 or _j >= self.height:
            return Exception("Coordonées invalides")
        self._open_full(_i, _j)
        return True

    def toggle_flag(self, _i, _j):
        """def toggle_flag ex4"""
        if _i < 0 or _i >= self.width or _j < 0 or _j >= self.height:
            return None
        if self._tiles[_i][_j].is_open:
            raise Exception("La case est déjà ouverte")
        self._tiles[_i][_j].is_flagged = not self._tiles[_i][_j].is_flagged
        return True

    def _open_full(self, _i, _j):
        if _i < 0 or _i >= self.width or _j < 0 or _j >= self.height:
            return Exception("Coordonées invalides")
        tile = self._tiles[_i][_j]
        if not tile.is_open:
            tile.open()
        return True


class Tile(ABC):
    """"Class Tile exo3"""

    def __init__(self, _grid, _x, _y):
        self._grid = _grid
        self._x = _x
        self._y = _y
        self.is_open = False
        self.is_flagged = False

    def __str__(self):
        if self.is_flagged:
            return "F"
        if not self.is_open:
            return "#"
        raise NotImplementedError

    def open(self):
        """exo 4"""
        self.is_open = True


class TileMine(Tile):
    """Class TileMine """

    def __str__(self):
        if self.is_flagged:
            return "F"
        if not self.is_open:
            return "#"
        return "O"


class TileHint(Tile):
    """Class TileHint"""

    def __init__(self, grid, i, j):
        super().__init__(grid, i, j)
        self._hint = None

    def __str__(self):
        if self.is_flagged:
            return "F"
        if not self.is_open:
            return "#"
        return str(self.hint) if self.hint else " "

    @property
    def hint(self):
        """def hint"""
        if self._hint is None:
            self._hint = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not i and not j:
                        continue
                    tile = self._grid.get_tile(self._x + i, self._y + j)
                    if isinstance(tile, TileMine):
                        self._hint += 1
        return self._hint

    def open(self):
        super().open()
        if not self.hint:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not i and not j:
                        continue
                    self._grid._open_full(self._x + i, self._y + j)


class MineSweeper:
    """Class MineSweeper"""

    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.is_playing = False
        self.grid = Grid(height, width)  # Create a new Grid object
        self.grid.place_mines()
        self.remaining = self.grid.remaining
        self.mine_found = False

    def open(self, _x, _y):
        """def open"""
        if not self.is_playing:
            raise Exception("La Partie est terminée !")
        if _x < 0 or _x >= self.width or _y < 0 or _y >= self.height:
            raise Exception("Coordonnées hors grille")

        self.grid.open(_x, _y)
        if str(self.grid.get_tile(_x, _y)) == "O":
            self.mine_found = True
            print("Perdu! Vous etes tomber sur une mine.")
        else:
            self.remaining -= 1
            print("Ouvrir la case " + str(_x) + ", " + str(_y))

        if self.is_win():
            self.is_playing = False
        if self.is_lost():
            self.is_playing = False

    def flag(self, _x, _y):
        """def flag"""
        if not self.is_playing:
            raise Exception("Aucune partie en cours !")
        if _x < 0 or _x >= self.width or _y < 0 or _y >= self.height:
            print("Coordonnées incorrectes ! Veuillez réessayer.")
            return
        self.grid.toggle_flag(_x, _y)
        print("Flag la case " + str(_x) + ", " + str(_y))

    def show(self):
        """def show"""
        if not self.is_playing:
            raise Exception("La partie est terminée")
        print(str(self.grid))

    def new_game(self, excluded_tile=None):
        """def new game"""
        self.grid = Grid(self.height, self.width, excluded_tile)
        self.grid.place_mines()
        self.is_playing = True

    def is_win(self):
        """exo 4"""
        if not self.remaining:
            return True
        return False

    def is_lost(self):
        """exo 4."""
        if self.mine_found:
            return True
        return False


def main():
    """def main"""
    finished_game = False
    if len(sys.argv) < 3:
        print("Usage: python main.py HEIGHT WIDTH")
        sys.exit(1)

    height = int(sys.argv[1])
    width = int(sys.argv[2])

    game = MineSweeper(height, width)
    game.new_game()
    while not finished_game:
        game.show()
        print("Nombre de case restante: " + str(game.remaining))
        choice = input("Entrez votre choix sous la forme "
                       "( O/F x y) O pour ouvrir, F pour flagger : ")
        choice = choice.split()

        if not len(choice) in {1, 3}:
            print("incorrect. Veuillez réessayer.")
            continue

        if choice[0] == "newgame":
            game.new_game()

        elif choice[0] == "quit":
            print("quit")
            sys.exit(1)

        elif choice[0] == "O":
            _x = int(choice[1])
            _y = int(choice[2])
            game.open(_x, _y)

        elif choice[0] == "F":
            _x = int(choice[1])
            _y = int(choice[2])
            game.flag(_x, _y)

        else:
            print("Action inconnue, réessayer.")
            continue


if __name__ == "__main__":
    main()
