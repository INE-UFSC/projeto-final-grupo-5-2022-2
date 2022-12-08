import random

from code.level.particles.FireParticle import FireParticle
from code.level.particles.ParticleSource import ParticleSource


class FireSource(ParticleSource):
    def __init__(self, pos):
        super().__init__(pos)
        self.__offset = 16

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, offset):
        self.__offset = offset

    def update(self):
        # criar as partículas de fogo
        for i in range(random.randint(1, 3)):
            x_offset = random.randint(-self.offset, self.offset)
            y_offset = random.randint(-self.offset, self.offset)
            particle = FireParticle((self.rect.centerx + x_offset, self.rect.centery + y_offset))
            self.group_manager.add_to_particles(particle)
