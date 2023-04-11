import pygame


class Checkbox:
    def __init__(self, window: pygame.Surface, text: str, checked: bool, color: str = "gray50",
                 bg_color: str = "white", fontname: str = "Arial", textcolor: str = "black") -> None:
        self.__window: pygame.Surface = window

        self.__checkbox_size_properties: tuple[tuple[int, int], tuple[int, int], int] = ((0, 0), (0, 0), 0)

        self.__x: int = self.__checkbox_size_properties[0][0]
        self.__y: int = self.__checkbox_size_properties[0][1]
        self.__width: int = self.__checkbox_size_properties[1][0]
        self.__height: int = self.__checkbox_size_properties[1][1]

        self.__text: str = text
        self.__checked: callable = checked
        self.__color: str = color
        self.__bg_color: str = bg_color
        self.__fontname: str = fontname
        self.__font_size: int = self.__checkbox_size_properties[2]
        self.__textcolor: str = textcolor

    def __get_font_size(self) -> int:
        font_size: float = 0.7 * self.__height
        font: pygame.font.Font = pygame.font.SysFont(self.__fontname, int(font_size))
        text: pygame.Surface = font.render(self.__text, True, self.__textcolor)
        while text.get_width() > self.__width - 1.5 * self.__height:
            font_size *= 0.99
            font = pygame.font.SysFont(self.__fontname, int(font_size))
            text = font.render(self.__text, True, self.__textcolor)
        return int(font_size)

    def draw(self, checkbox_size_properties: tuple[tuple[int, int], tuple[int, int], int]) -> None:
        self.__checkbox_size_properties = checkbox_size_properties

        self.__x = self.__checkbox_size_properties[0][0]
        self.__y = self.__checkbox_size_properties[0][1]
        self.__width = self.__checkbox_size_properties[1][0]
        self.__height = self.__checkbox_size_properties[1][1]
        self.__font_size = self.__checkbox_size_properties[2]

        if self.__font_size is None:
            self.__font_size = self.__get_font_size()

        font: pygame.font.Font = pygame.font.SysFont(self.__fontname, self.__font_size)
        text: pygame.Surface = font.render(self.__text, True, self.__textcolor)

        pygame.draw.rect(self.__window, self.__color, (self.__x, self.__y, self.__height, self.__height))
        pygame.draw.rect(self.__window, self.__bg_color, (self.__x + int(0.1 * self.__height),
                                                          self.__y + int(0.1 * self.__height),
                                                          int(0.8 * self.__height), int(0.8 * self.__height)))
        if self.__checked:
            pygame.draw.rect(self.__window, self.__color, (self.__x + int(0.2 * self.__height),
                                                           self.__y + int(0.2 * self.__height),
                                                           int(0.6 * self.__height), int(0.6 * self.__height)))

        self.__window.blit(text, (self.__x + 1.25 * self.__height, self.__y + (self.__height - self.__font_size) / 2))

    def clicked(self, pos: tuple[int, int]) -> None:
        if self.__x <= pos[0] <= self.__x + self.__width and self.__y <= pos[1] <= self.__y + self.__height:
            self.__checked = not self.__checked

    def get_text(self) -> str:
        return self.__text

    def get_checked(self) -> bool:
        return self.__checked
