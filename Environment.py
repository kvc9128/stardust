import random


def calculate_slope(point1, point2):
	"""
	simple calculation of slope = rise/run
	:param point1:
	:param point2:
	:return:
	"""
	x1, y1 = point1[0], point1[1]
	x2, y2 = point2[0], point2[1]
	if y2 - y1 == 0:
		return 1e10  # slope is undefined
	else:
		return (x2 - x1) / (y2 - y1)


def get_robot_corners(cur_pos):
	"""
	given a row and column, attempt toget robot wheel locations (refer to image)
	Robot's position will be determined by the "center". If robot is not placed,
	return -1, else ((x,y), (x,y), (x,y), (x,y))
	read front_left, front_right, back_left, back_right
	:param cur_pos:
	:param row:
	:param col:
	:return:
	"""
	if cur_pos is None:
		return -1
	else:
		row, col = cur_pos[0], cur_pos[1]
		front_left = (row - 1, col - 1)
		front_right = (row - 1, col + 1)
		back_left = (row + 1, col - 1)
		back_right = (row + 1, col - 1)
		return front_left, front_right, back_left, back_right


class Environment:
	def __init__(self, world_length, world_width, max_height=50, max_depth=-50, slope=0.15):
		"""
		:param world_length:
		:param world_width:
		:param max_height:
		:param max_depth:
		"""
		self.R = world_length
		self.C = world_width
		self.slope = slope
		self.max_height = max_height
		self.max_depth = max_depth
		# the default is a flat environment, if you want something else, be sure
		# to explicitly set flat=False *AND* something else to True!
		self.board = self.create_board(flat=False, mostlyFlat=True)
		self.robot_position = None

	def display_world(self):
		if self.board and self.robot_position is None:
			for row in self.board:
				print(row)
		elif self.board and self.robot_position:
			corners = set(get_robot_corners(self.robot_position))
			for i in range(self.R):
				for j in range(self.C):
					if (i,j) in corners:
						print(" W", end="\t\t")
					elif (i,j) == self.robot_position:
						print(" C", end="\t\t")
					else:
						print(self.board[i][j], end="\t")

				print("", end="\n")

	def isValid_row(self, row):
		return not (row == 0 or row == self.R or row == self.R - 1)

	def isValid_col(self, col):
		return not (col == 0 or col == self.C or col == self.C - 1)

	def create_board(self,
	                 flat=True,
	                 horizontalCliff=False,
	                 verticalCliff=False,
	                 planeWest=False,
	                 planeEast=False,
	                 planeNorth=False,
	                 planeSouth=False,
	                 mostlyFlat=False,
	                 crazy=False):

		board = []
		if flat:
			for row in range(self.R):
				row = []
				for col in range(self.C):
					row.append(round(0, 4))
				board.append(row)
			return board
		else:
			# if mostlyFlat:
			# only flat and mostly flat exist
			for row in range(self.R):
				row = []
				for col in range(self.C):
					if random.random() % 2 == 0:
						row.append(round(0 + random.random(), 2))
					else:
						row.append(round(0 - random.random(), 2))
				board.append(row)
			return board

	def place_robot(self, row, col):
		"""
		given a row and column, attempt to place robot_position on the board, refer to image.
		Robot's position will be determined by the "center". If a move is invalid,
		or position is invalid, return False. True if successfully placed.
		:param row:
		:param col:
		:return:
		"""
		if self.isValid_row(row) and self.isValid_col(col):
			self.robot_position = (row, col)
			return True
		else:
			return False

	def move_robot_north(self):
		"""
		given a row and column, attempt to move robot_position one unit north.
		Robot's position will be determined by the "center". If a move is invalid,
		or position is invalid, return False. True if successfully placed.
		:param row:
		:param col:
		:return:
		"""
		cur_pos = self.robot_position
		if cur_pos is None:
			return False
		else:
			row, col = cur_pos[0], cur_pos[1]
			if self.isValid_row(row - 1) and self.isValid_col(col):
				self.robot_position = (row - 1, col)
				return True
			else:
				return False

	def move_robot_east(self):
		"""
		given a row and column, attempt to move robot_position one unit east (right).
		Robot's position will be determined by the "center". If a move is invalid,
		or position is invalid, return False. True if successfully placed.
		:param row:
		:param col:
		:return:
		"""
		cur_pos = self.robot_position
		if cur_pos is None:
			return False
		else:
			row, col = cur_pos[0], cur_pos[1]
			if self.isValid_row(row) and self.isValid_col(col + 1):
				self.robot_position = (row, col + 1)
				return True
			else:
				return False

	def move_robot_south(self):
		"""
		given a row and column, attempt to move robot_position one unit south.
		Robot's position will be determined by the "center". If a move is invalid,
		or position is invalid, return False. True if successfully placed.
		:param row:
		:param col:
		:return:
		"""
		cur_pos = self.robot_position
		if cur_pos is None:
			return False
		else:
			row, col = cur_pos[0], cur_pos[1]
			if self.isValid_row(row + 1) and self.isValid_col(col):
				self.robot_position = (row + 1, col)
				return True
			else:
				return False

	def move_robot_west(self):
		"""
		given a row and column, attempt to move robot_position one unit west (left).
		Robot's position will be determined by the "center". If a move is invalid,
		or position is invalid, return False. True if successfully placed.
		:param row:
		:param col:
		:return:
		"""
		cur_pos = self.robot_position
		if cur_pos is None:
			return False
		else:
			row, col = cur_pos[0], cur_pos[1]
			if self.isValid_row(row) and self.isValid_col(col - 1):
				self.robot_position = (row, col - 1)
				return True
			else:
				return False

	def compute_current_state(self):
		"""
		Since this is a car/4 wheeled ground robot, we only need
		to worry about 2 axes of instability (roll) left-right and
		(pitch) front-back. And of course, these can occur at the
		same time.

		(forward_roll, backward_roll, forward_pitch, backward_pitch) define the
		state of the robot at any time
		:return:forward_roll, backward_roll, forward_pitch, backward_pitch
		"""
		corners = get_robot_corners(self.robot_position)
		if corners == -1:
			return None

		forward_roll = calculate_slope(corners[0], corners[1])
		backward_roll = calculate_slope(corners[2], corners[3])

		forward_pitch = calculate_slope(corners[0], corners[2])
		backward_pitch = calculate_slope(corners[1], corners[3])

		return forward_roll, backward_roll, forward_pitch, backward_pitch

	def calculate_state_change(self, new_point):
		"""
		Since this is a car/4 wheeled ground robot, we only need
		to worry about 2 axes of instability (roll) left-right and
		(pitch) front-back. And of course, these can occur at the
		same time.

		ASSUMES THAT NEW POINT IS A VALID STATE

		(forward_roll, backward_roll, forward_pitch, backward_pitch) define the
		state of the robot at any time
		:return:forward_roll, backward_roll, forward_pitch, backward_pitch
		"""
		current_state = self.compute_current_state()

		projected_corners = get_robot_corners(new_point)
		if projected_corners == -1:
			return None

		forward_roll = calculate_slope(projected_corners[0], projected_corners[1])
		backward_roll = calculate_slope(projected_corners[2], projected_corners[3])

		forward_pitch = calculate_slope(projected_corners[0], projected_corners[2])
		backward_pitch = calculate_slope(projected_corners[1], projected_corners[3])

		projected_state = (forward_roll, backward_roll, forward_pitch, backward_pitch)

		state_change = [
			current_state[0] - projected_state[0],
			current_state[1] - projected_state[1],
			current_state[2] - projected_state[2],
			current_state[3] - projected_state[3],
		]

		return state_change
