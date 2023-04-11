from typing import Union


class SudokuSymbol:
    def __init__(self, all_symbols: Union[list[int], list[str]], symbol: str, locked: bool = False) -> None:
        self.__symbol: str = ""
        self.__notes: list[str] = []
        self.__locked: bool = False
        self.__all_symbols: list[str] = [str(symbol) for symbol in all_symbols if symbol != ""]

        self.set_value(symbol)

        self.__locked: bool = locked

    def set_value(self, symbol: Union[str, bool] = False, lock: bool = False) -> bool:
        if self.__locked:
            return False
        # self.__symbol = str(symbol)
        if not symbol:
            self.__symbol = ""
            self.__notes = []
        else:
            symbol: str = str(symbol)
            if "_" in symbol:  # contains notes
                symbol: list = symbol.split("_")
                notes: list = symbol[1:]
                self.__symbol = symbol[0] if symbol[0] in self.__all_symbols else self.__symbol
                self.set_notes(notes)
            else:
                self.__symbol = symbol if symbol in self.__all_symbols else self.__symbol
                self.__notes = []
            """
            if self.__symbol in self.__all_symbols:  # remove notes if field is filled
                self.__notes = []
            else:
                self.__symbol = ""
            """

        if lock:
            self.lock()
        return True

    def append_value(self, value: str) -> bool:
        return self.set_value(self.__symbol + value)

    def accept_notes(self) -> bool:
        if self.__locked or self.__symbol != "":
            return False
        return True

    def set_notes(self, notes: list[str]):
        if self.accept_notes():
            self.__notes = [str(note) for note in notes if str(note) in self.__all_symbols]
            self.__notes = [*set(self.__notes)]
            self.__notes.sort()

    def lock(self):
        if not self.accept_notes():
            self.__locked = True

    def get_notes(self):
        return self.__notes

    def is_empty(self):
        return True if self.__symbol == "" else False

    def __repr__(self) -> str:
        if self.__symbol not in self.__all_symbols:
            if self.__notes:
                return "n"
            return " "
        return str(self.__symbol)

    def __str__(self) -> str:
        return "_".join([str(self.__symbol), *self.__notes])

    def __format__(self, spec: None = None) -> Union[None, tuple[str, str], list[str]]:
        if self.__symbol:
            if self.__locked:
                return self.__symbol, "black"
            return self.__symbol, "blue"
        if self.__notes:
            return self.__notes
        return None
