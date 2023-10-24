import numpy as np
import math
import random

from Environment import Environment

def main():
	world = Environment(10, 10)
	world.display_world()

	world.place_robot(5, 5)
	world.display_world()

	print("current state = ", world.compute_current_state())
	print("state change if new location is 51, 50")
	print(world.calculate_state_change((6, 5)))


main()