from symbol import SudokuSymbol
import time
from typing import Union

EXAMPLE_FIELD_STRING = "5&3&0_1_2_3&0_4_5_6&7&0_7_8_9&0&0&0%6&0&0&1&9&5&0&0&0%0&9&8&0&0&0&0&6&0%8&0&0&0&6&0&0&0&3%4&0" \
                       "&0&8&0&3&0&0&1%7&0&0&0&2&0&0&0&6%0&6&0&0&0&0&2&8&0%0&0&0&4&1&9&0&0&5%0&0&0&0&8&0&0&7&9"
STANDARD_RULES = {"horizontal": True, "vertical": True, "boxes": False}


class Sudoku:
    def __init__(self, size: Union[int, list[int], tuple[int, int]] = (9, 9), field_string: Union[None, str] = None,
                 field: Union[None, list[list[SudokuSymbol]]] = None,
                 rules: dict[str, Union[bool, list[list[tuple[int, int]]]]] = STANDARD_RULES,
                 all_symbols: Union[list[int], list[str]] = None) -> None:
        try:
            size: int = int(size)
            self.__rows: int = size
            self.__cols: int = size
        except TypeError:
            try:
                self.__rows: int = int(size[0])
                self.__cols: int = int(size[1])
            except (ValueError, TypeError):
                raise ValueError("Size specified can't be converted to a 2D field")

        if all_symbols is None:
            all_symbols = range(1, max(self.__rows, self.__cols) + 1)
        self.__all_symbols: list[str] = [str(symbol) for symbol in all_symbols]
        i = 0
        while str(i) in self.__all_symbols:
            i += 1
        self.__no_symbol: str = str(i)

        if field is not None:
            self.__field = field
        else:
            self.__field: list[list[SudokuSymbol]] = []

            if field_string is not None:
                self.__set_field(field_string)
            else:
                self.__set_empty()

        self.__rules = rules

    def __set_empty(self):
        self.__field = [[SudokuSymbol(self.__all_symbols, self.__no_symbol) for _ in range(self.__cols)]
                        for _ in range(self.__rows)]

    def __set_field(self, field_string):
        # assert if size matches (and field_string is rectangular)
        assert field_string.count("%") + 1 == self.__rows, ("The row number in the input field is different from the"
                                                            " row number specified")
        for row in field_string.split("%"):
            assert row.count("&") + 1 == self.__cols, ("At least one column number in the input field is different from"
                                                       " the column number specified")
        # store field_string in self.field (as nested list)
        field_rows: list[str] = field_string.split("%")  # split rows
        field_cols: list[list[str]] = []
        for i in range(self.__rows):
            field_cols.append(field_rows[i].split("&"))
        self.__field = [[SudokuSymbol(self.__all_symbols, field_cols[i][j])
                         for j in range(self.__cols)] for i in range(self.__rows)]
        print(self.__field)

    def __check_square_empty(self, x: int, y: int) -> bool:
        if self.__field[x][y].is_empty():
            return True
        return False

    def __check_square(self, x: int, y: int, symbol: str) -> bool:
        if not self.__check_square_empty(x, y):  # check if square is empty
            return False
        if str(symbol) not in self.__all_symbols:  # check if symbol is one of the allowed symbols
            return False
        for rule, enabled in self.__rules.items():  # check all rules
            if rule == "horizontal" and enabled:
                for i in range(self.__cols):
                    if repr(self.__field[i][y]) == repr(SudokuSymbol(self.__all_symbols, symbol)):
                        return False
            elif rule == "vertical" and enabled:
                for j in range(self.__rows):
                    if repr(self.__field[x][j]) == repr(SudokuSymbol(self.__all_symbols, symbol)):
                        return False
            elif rule == "boxes":
                if enabled is True and self.__rows == self.__cols == 9:
                    for i in range(3 * (x // 3), 3 * (x // 3 + 1)):
                        for j in range(3 * (y // 3), 3 * (y // 3 + 1)):
                            if repr(self.__field[i][j]) == repr(SudokuSymbol(self.__all_symbols, symbol)):
                                return False
                elif type(enabled) == list:
                    for i in range(self.__cols):
                        for j in range(self.__rows):
                            for group in enabled:
                                if (i, j) in group and (x, y) in group:
                                    if repr(self.__field[i][j]) == repr(SudokuSymbol(self.__all_symbols, symbol)):
                                        return False
            elif (rule == "diagonals" and enabled and self.__rows == self.__cols
                  and (x == y or x == self.__rows - y - 1)):
                # top-left to bottom-right
                for d in range(self.__rows):
                    if repr(self.__field[d][d]) == repr(SudokuSymbol(self.__all_symbols, symbol)) and x == y:
                        return False

                # top-right to bottom-left
                for d in range(self.__rows):
                    if (repr(self.__field[d][self.__rows - d - 1]) == repr(SudokuSymbol(self.__all_symbols, symbol))
                            and x == self.__rows - y - 1):
                        return False
        return True

    def __set_square(self, x: int, y: int, symbol: str) -> bool:
        if self.__check_square(x, y, symbol):
            self.__field[x][y].set_value(symbol)
            return True
        return False

    def __remove_square(self, x: int, y: int) -> None:
        self.__field[x][y] = SudokuSymbol(self.__all_symbols, self.__no_symbol)

    def __get_next_empty(self) -> Union[None, tuple[int, int]]:
        for i in range(self.__cols):
            for j in range(self.__rows):
                if self.__check_square_empty(i, j):
                    return i, j

    def lock_filled(self):
        for i in range(self.__cols):
            for j in range(self.__rows):
                if not self.__check_square_empty(i, j):
                    self.__field[i][j].lock()

    def solve(self) -> bool:
        next_empty: Union[None, tuple[int, int]] = self.__get_next_empty()
        if not next_empty:  # no empty squares
            return True
        for symbol in self.__all_symbols:
            if self.__set_square(*next_empty, symbol):
                solution = self.solve()
                if solution:
                    return True
                self.__remove_square(*next_empty)

    def get_field(self):
        return self.__field

    def __str__(self) -> str:
        list_rows: list[str] = []
        for i in range(self.__rows):
            list_rows.append("|".join(repr(val) for val in self.__field[i]))
        basestring: str = "\n-" + (self.__cols - 1) * "+-" + "\n"
        return basestring.join(list_rows)

    def __repr__(self) -> str:
        string: str = ""
        for row in self.__field:
            for square in row:
                string += str(square) + "&"
            string = string[:-1]
            string += "%"
        string = string[:-1]
        return string


def main() -> None:
    sudoku: Sudoku = Sudoku(field_string=EXAMPLE_FIELD_STRING, rules=STANDARD_RULES)
    print(sudoku)
    start_time: float = time.time()
    sudoku.solve()
    end_time: float = time.time()
    print(sudoku)
    print(f"Time used: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
