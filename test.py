import numpy as np
import math
import random

from Environment import Environment

def main():
	world = Environment(10, 10)
	world.display_world()

	world.place_robot(4, 4)
	world.display_world()
	print("current state = ", world.compute_current_state())
	print("projected state one unit south = ", world.calculate_state_change((5, 4)))
	print("moving one unit south")
	world.move_robot_south()
	world.display_world()
	print("current state = ", world.compute_current_state())
	print("projected state one unit south = ", world.calculate_state_change((6, 4)))
	print("moving one unit south")
	world.move_robot_south()
	world.display_world()
	print("current state = ", world.compute_current_state())
	print("projected state one unit south = ", world.calculate_state_change((7, 4)))
	print("moving one unit south")
	world.move_robot_south()
	world.display_world()
	print("current state = ", world.compute_current_state())
	print("projected state one unit south = ", world.calculate_state_change((8, 4)))
	print("moving one unit south")
	world.move_robot_south()
	world.display_world()


main()
