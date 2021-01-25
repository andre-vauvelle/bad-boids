import yaml
import boids
from copy import deepcopy

before = deepcopy(boids.b_init)
boids.update_boids(boids.b_init)
after = boids.b_init
fixture = {"before": before, "after": after}
fixture_file = open("fixture.yml", 'w')
fixture_file.write(yaml.dump(fixture))
fixture_file.close()
