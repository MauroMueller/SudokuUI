import pygame
from typing import Union


class Button:
    def __init__(self, window: pygame.Surface, text: str, action: callable, color: str = "gray50",
                 fontname: str = "Arial", textcolor: str = "black") -> None:
        self.__window: pygame.Surface = window

        self.__button_size_properties: tuple[tuple[int, int], tuple[int, int], int] = ((0, 0), (0, 0), 0)

        self.__x: int = self.__button_size_properties[0][0]
        self.__y: int = self.__button_size_properties[0][1]
        self.__width: int = self.__button_size_properties[1][0]
        self.__height: int = self.__button_size_properties[1][1]

        self.__text: str = text
        self.__action: callable = action
        self.__color: str = color
        self.__fontname: str = fontname
        self.__font_size: int = self.__button_size_properties[2]
        self.__textcolor: str = textcolor

    def __get_font_size(self) -> int:
        font_size: float = 0.7 * self.__height
        font: pygame.font.Font = pygame.font.SysFont(self.__fontname, int(font_size))
        text: pygame.Surface = font.render(self.__text, True, self.__textcolor)
        while text.get_width() > self.__width - 0.5 * self.__height:
            font_size *= 0.99
            font = pygame.font.SysFont(self.__fontname, int(font_size))
            text = font.render(self.__text, True, self.__textcolor)
        return int(font_size)

    def draw(self, button_size_properties: tuple[tuple[int, int], tuple[int, int], int],
             text: Union[None, str] = None) -> None:
        self.__button_size_properties = button_size_properties

        self.__x = self.__button_size_properties[0][0]
        self.__y = self.__button_size_properties[0][1]
        self.__width = self.__button_size_properties[1][0]
        self.__height = self.__button_size_properties[1][1]
        self.__font_size = self.__button_size_properties[2]

        if text is not None:
            self.__text = text

        if self.__font_size is None:
            self.__font_size = self.__get_font_size()

        font: pygame.font.Font = pygame.font.SysFont(self.__fontname, self.__font_size)
        text: pygame.Surface = font.render(self.__text, True, self.__textcolor)

        pygame.draw.rect(self.__window, self.__color, (self.__x, self.__y, self.__width, self.__height))

        self.__window.blit(text, (self.__x + 0.25 * self.__height, self.__y + (self.__height - self.__font_size) / 2))

    def clicked(self, pos: tuple[int, int]) -> None:
        if self.__x <= pos[0] <= self.__x + self.__width and self.__y <= pos[1] <= self.__y + self.__height:
            self.__action()
