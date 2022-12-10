from code.level.particles.Particle import Particle


class AnimationParticle(Particle):
    def __init__(self, pos, animation, animation_speed, destroy_on_end=False):
        super().__init__()
        self.__sprite_type = 'particle'
        self.__animation = animation
        self.__animation_speed = animation_speed
        self.__frame_index = 0
        self.__destroy_on_end = destroy_on_end
        self.__image = self.__animation[0]
        self.__rect = self.__image.get_rect(center=pos)

    @property
    def sprite_type(self):
        return self.__sprite_type

    def animate(self):
        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(self.__animation):
            if self.__destroy_on_end:
                self.kill()
            self.__frame_index = 0
        self.__image = self.__animation[int(self.__frame_index)]
        self.__rect = self.__image.get_rect(center=self.__rect.center)

    @property
    def sprite_type(self):
        return self.__sprite_type

    @sprite_type.setter
    def sprite_type(self, value):
        self.__sprite_type = value

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect
