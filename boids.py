"""
A deliberately bad implementation of [Boids](http://dl.acm.org/citation.cfm?doid=37401.37406)
for use as an exercise on refactoring.
"""

from matplotlib import pyplot as plt
from matplotlib import animation
import os
import numpy as np
import yaml


# Deliberately terrible code for teaching purposes

class Boids:
    def __init__(self, xs, ys, xvs, yvs):
        self.xs = xs
        self.ys = ys
        self.xvs = xvs
        self.yvs = yvs


def init_boids():
    b_init = yaml.load(open(os.path.join(os.path.dirname(__file__), 'init_boids.yaml')), Loader=yaml.FullLoader)
    boids_x = np.random.uniform(b_init['position']['x']['lower'], b_init['position']['x']['upper'],
                                size=b_init['n_sample'])
    boids_y = np.random.uniform(b_init['position']['y']['lower'], b_init['position']['y']['upper'],
                                size=b_init['n_sample'])
    boid_x_velocities = np.random.uniform(b_init['velocity']['x']['lower'], b_init['velocity']['x']['upper'],
                                          size=b_init['n_sample'])
    boid_y_velocities = np.random.uniform(b_init['velocity']['y']['lower'], b_init['velocity']['y']['upper'],
                                          size=b_init['n_sample'])
    return Boids(boids_x, boids_y, boid_x_velocities, boid_y_velocities)


boids = init_boids()


def update_boids(boids):
    # Fly towards the middle
    for i in range(len(boids.xs)):
        for j in range(len(boids.xs)):
            boids.xvs[i] = boids.xvs[i] + (boids.xs[j] - boids.xs[i]) * 0.01 / len(boids.xs)
    for i in range(len(boids.xs)):
        for j in range(len(boids.xs)):
            boids.yvs[i] = boids.yvs[i] + (boids.ys[j] - boids.ys[i]) * 0.01 / len(boids.xs)
    # Fly away from nearby boids
    for i in range(len(boids.xs)):
        for j in range(len(boids.xs)):
            if (boids.xs[j] - boids.xs[i]) ** 2 + (boids.ys[j] - boids.ys[i]) ** 2 < 100:
                boids.xvs[i] = boids.xvs[i] + (boids.xs[i] - boids.xs[j])
                boids.yvs[i] = boids.yvs[i] + (boids.ys[i] - boids.ys[j])
    # Try to match speed with nearby boids
    for i in range(len(boids.xs)):
        for j in range(len(boids.xs)):
            if (boids.xs[j] - boids.xs[i]) ** 2 + (boids.ys[j] - boids.ys[i]) ** 2 < 10000:
                boids.xvs[i] = boids.xvs[i] + (boids.xvs[j] - boids.xvs[i]) * 0.125 / len(boids.xs)
                boids.yvs[i] = boids.yvs[i] + (boids.yvs[j] - boids.yvs[i]) * 0.125 / len(boids.xs)
    # Move according to velocities
    for i in range(len(boids.xs)):
        boids.xs[i] = boids.xs[i] + boids.xvs[i]
        boids.ys[i] = boids.ys[i] + boids.yvs[i]


figure = plt.figure()
axes = plt.axes(xlim=(-500, 1500), ylim=(-500, 1500))
scatter = axes.scatter(boids.xs, boids.ys)


def animate(frame):
    update_boids(boids)
    scatter.set_offsets(list(zip(boids.xs, boids.ys)))


anim = animation.FuncAnimation(figure, animate,
                               frames=50, interval=50)

if __name__ == "__main__":
    plt.show()
