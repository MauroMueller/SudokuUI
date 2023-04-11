from text import Sudoku


def main():
    s: Sudoku = Sudoku()
    print(s.get_field())
    s.get_field()[0][0].set_value(9)
    print(s.get_field())


if __name__ == "__main__":
    main()