import pygame
import pymunk
import numpy as np
from scipy.interpolate import splprep, splev
import sys
import pymunk.pygame_util

class PhysicsEngine:
    def __init__(self, width, height, gravity):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.gravity = gravity
        self.space = self.create_space(self.gravity)
    
    def create_space(self, gravity):
        """
        build a physics space
        """
        space = pymunk.Space()
        space.gravity = gravity
        return space
    
    def add_ball(self, position, radius, mass, velocity):
        """
        add a ball to the physics space
        """
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        body.position = position
        body.velocity = velocity
        shape = pymunk.Circle(body, radius)
        shape.friction = 0.7
        self.space.add(body, shape)
        

    def generate_spline(self, points, num_points=100):
        """
        add a curved floor to the physics space
        """
        points = np.array(points)
        tck, _ = splprep(points.T, s=0)
        u = np.linspace(0, 1, num_points)
        spline_points = splev(u, tck)
        return list(zip(spline_points[0], spline_points[1]))

    def add_curved_floor(self, points, thickness, frictions):
        """
        add a curved floor to the physics space
        """
        spline_points = self.generate_spline(points)
        for i in range(len(spline_points) - 1):
            segment = pymunk.Segment(self.space.static_body, spline_points[i], spline_points[i + 1], thickness)
            segment.friction = frictions
            self.space.add(segment)

    def add_polygon(self, position, vertices, mass, velocity):
        """
        add a polygon to the physics space
        """
        inertia = pymunk.moment_for_poly(mass, vertices)
        body = pymunk.Body(mass, inertia)
        body.position = position
        body.velocity = velocity
        shape = pymunk.Poly(body, vertices)
        shape.friction = 0.7
        self.space.add(body, shape)
    
    def draw_space(self, screen):
        """
        draw the physics space
        """
        draw_options = pymunk.pygame_util.DrawOptions(screen)
        self.space.debug_draw(draw_options)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))  
            self.space.step(1 / 50.0)  
            self.draw_space(self.screen)  

            pygame.display.flip()
            self.clock.tick(50)  
            


