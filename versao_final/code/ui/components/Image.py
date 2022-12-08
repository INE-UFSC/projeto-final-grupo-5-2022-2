from code.library.Resources import Resources
from code.ui.components.UIComponent import UIComponent


class Image(UIComponent):
    def __init__(self, pos_kwargs, image_path):
        super().__init__()
        self.__pos_kwargs = pos_kwargs
        self.__image = Resources().get_sprite(image_path)

    def draw(self):
        rect = self.__image.get_rect(**self.__pos_kwargs)
        self.display_surface.blit(self.__image, rect)
