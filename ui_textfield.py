import pygame


class Textfield:
    def __init__(self, window: pygame.Surface, text: str = "", fontname: str = "Arial", textcolor: str = "black",
                 bg_color: str = "white", border_color: str = "gray83", placeholder: str = "Notes",
                 placeholder_color: str = "gray50") -> None:
        self.__window: pygame.Surface = window

        self.__textfield_size_properties: tuple[tuple[int, int], tuple[int, int], int] = ((0, 0), (0, 0), 0)

        self.__x = self.__textfield_size_properties[0][0]
        self.__y = self.__textfield_size_properties[0][1]
        self.__width = self.__textfield_size_properties[1][0]
        self.__height = self.__textfield_size_properties[1][1]
        self.__font_size = self.__textfield_size_properties[2]

        self.__text: str = text
        self.__fontname: str = fontname
        self.__font_size: int = self.__textfield_size_properties[2]
        self.__textcolor: str = textcolor
        self.__bg_color: str = bg_color
        self.__border_color: str = border_color
        self.__cursor_index: int = len(self.__text)
        self.__placeholder: str = placeholder
        self.__placeholder_color: str = placeholder_color

        self.__active: bool = False

    def __get_font_size(self) -> int:
        font_size: float = 0.8 * self.__height
        font: pygame.font.Font = pygame.font.SysFont(self.__fontname, int(font_size))
        if self.__text:
            text: pygame.Surface = font.render(self.__text, True, self.__textcolor)
        else:
            text: pygame.Surface = font.render(self.__placeholder, True, self.__placeholder_color)
        while text.get_width() > self.__width - 0.5 * self.__height:
            font_size *= 0.99
            font = pygame.font.SysFont(self.__fontname, int(font_size))
            if self.__text:
                text = font.render(self.__text, True, self.__textcolor)
            else:
                text = font.render(self.__placeholder, True, self.__placeholder_color)
        return int(font_size)

    def __get_text_surface(self) -> tuple[pygame.font, pygame.Surface]:
        font: pygame.font.Font = pygame.font.SysFont(self.__fontname, self.__font_size)
        if self.__text:
            return font, font.render(self.__text, True, self.__textcolor)
        return font, font.render(self.__placeholder, True, self.__placeholder_color)

    def __get_cursor_rect(self) -> pygame.Rect:
        font, text_surface = self.__get_text_surface()
        cursor_x: int = (self.__x + 0.25 * self.__height
                         + text_surface.get_rect().left + font.size(self.__text[:self.__cursor_index])[0])
        cursor_y: int = self.__y + (self.__height - self.__font_size) / 2 + text_surface.get_rect().top
        cursor_height: int = text_surface.get_height()
        return pygame.Rect(cursor_x, cursor_y, 2, cursor_height)

    def __draw_cursor(self):
        pygame.draw.rect(self.__window, "black", self.__get_cursor_rect())

    def draw(self, textfield_size_properties: tuple[tuple[int, int], tuple[int, int], int]) -> None:
        self.__textfield_size_properties = textfield_size_properties

        self.__x = self.__textfield_size_properties[0][0]
        self.__y = self.__textfield_size_properties[0][1]
        self.__width = self.__textfield_size_properties[1][0]
        self.__height = self.__textfield_size_properties[1][1]
        self.__font_size = self.__textfield_size_properties[2]

        if self.__font_size is None:
            self.__font_size = self.__get_font_size()

        _, text_surface = self.__get_text_surface()

        pygame.draw.rect(self.__window, self.__bg_color, (self.__x, self.__y, self.__width, self.__height))
        pygame.draw.rect(self.__window, self.__border_color, (self.__x, self.__y, self.__width, self.__height), 1)

        #text_rect: pygame.Rect = text_surface.get_rect()
        #text_rect.center = self.__rect.center
        #self.__window.blit(text_surface, text_rect)

        self.__window.blit(text_surface,
                           (self.__x + 0.25 * self.__height, self.__y + (self.__height - self.__font_size) / 2))

        if pygame.time.get_ticks() % 1000 < 500 and self.__active:
            self.__draw_cursor()

    def clicked(self, pos) -> bool:
        if self.__x <= pos[0] <= self.__x + self.__width and self.__y <= pos[1] <= self.__y + self.__height:
            self.__active = True
            return True
        self.__active = False
        return False

    def handle_key(self, key: pygame.key, event: pygame.event.Event) -> None:
        if self.__active:
            if key == pygame.K_LEFT:
                self.__cursor_index = max(0, self.__cursor_index - 1)
            elif key == pygame.K_RIGHT:
                self.__cursor_index = min(len(self.__text), self.__cursor_index + 1)
            elif key == pygame.K_BACKSPACE:
                if self.__cursor_index > 0:
                    self.__text = self.__text[:self.__cursor_index - 1] + self.__text[self.__cursor_index:]
                    self.__cursor_index -= 1
            elif key == pygame.K_DELETE:
                if self.__cursor_index < len(self.__text):
                    self.__text = self.__text[:self.__cursor_index] + self.__text[self.__cursor_index + 1:]
            else:
                self.__text = self.__text[:self.__cursor_index] + event.unicode + self.__text[self.__cursor_index:]
                self.__cursor_index += 1

    def set_active(self, active: bool = True) -> None:
        self.__active = active

    def is_active(self) -> bool:
        return self.__active

    def set_text(self, text: str) -> None:
        self.__text = text

    def get_text(self) -> str:
        return self.__text
