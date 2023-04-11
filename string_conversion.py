from typing import Union


class SudokuString:
    def __init__(self, notation: str="sudokustring", filename: Union[None, str] = None,
                 string: Union[None, str] = None) -> None:
        self.__standard: Union[None, str] = None
        self.__sudokustring: Union[None, str] = None
        self.__square: Union[None, str] = None
        if filename:
            self.__input(filename, notation)
        else:
            if notation == "standard":
                self.__standard = string
            elif notation == "sudokustring":
                self.__sudokustring = string
            elif notation == "square":
                self.__square = string

    def __input(self, filename: str, notation: str = "sudokustring") -> None:
        with open(filename, "r") as f:
            if notation == "standard":
                self.__standard = f.read().rstrip()
            if notation == "sudokustring":
                self.__sudokustring = f.read().rstrip()
            elif notation == "square":
                self.__square = f.read().rstrip()

    def output(self, filename: str, notation: str = "sudokustring") -> None:
        with open(filename, "w+") as f:
            f.write(self.__str__(notation))

    def __sudokustring_to_standard(self) -> str:
        field_rows: list[str] = self.__sudokustring.split("%")  # split rows
        field: list[list[str]] = []
        for row in field_rows:
            field.append(row.split("&"))
        for i, row in enumerate(field):
            for j, item in enumerate(row):
                field[i][j] = item[0] if item != "" else "0"
                field[i][j] = "0" if field[i][j] == "_" else field[i][j]
        strings: list[str] = []
        for row in field:
            strings.append("".join(row))
        strings[-1] = strings[-1][:-1]
        self.__standard = "".join(strings)
        return self.__standard

    def __square_to_standard(self) -> str:
        self.__standard = "".join(self.__square.split("\n"))
        return self.__standard

    def __standard_to_sudokustring(self) -> str:
        string = ""
        for line in [self.__standard[i:i + 9] for i in range(0, len(self.__standard), 9)]:
            line = line.rstrip()
            for char in line:
                string += char + "&"
            string = string[:-1]
            string += "%"
        self.__sudokustring = string[:-1]
        return self.__sudokustring

    def __square_to_sudokustring(self) -> str:
        string = ""
        for line in self.__square.split("\n"):
            line = line.rstrip()
            for char in line:
                string += char + "&"
            string = string[:-1]
            string += "%"
        self.__sudokustring = string[:-1]
        return self.__sudokustring

    def __standard_to_square(self) -> str:
        self.__square = "\n".join([self.__standard[i:i + 9] for i in range(0, len(self.__standard), 9)])
        return self.__square

    def __sudokustring_to_square(self) -> str:
        field_rows: list[str] = self.__sudokustring.split("%")  # split rows
        field: list[list[str]] = []
        for row in field_rows:
            field.append(row.split("&"))
        for i, row in enumerate(field):
            for j, item in enumerate(row):
                field[i][j] = item[0] if item != "" else "0"
                field[i][j] = "0" if field[i][j] == "_" else field[i][j]
        strings: list[str] = []
        for row in field:
            strings.append("".join(row) + "\n")
        strings[-1] = strings[-1][:-1]
        self.__square = "".join(strings)
        return self.__square

    def __str__(self, notation: str = "sudokustring") -> str:
        if notation == "standard":
            if self.__standard is not None:
                pass
            elif self.__sudokustring is not None:
                self.__sudokustring_to_standard()
            elif self.__square is not None:
                self.__square_to_standard()
            return self.__standard
        elif notation == "sudokustring":
            if self.__sudokustring is not None:
                pass
            elif self.__standard is not None:
                self.__standard_to_sudokustring()
            elif self.__square is not None:
                self.__square_to_sudokustring()
            return self.__sudokustring
        elif notation == "square":
            if self.__square is not None:
                pass
            elif self.__standard is not None:
                self.__standard_to_square()
            elif self.__sudokustring is not None:
                self.__sudokustring_to_square()
            return self.__square


def main():
    EXAMPLE_FIELD_STRING = "5&3&0_1_2_3&0_4_5_6&7&0_7_8_9&0&0&0%6&0&0&1&9&5&0&0&0%0&9&8&0&0&0&0&6&0%8&0&0&0&6&0&0&0&3" \
                           "%4&0&0&8&0&3&0&0&1%7&0&0&0&2&0&0&0&6%0&6&0&0&0&0&2&8&0%0&0&0&4&1&9&0&0&5%0&0&0&0&8&0&0&7&9"
    EXAMPLE_FIELD_STRING_2 = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    EXAMPLE_FIELD_STRING_3 = "530070000\n600195000\n098000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079"
    s: SudokuString = SudokuString(notation="standard", string=EXAMPLE_FIELD_STRING_2)
    print(s.__str__("standard"))
    print("----")
    print(s.__str__("sudokustring"))
    print("----")
    print(s.__str__("square"))
    #s.output("sudoku_files/self-made/out_basic.txt", notation="square")
    #s.output("sudoku_files/self-made/out.txt", notation="sudokustring")


if __name__ == "__main__":
    main()
