from typing import Union


class GroupSymbol:
    def __init__(self, symbol: Union[None, str] = None, color: str = "gray50") -> None:
        self.__symbol: Union[None, str] = symbol
        self.__color: str = color

    def set_value(self, symbol: Union[None, str] = None, color: str = "gray50") -> None:
        self.set_symbol(symbol)
        self.set_color(color)

    def append_value(self, value: str) -> None:
        if len(self.__symbol) < 2:
            self.set_value(self.__symbol + value)

    def set_symbol(self, symbol: Union[None, str] = None):
        self.__symbol = symbol

    def set_color(self, color: str = "black"):
        self.__color = color

    def is_empty(self):
        return True if self.__symbol is None else False

    def __format__(self, spec: None = None) -> Union[tuple[str, str], tuple[None, None]]:
        if self.__symbol is not None:
            return self.__symbol, self.__color
        return None, None


def main() -> None:
    pass


if __name__ == "__main__":
    main()
