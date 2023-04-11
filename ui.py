import os
import pygame
import math
from ui_button import Button
from ui_textfield import Textfield
from ui_checkbox import Checkbox
from symbol import SudokuSymbol
from text import Sudoku
from string_conversion import SudokuString
from group_symbol import GroupSymbol
from file_select import select_file
from typing import Union


"""
colors used:
"white": (255, 255, 255)
"black": (0, 0, 0)
"gray50": (127, 127, 127)
"gray83": (212, 212, 212)
"red": (255, 0, 0)
"""


class SudokuWindow:
    def __init__(self, sudoku_width: int = 9, sudoku_height: int = 9, field_groups: list[list[tuple[int, int]]] = None,
                 all_symbols: list = None,
                 rules: Union[None, dict[str, Union[bool, list[list[tuple[int, int]]]]]] = None, win_width: int = 1098,
                 win_height: int = 691, caption: str = "Sudoku", fontname: str = "Arial",
                 thin_thickness_factor: float = 1 / 58, thick_thickness_factor: float = 3 / 58,
                 selected_thickness_factor: float = 4 / 58, file_select_breaks: bool = False) -> None:
        self.__original_sudoku_size: tuple[int, int] = sudoku_width, sudoku_height
        self.__original_win_size: tuple[int, int] = win_width, win_height
        self.__sudoku_size: tuple[int, int] = self.__original_sudoku_size[:]
        self.__win_size: tuple[int, int] = self.__original_win_size[:]

        if all_symbols is None:
            self.__original_all_symbols: list[str] = [str(i+1) for i in range(max(self.__original_sudoku_size))]
        else:
            self.__original_all_symbols: list[str] = [str(i) for i in all_symbols]
        self.__original_all_symbols.sort()

        if field_groups is None:
            self.__set_standard_field_groups()
            self.__original_field_groups: list[list[tuple[int, int]]] = [[self.__field_groups[i][j][:]
                                                                          for j in range(len(self.__field_groups[i]))]
                                                                         for i in range(len(self.__field_groups))]
            """
            assert self.__sudoku_size == (9, 9), ("If the sudoku size isn't 9x9 fields, a field_groups list must be"
                                                  " provided.")
            self.__field_groups: list[list[tuple[int, int]]] = []
            for i in range(3):
                for j in range(3):
                    group = []
                    for m in range(3):
                        for n in range(3):
                            group.append((i * 3 + m, j * 3 + n))
                    self.__field_groups.append(group)
            """
        else:
            self.__original_field_groups: list[list[tuple[int, int]]] = field_groups

        self.__caption: str = caption
        self.__fontname: str = fontname

        pygame.init()
        self.__pygame_window: pygame.Surface = pygame.display.set_mode(self.__win_size, pygame.RESIZABLE)
        pygame.display.set_caption(self.__caption)

        pygame.font.init()
        self.__font_size: int = 0
        self.__font: pygame.font.Font = pygame.font.SysFont(self.__fontname, self.__font_size)

        self.__all_symbols: list[str] = self.__original_all_symbols[:]

        self.__board: list[list[SudokuSymbol]] = [[SudokuSymbol(self.__all_symbols, "0")
                                                   for _ in range(self.__sudoku_size[0])]
                                                  for _ in range(self.__sudoku_size[1])]

        self.__selected: Union[None, tuple[int, int]] = None

        self.__field_groups: list[list[tuple[int, int]]] = [[self.__original_field_groups[i][j][:]
                                                             for j in range(len(self.__original_field_groups[i]))]
                                                            for i in range(len(self.__original_field_groups))]

        self.__rules: dict[str, bool] = dict()
        self.__set_rules(rules)
        self.__original_rules: dict[str, bool] = {key: value for key, value in self.__rules.items()}

        self.__thin_thickness_factor: float = thin_thickness_factor
        self.__thick_thickness_factor: float = thick_thickness_factor
        self.__selected_thickness_factor: float = selected_thickness_factor

        self.__thin_thickness: int = 0
        self.__thick_thickness: int = 0
        self.__selected_thickness: int = 0

        self.__cell_size: int = 0
        self.__board_size: tuple[int, int] = (0, 0)
        self.__button_factor: float = 0
        self.__borders: tuple[int, int] = (0, 0)

        self.__font_size_notes: int = 0
        self.__font_notes: pygame.font.Font = pygame.font.SysFont(self.__fontname, self.__font_size_notes)

        self.__notes_cols: int = 0
        self.__notes_rows: int = 0
        self.__notes_distance_x: int = 0
        self.__notes_distance_y: int = 0

        self.__buttons: list[Button] = [Button(self.__pygame_window, "Lock", self.__lock_selected),
                                        Button(self.__pygame_window, "Solve", self.__solve),
                                        Button(self.__pygame_window, "Clear", self.__clear),
                                        Button(self.__pygame_window, "Import/Export", self.__io_window),
                                        Button(self.__pygame_window, "Change Size", self.__size_change_1),
                                        Button(self.__pygame_window, "Quit", self.__quit)]

        self.__textfield = Textfield(self.__pygame_window)

        self.__io_buttons: list[Button] = [Button(self.__pygame_window, "Back", self.__exit_side_window),
                                           Button(self.__pygame_window, "Import", self.__import_window),
                                           Button(self.__pygame_window, "Export", self.__export_window)]

        self.__in_buttons: list[Button] = [Button(self.__pygame_window, "Back", self.__io_window),
                                           Button(self.__pygame_window, "Standard", self.__in_standard),
                                           Button(self.__pygame_window, "SudokuString", self.__in_sudokustring),
                                           Button(self.__pygame_window, "Square", self.__in_square)]

        self.__out_buttons: list[Button] = [Button(self.__pygame_window, "Back", self.__io_window),
                                            Button(self.__pygame_window, "Standard", self.__out_standard),
                                            Button(self.__pygame_window, "SudokuString", self.__out_sudokustring),
                                            Button(self.__pygame_window, "Square", self.__out_square)]

        self.__size_change_1_clickable: list[Union[Button, Textfield]] = [
            Button(self.__pygame_window, "Back", self.__exit_side_window),
            Textfield(self.__pygame_window, text="9", placeholder="Width"),
            Textfield(self.__pygame_window, text="9", placeholder="Height"),
            Button(self.__pygame_window, "Continue", self.__size_change_2)]

        self.__size_change_2_clickable: list[Union[Button, Textfield]] = [
            Button(self.__pygame_window, "Back", self.__size_change_1),
            Textfield(self.__pygame_window, placeholder="Allowed Symbols"),
            Button(self.__pygame_window, "Clear Board and Continue", self.__size_change_3)]

        self.__size_change_3_clickable: list[Union[Button, Checkbox]] = [
            Checkbox(self.__pygame_window, "Horizontal", True),
            Checkbox(self.__pygame_window, "Vertical", True),
            Checkbox(self.__pygame_window, "Boxes", True),
            Checkbox(self.__pygame_window, "Diagonals", False),
            Button(self.__pygame_window, "Apply", self.__size_change_4)]

        self.__field_groups_board: list[list[GroupSymbol]] = [[GroupSymbol() for _ in range(self.__sudoku_size[0])]
                                                              for _ in range(self.__sudoku_size[1])]

        self.__file_select_breaks: bool = file_select_breaks

        self.__run: bool = True
        self.__ui_mode: str = "main"

        self.__alt_pressed: bool = False

    def __set_rules(self, rules: Union[None, dict[str, Union[bool, list[list[tuple[int, int]]]]]] = None) -> None:
        if rules is None:
            self.__rules = {"horizontal": True, "vertical": True, "boxes": None}
        else:
            self.__rules = rules
        if self.__rules["boxes"] is not False:
            self.__rules["boxes"] = self.__field_groups

    def __calc_size_properties(self, leave_win_size: bool = False) -> (tuple[tuple[int, int], int, float,
                                                                       tuple[int, int], tuple[int, int],
                                                                       tuple[int, int, int], int, pygame.font.Font,
                                                                       tuple[int, int], tuple[int, int], int,
                                                                       pygame.font.Font]):
        # Calculate the size of the cells
        win_size: tuple[int, int] = self.__pygame_window.get_size() if not leave_win_size else self.__win_size
        cell_size: int = min(math.floor(0.8 * win_size[0] / (5/3 * self.__sudoku_size[0])),
                             math.floor(0.8 * win_size[1] / self.__sudoku_size[1]))
        button_factor: float = 0.8 * win_size[0] / (cell_size * self.__sudoku_size[0]) - 1
        button_factor = max(min(button_factor, 3/2), 2/3)

        # Calculate the size of the board
        board_size: tuple[int, int] = cell_size * self.__sudoku_size[0], cell_size * self.__sudoku_size[1]

        # Calculate the size of the border
        border_left: int = int((win_size[0] - (1 + button_factor) * board_size[0]) / 4)
        border_top: int = int((win_size[1] - board_size[1]) / 2)
        borders: tuple[int, int] = border_left, border_top

        # Change line thickness
        thin_thickness: int = math.ceil(self.__thin_thickness_factor * cell_size)
        thick_thickness: int = math.ceil(self.__thick_thickness_factor * cell_size)
        selected_thickness: int = math.ceil(self.__selected_thickness_factor * cell_size)

        # Change font (main symbols)
        font_size: int = int(cell_size / 52 * 36)
        font: pygame.font.Font = pygame.font.SysFont(self.__fontname, font_size)

        # Note dimensions
        notes_cols: int = math.ceil(math.sqrt(len(self.__all_symbols)))
        notes_rows: int = math.ceil(len(self.__all_symbols) / notes_cols)
        notes_distance_x: int = round((cell_size - thin_thickness) / (2 * notes_cols))
        notes_distance_y: int = round((cell_size - thin_thickness) / (2 * notes_rows))

        # Font (notes)
        font_size_notes: int = int(1.6 * notes_distance_y)
        font_notes: pygame.font.Font = pygame.font.SysFont(self.__fontname, font_size_notes)
        return (win_size, cell_size, button_factor, board_size, borders,
                (thin_thickness, thick_thickness, selected_thickness), font_size, font, (notes_cols, notes_rows),
                (notes_distance_x, notes_distance_y), font_size_notes, font_notes)

    def __set_size_properties(self, leave_win_size: bool = False) -> (tuple[tuple[int, int], tuple[int, int], int,
                                                                      tuple[int, int], tuple[int, int]]):
        (self.__win_size, self.__cell_size, self.__button_factor, self.__board_size, self.__borders,
         (self.__thin_thickness, self.__thick_thickness, self.__selected_thickness), self.__font_size, self.__font,
         (self.__notes_rows, self.__notes_cols), (self.__notes_distance_x, self.__notes_distance_y),
         self.__font_size_notes, self.__font_notes) = self.__calc_size_properties(leave_win_size=leave_win_size)
        return self.__sudoku_size, self.__win_size, self.__cell_size, self.__board_size, self.__borders

    def __set_standard_field_groups(self) -> None:
        match self.__sudoku_size:
            case (6, 6):
                self.__field_groups_board = [[GroupSymbol(chr(ord("A") + i//3 + 2 * (j//2)))
                                              for i in range(self.__sudoku_size[0])]
                                             for j in range(self.__sudoku_size[1])]
            case (9, 9):
                self.__field_groups_board = [[GroupSymbol(chr(ord("A") + i//3 + 3 * (j//3)))
                                              for i in range(self.__sudoku_size[0])]
                                             for j in range(self.__sudoku_size[1])]
            case(12, 12):
                self.__field_groups_board = [[GroupSymbol(chr(ord("A") + i//3 + 4 * (j//4)))
                                              for i in range(self.__sudoku_size[0])]
                                             for j in range(self.__sudoku_size[1])]
            case _:
                self.__field_groups_board = [[GroupSymbol() for _ in range(self.__sudoku_size[0])]
                                             for _ in range(self.__sudoku_size[1])]

        self.__update_field_groups()

    def __update_field_groups(self) -> None:
        self.__field_groups = []
        group_symbols: set[str, None] = set()
        for i in range(self.__sudoku_size[0]):
            for j in range(self.__sudoku_size[1]):

                group_symbols.add(self.__field_groups_board[j][i].__format__()[0])
        for group in group_symbols:
            if group is None:
                continue
            group_list: list[tuple[int, int]] = []
            for i in range(self.__sudoku_size[0]):
                for j in range(self.__sudoku_size[1]):
                    if group == self.__field_groups_board[j][i].__format__()[0]:
                        group_list.append((i, j))
            if group_list:
                self.__field_groups.append([group_list[cell][:] for cell in range(len(group_list))])

    def __handle_click(self, pos) -> None:
        if self.__ui_mode == "main":
            # Handle button clicks
            for button in self.__buttons:
                button.clicked(pos)

            # Handle textfield click
            self.__textfield.clicked(pos)

            # Handle click on field
            x, y = pos
            if self.__borders[0] < x < self.__borders[0] + self.__board_size[0] \
                    and self.__borders[1] < y < self.__borders[1] + self.__board_size[1]:
                i = int((x - self.__borders[0]) // self.__cell_size)
                j = int((y - self.__borders[1]) // self.__cell_size)
                self.__selected = i, j
                self.__update_notes_textfield()
            elif not self.__textfield.is_active():
                self.__selected = None
        elif self.__ui_mode == "io":
            for button in self.__io_buttons:
                button.clicked(pos)
        elif self.__ui_mode == "in":
            for button in self.__in_buttons:
                button.clicked(pos)
        elif self.__ui_mode == "out":
            for button in self.__out_buttons:
                button.clicked(pos)
        elif self.__ui_mode == "size_change_1":
            for clickable in self.__size_change_1_clickable:
                clickable.clicked(pos)
        elif self.__ui_mode == "size_change_2":
            for clickable in self.__size_change_2_clickable:
                clickable.clicked(pos)
        elif self.__ui_mode == "size_change_3":
            # Handle clickable clicks
            for clickable in self.__size_change_3_clickable:
                clickable.clicked(pos)

            # Handle click on field
            x, y = pos
            if self.__borders[0] < x < self.__borders[0] + self.__board_size[0] \
                    and self.__borders[1] < y < self.__borders[1] + self.__board_size[1]:
                i = int((x - self.__borders[0]) // self.__cell_size)
                j = int((y - self.__borders[1]) // self.__cell_size)
                self.__selected = i, j
                self.__update_notes_textfield()
            elif not self.__textfield.is_active():
                self.__selected = None

    def __handle_key(self, key: pygame.key, event: pygame.event.Event) -> None:
        if self.__ui_mode == "main":
            if self.__selected is not None:
                i, j = self.__selected
                if self.__textfield.is_active():
                    if key == pygame.K_RETURN:
                        self.__textfield.set_active(False)
                        self.__update_notes_textfield()
                    else:
                        self.__textfield.handle_key(key, event)
                        self.__board[j][i].set_notes([note.strip() for note in self.__textfield.get_text().split(",")])
                else:
                    if key == pygame.K_LEFT:
                        self.__selected = (max(0, i - 1), j)
                    elif key == pygame.K_RIGHT:
                        self.__selected = (min(self.__sudoku_size[0] - 1, i + 1), j)
                    elif key == pygame.K_UP:
                        self.__selected = (i, max(0, j - 1))
                    elif key == pygame.K_DOWN:
                        self.__selected = (i, min(self.__sudoku_size[1] - 1, j + 1))
                    elif key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
                        self.__board[j][i].set_value()
                    elif str(event.unicode) in self.__all_symbols:
                        if self.__board[j][i].is_empty():
                            self.__board[j][i].set_value(str(event.unicode))
                        else:
                            self.__board[j][i].append_value(str(event.unicode))
                    elif key == pygame.K_n:
                        self.__textfield.set_active()
                    self.__update_notes_textfield()
            else:
                if key == pygame.K_LEFT or key == pygame.K_RIGHT or key == pygame.K_UP or key == pygame.K_DOWN:
                    self.__selected = 0, 0
        elif self.__ui_mode == "size_change_1":
            for clickable in self.__size_change_1_clickable:
                if type(clickable) == Textfield:
                    if clickable.is_active():
                        if key == pygame.K_RETURN:
                            clickable.set_active(False)
                        else:
                            clickable.handle_key(key, event)
        elif self.__ui_mode == "size_change_2":
            for clickable in self.__size_change_2_clickable:
                if type(clickable) == Textfield:
                    if clickable.is_active():
                        if key == pygame.K_RETURN:
                            clickable.set_active(False)
                        else:
                            clickable.handle_key(key, event)
        elif self.__ui_mode == "size_change_3":
            if self.__selected is not None:
                i, j = self.__selected
                if key == pygame.K_LEFT:
                    self.__selected = (max(0, i - 1), j)
                elif key == pygame.K_RIGHT:
                    self.__selected = (min(self.__sudoku_size[0] - 1, i + 1), j)
                elif key == pygame.K_UP:
                    self.__selected = (i, max(0, j - 1))
                elif key == pygame.K_DOWN:
                    self.__selected = (i, min(self.__sudoku_size[1] - 1, j + 1))
                elif key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
                    self.__field_groups_board[j][i].set_value()
                else:
                    """
                    if self.__field_groups_board[j][i].is_empty():
                        self.__field_groups_board[j][i].set_value(str(event.unicode))
                    else:
                        self.__field_groups_board[j][i].append_value(str(event.unicode))
                    """
                    self.__field_groups_board[j][i].set_value(str(event.unicode))
                    self.__update_field_groups()
            else:
                if key == pygame.K_LEFT or key == pygame.K_RIGHT or key == pygame.K_UP or key == pygame.K_DOWN:
                    self.__selected = 0, 0

    def __draw_cells(self, board: Union[None, list[list[SudokuSymbol]], list[list[GroupSymbol]]] = None) -> None:
        if board is None:
            board = self.__board
        # Draw the cells
        for i in range(self.__sudoku_size[0]):
            for j in range(self.__sudoku_size[1]):
                x: int = self.__borders[0] + i * self.__cell_size
                y: int = self.__borders[1] + j * self.__cell_size
                pygame.draw.rect(self.__pygame_window, "white", (x, y, self.__cell_size, self.__cell_size))
                render: Union[None, tuple[str, str], tuple[None, None], list[str]] = board[j][i].__format__()
                if type(render) == tuple:
                    if render[0] is not None:
                        text: pygame.Surface = self.__font.render(render[0], True, render[1])
                        coordinates: tuple[int, int] = (int(x + (self.__cell_size + self.__thin_thickness
                                                                 - text.get_width()) / 2),
                                                        int(y + (self.__cell_size + self.__thin_thickness
                                                                 - text.get_height()) / 2))
                        self.__pygame_window.blit(text, coordinates)
                elif type(render) == list:
                    for n_j in range(self.__notes_rows):
                        for n_i in range(self.__notes_cols):
                            note_x = x + self.__thin_thickness + self.__notes_distance_x * (2 * n_i + 1)
                            note_y = y + self.__thin_thickness + self.__notes_distance_y * (2 * n_j + 1)
                            for note in render:
                                if note == self.__all_symbols[self.__notes_cols * n_j + n_i]:
                                    text: pygame.Surface = self.__font_notes.render(note, True, "grey50")
                                    coordinates = (int(note_x - text.get_width() / 2),
                                                   int(note_y - text.get_height() / 2))
                                    self.__pygame_window.blit(text, coordinates)

    def __draw_borders(self) -> None:
        # Draw the outer borders
        pygame.draw.line(self.__pygame_window, "black", self.__borders,
                         (self.__borders[0], self.__borders[1] + self.__board_size[1]), self.__thick_thickness)
        pygame.draw.line(self.__pygame_window, "black", (self.__borders[0] + self.__board_size[0], self.__borders[1]),
                         (self.__borders[0] + self.__board_size[0], self.__borders[1] + self.__board_size[1]),
                         self.__thick_thickness)
        pygame.draw.line(self.__pygame_window, "black", self.__borders,
                         (self.__borders[0] + self.__board_size[0], self.__borders[1]), self.__thick_thickness)
        pygame.draw.line(self.__pygame_window, "black", (self.__borders[0], self.__borders[1] + self.__board_size[1]),
                         (self.__borders[0] + self.__board_size[0], self.__borders[1] + self.__board_size[1]),
                         self.__thick_thickness)

        # Draw the inner vertical lines
        for i in range(self.__sudoku_size[0] - 1):
            for j in range(self.__sudoku_size[1]):
                thickness: int = self.__thick_thickness
                for group in self.__field_groups:
                    if (i, j) in group and (i + 1, j) in group:
                        thickness = self.__thin_thickness
                        break
                pygame.draw.line(self.__pygame_window, "black",
                                 (self.__borders[0] + (i + 1) * self.__cell_size,
                                  self.__borders[1] + j * self.__cell_size),
                                 (self.__borders[0] + (i + 1) * self.__cell_size,
                                  self.__borders[1] + (j + 1) * self.__cell_size), thickness)

        # Draw the inner horizontal lines
        for i in range(self.__sudoku_size[1] - 1):
            for j in range(self.__sudoku_size[0]):
                thickness: int = self.__thick_thickness
                for group in self.__field_groups:
                    if (j, i) in group and (j, i + 1) in group:
                        thickness = self.__thin_thickness
                        break
                pygame.draw.line(self.__pygame_window, "black",
                                 (self.__borders[0] + j * self.__cell_size,
                                  self.__borders[1] + (i + 1) * self.__cell_size),
                                 (self.__borders[0] + (j + 1) * self.__cell_size,
                                  self.__borders[1] + (i + 1) * self.__cell_size), thickness)

    def __draw_selected(self) -> None:
        if self.__selected is not None:
            x = self.__borders[0] + self.__selected[0] * self.__cell_size
            y = self.__borders[1] + self.__selected[1] * self.__cell_size
            pygame.draw.rect(self.__pygame_window, "red",
                             (x, y, self.__cell_size + self.__thin_thickness, self.__cell_size + self.__thin_thickness),
                             self.__selected_thickness)

    def __draw_buttons(self) -> None:
        button_space: float = self.__board_size[1] / (len(self.__buttons) + 1)
        for i, button in enumerate(self.__buttons):
            size_properties: tuple[tuple[int, int], tuple[int, int], Union[None, int]] = (
                (self.__borders[0] + self.__board_size[0] + 2 * self.__borders[0],
                 int(self.__borders[1] + i * 1 * button_space + 0.1 * button_space)),
                (int(self.__button_factor * self.__board_size[0]), int(0.8 * button_space)), None)
            if i == 0:
                text: str = "Lock" if not self.__alt_pressed else "Lock All"
            elif i == 2:
                text: str = "Clear" if not self.__alt_pressed else "Reset"
            else:
                text: None = None
            button.draw(size_properties, text)

    def __draw_notes_textfield(self) -> None:
        button_space: float = self.__board_size[1] / (len(self.__buttons) + 1)
        size_properties: tuple[tuple[int, int], tuple[int, int], Union[None, int]] = (
            (self.__borders[0] + self.__board_size[0] + 2 * self.__borders[0],
             int(self.__borders[1] + len(self.__buttons) * 1 * button_space + 0.1 * button_space)),
            (int(self.__button_factor * self.__board_size[0]), int(0.8 * button_space)), None)
        self.__textfield.draw(size_properties)

    def __update_notes_textfield(self) -> None:
        try:
            i, j = self.__selected
            self.__textfield.set_text(",".join(self.__board[j][i].get_notes()))
        except TypeError:
            pass

    def __draw_field(self, board: Union[None, list[list[SudokuSymbol]], list[list[GroupSymbol]]] = None) -> None:
        self.__draw_cells(board=board)
        self.__draw_borders()
        self.__draw_selected()

    def __draw_separating_line(self) -> None:
        pygame.draw.line(self.__pygame_window, "black",
                         (2 * self.__borders[0] + self.__board_size[0], self.__borders[1]),
                         (2 * self.__borders[0] + self.__board_size[0], self.__borders[1] + self.__board_size[1]),
                         self.__thin_thickness)

    def __draw_io_buttons(self) -> None:
        button_space: float = self.__board_size[1] / (len(self.__buttons) + 1)
        for i, button in enumerate(self.__io_buttons):
            size_properties: tuple[tuple[int, int], tuple[int, int], Union[None, int]] = (
                (self.__borders[0],
                 int(self.__borders[1] + i * 1 * button_space + 0.1 * button_space)),
                (int(self.__button_factor * self.__board_size[0]), int(0.8 * button_space)), None)
            button.draw(size_properties)

    def __draw_in_buttons(self) -> None:
        button_space: float = self.__board_size[1] / (len(self.__buttons) + 1)
        for i, button in enumerate(self.__in_buttons):
            size_properties: tuple[tuple[int, int], tuple[int, int], Union[None, int]] = (
                (self.__borders[0],
                 int(self.__borders[1] + i * 1 * button_space + 0.1 * button_space)),
                (int(self.__button_factor * self.__board_size[0]), int(0.8 * button_space)), None)
            button.draw(size_properties)

    def __draw_out_buttons(self) -> None:
        button_space: float = self.__board_size[1] / (len(self.__buttons) + 1)
        for i, button in enumerate(self.__out_buttons):
            size_properties: tuple[tuple[int, int], tuple[int, int], Union[None, int]] = (
                (self.__borders[0],
                 int(self.__borders[1] + i * 1 * button_space + 0.1 * button_space)),
                (int(self.__button_factor * self.__board_size[0]), int(0.8 * button_space)), None)
            button.draw(size_properties)

    def __draw_size_change_1_clickable(self):
        button_space: float = self.__board_size[1] / (len(self.__buttons) + 1)
        for i, clickable in enumerate(self.__size_change_1_clickable):
            size_properties: tuple[tuple[int, int], tuple[int, int], Union[None, int]] = (
                (self.__borders[0],
                 int(self.__borders[1] + i * 1 * button_space + 0.1 * button_space)),
                (int(self.__button_factor * self.__board_size[0]), int(0.8 * button_space)), None)
            clickable.draw(size_properties)

    def __draw_size_change_2_clickable(self):
        button_space: float = self.__board_size[1] / (len(self.__buttons) + 1)
        for i, clickable in enumerate(self.__size_change_2_clickable):
            size_properties: tuple[tuple[int, int], tuple[int, int], Union[None, int]] = (
                (self.__borders[0],
                 int(self.__borders[1] + i * 1 * button_space + 0.1 * button_space)),
                (int(self.__button_factor * self.__board_size[0]), int(0.8 * button_space)), None)
            clickable.draw(size_properties)

    def __draw_size_change_3_clickable(self):
        button_space: float = self.__board_size[1] / (len(self.__buttons) + 1)
        to_draw: list[Button, Checkbox] = []
        for i, clickable in enumerate(self.__size_change_3_clickable):
            if type(clickable) == Checkbox:
                if clickable.get_text().lower() == "diagonals" and self.__sudoku_size[0] != self.__sudoku_size[1]:
                    continue
            to_draw.append(clickable)
        for i, clickable in enumerate(to_draw):
            size_properties: tuple[tuple[int, int], tuple[int, int], Union[None, int]] = (
                (self.__borders[0] + self.__board_size[0] + 2 * self.__borders[0],
                 int(self.__borders[1] + i * 1 * button_space + 0.1 * button_space)),
                (int(self.__button_factor * self.__board_size[0]), int(0.8 * button_space)), None)
            clickable.draw(size_properties)

    def __draw_all(self) -> None:
        # Draw the background
        self.__pygame_window.fill("white")

        if self.__ui_mode == "main":
            self.__draw_field()
            self.__draw_buttons()
            if self.__selected is not None:
                i, j = self.__selected
                if self.__board[j][i].accept_notes():
                    self.__draw_notes_textfield()

            self.__draw_separating_line()
        elif self.__ui_mode == "io":
            self.__draw_io_buttons()
        elif self.__ui_mode == "in":
            self.__draw_in_buttons()
        elif self.__ui_mode == "out":
            self.__draw_out_buttons()
        elif self.__ui_mode == "size_change_1":
            self.__draw_size_change_1_clickable()
        elif self.__ui_mode == "size_change_2":
            self.__draw_size_change_2_clickable()
        elif self.__ui_mode == "size_change_3":
            self.__draw_field(board=self.__field_groups_board)
            self.__draw_size_change_3_clickable()

            self.__draw_separating_line()

    def __set_ui_mode(self, ui_mode: str = "main") -> None:
        # wait for MOUSEBUTTONUP needed to register all clicks
        while True:
            e: pygame.event.Event = pygame.event.wait()
            if e.type == pygame.MOUSEBUTTONUP:
                break
        self.__ui_mode = ui_mode

    def run(self) -> None:
        self.__set_size_properties()
        while self.__run:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__quit()
                elif event.type == pygame.VIDEORESIZE:
                    if self.__ui_mode == "main":
                        self.__win_size = event.w, event.h
                        self.__pygame_window = pygame.display.set_mode(self.__win_size, pygame.RESIZABLE)
                        self.__set_size_properties()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.__handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.get_mods() & pygame.KMOD_ALT:
                        self.__alt_pressed = True
                    if event.key == pygame.K_ESCAPE:
                        self.__quit()
                    else:
                        self.__handle_key(event.key, event)
                elif event.type == pygame.KEYUP:
                    if not pygame.key.get_mods() & pygame.KMOD_ALT:
                        self.__alt_pressed = False

            # Draw everything
            self.__draw_all()

            # Update the display
            pygame.display.update()

    def __lock_selected(self) -> None:
        if self.__alt_pressed:  # if option is pressed, lock all
            for i in range(self.__sudoku_size[0]):
                for j in range(self.__sudoku_size[1]):
                    self.__board[j][i].lock()
        else:
            if self.__selected is not None:
                i, j = self.__selected
                self.__board[j][i].lock()

    def __solve(self) -> None:
        sudoku: Sudoku = Sudoku(size=self.__sudoku_size, field=self.__board, rules=self.__rules,
                                all_symbols=self.__all_symbols)
        sudoku.solve()
        self.__board = sudoku.get_field()

    def __clear(self) -> None:
        if self.__alt_pressed:
            self.__sudoku_size = self.__original_sudoku_size[:]
            self.__win_size = self.__original_win_size[:]
            self.__all_symbols = self.__original_all_symbols[:]
            self.__field_groups = [[self.__original_field_groups[i][j][:]
                                    for j in range(len(self.__original_field_groups[i]))]
                                   for i in range(len(self.__original_field_groups))]
            self.__rules = {key: value for key, value in self.__original_rules.items()}

            self.__set_size_properties()
        self.__board = [[SudokuSymbol(self.__all_symbols, "") for _ in range(self.__sudoku_size[0])]
                        for _ in range(self.__sudoku_size[1])]

    def __exit_side_window(self) -> None:
        self.__set_ui_mode("main")
        self.__pygame_window = pygame.display.set_mode(self.__win_size, pygame.RESIZABLE)
        pygame.display.set_caption(self.__caption)

    def __io_window(self) -> None:
        self.__set_ui_mode("io")
        self.__pygame_window = pygame.display.set_mode(
            (self.__win_size[0] - (2 * self.__borders[0] + self.__board_size[0]),
             2 * self.__borders[1] + self.__board_size[1]))
        pygame.display.set_caption(self.__caption + " Import/Export")

    def __import_window(self) -> None:
        self.__set_ui_mode("in")
        self.__pygame_window = pygame.display.set_mode(
            (self.__win_size[0] - (2 * self.__borders[0] + self.__board_size[0]),
             2 * self.__borders[1] + self.__board_size[1]))
        pygame.display.set_caption(self.__caption + " Import")

    def __export_window(self) -> None:
        self.__set_ui_mode("out")
        self.__pygame_window = pygame.display.set_mode(
            (self.__win_size[0] - (2 * self.__borders[0] + self.__board_size[0]),
             2 * self.__borders[1] + self.__board_size[1]))
        pygame.display.set_caption(self.__caption + " Export")

    def __size_change_1(self) -> None:
        self.__set_ui_mode("size_change_1")
        self.__pygame_window = pygame.display.set_mode(
            (self.__win_size[0] - (2 * self.__borders[0] + self.__board_size[0]),
             2 * self.__borders[1] + self.__board_size[1]))
        pygame.display.set_caption(self.__caption + " - Change Size")

    def __size_change_2(self) -> None:
        try:
            sudoku_size_temp: tuple[int, int] = (int(self.__size_change_1_clickable[1].get_text()),
                                                 int(self.__size_change_1_clickable[2].get_text()))

            self.__size_change_2_clickable[1].set_text(",".join([str(i + 1) for i in range(max(sudoku_size_temp))]))

            self.__set_ui_mode("size_change_2")
            self.__pygame_window = pygame.display.set_mode(
                (self.__win_size[0] - (2 * self.__borders[0] + self.__board_size[0]),
                 2 * self.__borders[1] + self.__board_size[1]))
            pygame.display.set_caption(self.__caption + " - Change Size")
        except ValueError:
            pass

    def __size_change_3(self) -> None:
        try:
            # Set stuff from first page:
            self.__sudoku_size = (int(self.__size_change_1_clickable[1].get_text()),
                                  int(self.__size_change_1_clickable[2].get_text()))

            # Set stuff from second page:
            all_symbols_temp: Union[list[str], None, str] = self.__size_change_2_clickable[1].get_text().split(",")
            if all_symbols_temp is None or all_symbols_temp == "":
                self.__all_symbols = [str(i + 1) for i in range(max(self.__sudoku_size))]
            else:
                self.__all_symbols = [str(i).strip() for i in all_symbols_temp]
            try:
                self.__all_symbols = [int(symbol) for symbol in self.__all_symbols]
                self.__all_symbols.sort()
                self.__all_symbols = [str(symbol) for symbol in self.__all_symbols]
            except ValueError:
                self.__all_symbols.sort()

            self.__board = [[SudokuSymbol(all_symbols_temp, "0")
                             for _ in range(self.__sudoku_size[0])]
                            for _ in range(self.__sudoku_size[1])]

            self.__set_standard_field_groups()

            self.__set_size_properties(leave_win_size=True)

            self.__set_ui_mode("size_change_3")
            self.__pygame_window = pygame.display.set_mode(self.__win_size)
            pygame.display.set_caption(self.__caption + " - Change Size")
        except TypeError:
            pass

    def __size_change_4(self) -> None:
        # Set stuff from third page:
        rules: dict[str, bool] = dict()
        for clickable in self.__size_change_3_clickable:
            if type(clickable) == Checkbox:
                rules[clickable.get_text().lower()] = clickable.get_checked()
        self.__set_rules(rules)

        self.__exit_side_window()
        self.__set_size_properties()

    def __in_standard(self) -> None:
        if not self.__file_select_breaks:
            filename = select_file()
        else:
            filename = "sudoku_files/in-out/in_standard.txt"
        with open(filename, "r") as f:
            contents: str = f.read()
        contents = str(SudokuString(notation="standard", string=contents))
        sudoku: Sudoku = Sudoku(size=self.__sudoku_size, field_string=contents)
        sudoku.lock_filled()
        self.__board = sudoku.get_field()
        self.__exit_side_window()

    def __in_sudokustring(self) -> None:
        if not self.__file_select_breaks:
            filename = select_file()
        else:
            filename = "sudoku_files/in-out/in_sudokustring.txt"
        with open(filename, "r") as f:
            contents: str = f.read()
        sudoku: Sudoku = Sudoku(size=self.__sudoku_size, field_string=contents)
        sudoku.lock_filled()
        self.__board = sudoku.get_field()
        self.__exit_side_window()

    def __in_square(self) -> None:
        if not self.__file_select_breaks:
            filename = select_file()
        else:
            filename = "sudoku_files/in-out/in_square.txt"
        with open(filename, "r") as f:
            contents: str = f.read()
        contents = str(SudokuString(notation="square", string=contents))
        sudoku: Sudoku = Sudoku(size=self.__sudoku_size, field_string=contents)
        sudoku.lock_filled()
        self.__board = sudoku.get_field()
        self.__exit_side_window()

    def __out_standard(self) -> None:
        if not self.__file_select_breaks:
            filename = select_file()
        else:
            filename = "sudoku_files/in-out/out_standard.txt"
        sudoku: Sudoku = Sudoku(size=self.__sudoku_size, field=self.__board)
        with open(filename, "w+") as f:
            f.write(SudokuString(string=repr(sudoku)).__str__(notation="standard"))
        self.__exit_side_window()

    def __out_sudokustring(self) -> None:
        if not self.__file_select_breaks:
            filename = select_file()
        else:
            filename = "sudoku_files/in-out/out_sudokustring.txt"
        sudoku: Sudoku = Sudoku(size=self.__sudoku_size, field=self.__board)
        with open(filename, "w+") as f:
            f.write(repr(sudoku))
        self.__exit_side_window()

    def __out_square(self) -> None:
        if not self.__file_select_breaks:
            filename = select_file()
        else:
            filename = "sudoku_files/in-out/out_square.txt"
        sudoku: Sudoku = Sudoku(size=self.__sudoku_size, field=self.__board)
        with open(filename, "w+") as f:
            f.write(SudokuString(string=repr(sudoku)).__str__(notation="square"))
        self.__exit_side_window()

    def __quit(self) -> None:
        self.__run = False
        if self.__alt_pressed:
            if os.name == "posix":
                os.system("open dependencies/totallyimportant.mp4")
            elif os.name == "nt":
                os.system("start dependencies/totallyimportant.mp4")

    @staticmethod
    def quit() -> None:
        pygame.quit()


def main() -> None:
    win: SudokuWindow = SudokuWindow(file_select_breaks=True)
    win.run()
    SudokuWindow.quit()


if __name__ == "__main__":
    main()
