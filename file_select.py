def select_file(title: str = "test") -> str:
    import easygui as g
    return g.fileopenbox(title)


def main() -> None:
    print(select_file())


if __name__ == "__main__":
    main()
