from code.level.particles.LightParticle import LightParticle
from code.level.particles.ParticleSource import ParticleSource


class LightSource(ParticleSource):
    def __init__(self, pos, outer_diameter=128, outer_color='#f77622', inner_diameter=96, inner_color='#feae34'):
        super().__init__(pos)
        outer_particle = LightParticle(pos, outer_diameter, outer_color, 16, 16)
        inner_particle = LightParticle(pos, inner_diameter, inner_color, 64, 8)
        self.group_manager.add_to_particles(outer_particle)
        self.group_manager.add_to_particles(inner_particle)
        self.particles = [outer_particle, inner_particle]

    def kill(self):
        for particle in self.particles:
            particle.kill()
        super().kill()

    def update(self):
        for particle in self.particles:
            particle.rect.center = self.rect.center
