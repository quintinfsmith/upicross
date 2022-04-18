import random

class IncongruentBoardError(Exception):
    '''Thrown when two boards of different dimentions are compared'''

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = {}

    def set_cell(self, x, y, state):
        self.grid[(x, y)] = state

    def populate(self, density):
        stack = []
        for i in range(self.width * self.height):
            stack.append(0)
        for i in range(int(density * self.width * self.height)):
            stack[i] = 2

        for i in range(4):
            random.shuffle(stack)

        for y in range(self.height):
            for x in range(self.width):
                self.set_cell(x, y, stack.pop())

    def get_cell_value(self, x, y):
        return self.grid.get((x, y), 0)

    def get_row_guide(self, row):
        output = []
        current_count = None
        for x in range(self.width):
            if self.get_cell_value(x, row) == 2:
                if current_count is None:
                    current_count = 0
                current_count += 1
            else:
                if current_count is not None:
                    output.append(current_count)
                current_count = None

        if current_count is not None:
            output.append(current_count)

        return output

    def get_column_guide(self, column):
        output = []
        current_count = None
        for y in range(self.height):
            if self.get_cell_value(column, y) == 2:
                if current_count is None:
                    current_count = 0
                current_count += 1
            else:
                if current_count is not None:
                    output.append(current_count)
                current_count = None

        if current_count is not None:
            output.append(current_count)

        return output

    def compare_board(self, board):
        if not (board.get_width() == self.get_width() and board.get_height() == self.get_height()):
            raise IncongruentBoardError()

        output = True
        for x in range(self.get_width()):
            this_column = self.get_column_guide(x)
            that_column = board.get_column_guide(x)
            if len(this_column) != len(that_column):
                output = False
                break

            for i in range(len(this_column)):
                if this_column[i] != that_column[i]:
                    output = False
                    break
        if output:
            for y in range(self.get_height()):
                this_row = self.get_row_guide(y)
                that_row = board.get_row_guide(y)
                if len(this_row) != len(that_row):
                    output = False
                    break

                for i in range(len(this_row)):
                    if this_row[i] != that_row[i]:
                        output = False
                        break
        return output

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def __str__(self):
        rows = []
        max_row_len = 0
        for y in range(self.height):
            rowstring = str(self.get_row_guide(y))
            max_row_len = max(len(rowstring), max_row_len)
            rows.append(rowstring)

        for y, string in enumerate(rows):
            rows[y] = " " * (max_row_len - len(string)) + string

        columns = []
        for x in range(self.width):
            for n in self.get_column_guide(x):
                columns.append(self.get_column_guide(x))

        output = (" " * max_row_len) + ("--" * self.width) + "-\n"
        for y in range(self.height):
            output += str(rows[y]) + "|"
            for x in range(self.width):
                value = self.get_cell_value(x, y)
                if value == 2:
                    output += "#|"
                elif value == 1:
                    output += ".|"
                else:
                    output += " |"
            output += "\n" + (" " * max_row_len) + "|" + ("--" * (self.width - 1)) + "-|\n"
        return output[0:-1]


class Cursor:
    def __init__(self, board):
        self.board = board
        self.cursor_position = 0

    def keep_cursor_within_bounds(self):
        self.cursor_position = max(0, self.cursor_position)
        length = self.board.get_width() * self.board.get_height()
        self.cursor_position = min(length - 1, self.cursor_position)

    def set_cursor_position(self, x, y):
        self.cursor_position = (y * self.board.get_width()) + x
        self.keep_cursor_within_bounds()

    def move_cursor_up(self):
        self.cursor_position -= self.board.get_width()
        self.keep_cursor_within_bounds()

    def move_cursor_down(self):
        self.cursor_position += self.board.get_width()
        self.keep_cursor_within_bounds()

    def move_cursor_left(self):
        self.cursor_position -= 1
        self.keep_cursor_within_bounds()

    def move_cursor_right(self):
        self.cursor_position += 1
        self.keep_cursor_within_bounds()


if __name__ == "__main__":
    board = Board(15, 10)
    board.populate(.50)
    print(board)
