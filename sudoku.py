def abs(a, b):
	if a > b:
		return a - b
	return b - a

class Sudoku(object):

	def __init__(self, array):
		self.field = array
		self.worksheet = [[] for i in range(9)]
		self.standart_square = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
		for i in range(9):
			for q in range(9):
				if array[i][q] != "0":
					square_number = (q // 3 + 1) + 3 * (i // 3) 
					member = int(array[i][q]) - 1
					self.worksheet[member].append([i, q, square_number])


	def squares_which_affect_function(self, square_number, squares_with_number): 
		squares_which_affect = []  						
		for i in range(3):
			for q in range(3):
				if self.standart_square[i][q] == square_number:
					y, x = i, q
					break
		for i in range(3):
			if self.standart_square[y][i] != square_number and self.standart_square[y][i] in squares_with_number:
				squares_which_affect.append(self.standart_square[y][i])
		for i in range(3):
			if self.standart_square[i][x] != square_number and self.standart_square[i][x] in squares_with_number:
				squares_which_affect.append(self.standart_square[i][x])	
		return squares_which_affect
	
	def square_creating_by_number(self, square_number):
		area = []
		for y in range(3):
			area.append([])
			for x in range(3): 
				area[y].append(self.field[(square_number - 1) // 3 * 3 + y][(square_number - 1) % 3 * 3 + x])
		return area

	def two_d_slice(self, square, axis, number):
		number = number % 3
		if axis == 'hor':
			square[number] = ['*' for i in range(len(square[0]))]
		elif axis == 'ver':
			for i in range(3):
				square[i][number] = '*'
		return square

	def count_of_zeros_in_array_function(self, array):
		result = 0
		y, x = 0, 0
		for i in range(len(array)):
			for q in range(len(array[0])):
				if array[i][q] == '0':
					result += 1
					y, x = i, q
		return result, y, x


	def algorhitm_2(self):
		counter = 0
		for i in range(9):

			squares_with_number = sorted([self.worksheet[i][q][2] for q in range(len(self.worksheet[i]))]) 
			squares_without_number = [] 
			for q in range(9):
				if not (q + 1) in squares_with_number:
					squares_without_number.append(q + 1)

			for q in range(len(squares_without_number)): 
				this_square_number = squares_without_number[q] 
				square_this = self.square_creating_by_number(this_square_number) 
				squares_which_affect = self.squares_which_affect_function(squares_without_number[q],squares_with_number)

				for j in range(len(self.worksheet[i])): 
					if not self.worksheet[i][j][2] in squares_which_affect:
						continue

					affect_square_number = self.worksheet[i][j][2]

					if abs(this_square_number, affect_square_number) == 1 or abs(this_square_number, affect_square_number) == 2:
						square_this = self.two_d_slice(square_this, 'hor', self.worksheet[i][j][0]) 
						
					else:
						square_this = self.two_d_slice(square_this, 'ver', self.worksheet[i][j][1]) 

				number, y, x = self.count_of_zeros_in_array_function(square_this)

				if number != 1:
					continue
				y = (this_square_number - 1) // 3 * 3 + y
				x = (this_square_number - 1) % 3 * 3 + x
				self.field[y][x] = i + 1
				counter += 1
				self.worksheet[i].append([y, x, this_square_number])

		return counter

	def algorhitm_1_secondary(self, y, x): 
		line = self.field[y]
		column = [self.field[i][x] for i in range(9)]
		square = []
		for i in range(y - y % 3, y + 3 - y % 3):   
			square.append(self.field[i][x - x % 3 : x + 3 - x % 3])
		
		control_number = 0
		for i in range(9):
			if (str(i + 1) in line) or (str(i + 1) in column) or (str(i + 1) in square):
				continue
			else:
				if control_number == 0:
					control_number = i + 1
				else:
					return 0
		return control_number 

	def algorhitm_1(self):

		counter = 0
		for i in range(9):
			for q in range(9):
				if self.field[i][q] != '0':
					continue
				candidate = self.algorhitm_1_secondary(i, q)
				if candidate > 0:
					self.field[i][q] = candidate
					counter += 1
					self.worksheet[candidate - 1].append([i, q, (q // 3 + 1) + 3 * (i // 3)])
		return counter

	def main_solution(self):

		counter = 1     
		while counter > 0:
			counter = 0
			counter += self.algorhitm_1()
			counter += self.algorhitm_2()
		return self.field

Field = [['0' for i in range(9)] for i in range (9)]
for i in range(9):
	m = list(input())
	for q in range(9):
		Field[i][q] = m[q]

Sudoku1 = Sudoku(Field)
Sudoku1.main_solution()
print()
print('Solution: ')

for i in range(9):
	for q in range(9):
		if (q + 1) % 3 == 0:
			print(Sudoku1.field[i][q], end = '  ')
		else:
			print(Sudoku1.field[i][q], end = ' ')
	if (i + 1) % 3 == 0:
		print()
	print()