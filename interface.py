from board import Board
from interactor import Interactor
import wrecked
import time

class Session:
    def __init__(self, **kwargs):
        self.root = wrecked.init()

        width = kwargs.get('width', 15)
        height = kwargs.get('height', 10)
        self.match_board = Board(width, height)
        self.match_board.populate(kwargs.get('density', .5))
        self.game_board = Board(width, height)
        self.playing = False
        self.complete = False

        self.cursor_position = 0

        self.rect_row_guides = self.root.new_rect()
        self.rect_column_guides = self.root.new_rect()
        self.rect_board = self.root.new_rect()
        #self.layer_board = self.rect_board.new_rect()
        #self.layer_board.set_transparency(True)
        #self.rect_cursor = self.layer_board.new_rect()

        self.cell_rects = {}
        for y in range(height):
            for x in range(width):
                self.cell_rects[(x, y)] = self.rect_board.new_rect()

    def keep_cursor_within_bounds(self):
        self.cursor_position = max(0, self.cursor_position)
        length = self.game_board.get_width() * self.game_board.get_height()
        self.cursor_position = min(length - 1, self.cursor_position)

    def draw(self):
        self.root.draw()

    def check_complete(self):
        if self.match_board.compare_board(self.game_board):
            self.complete = True
            self.quit()

    def set_board_cell(self, value):
        board_width = self.game_board.get_width()
        x = self.cursor_position % board_width
        y = self.cursor_position // board_width
        self.game_board.set_cell(x, y, value)
        self.draw_board_cell(self.cursor_position)
        self.draw()
        self.check_complete()

    def set_cursor_position(self, x, y):
        original_cursor_position = self.cursor_position
        self.cursor_position = (y * self.game_board.get_width()) + x
        self.keep_cursor_within_bounds()
        self.draw_board_cell(original_cursor_position)
        self.draw_board_cell(self.cursor_position)
        self.draw()

    def move_cursor_up(self):
        original_cursor_position = self.cursor_position
        self.cursor_position -= self.game_board.get_width()
        self.keep_cursor_within_bounds()
        self.draw_board_cell(original_cursor_position)
        self.draw_board_cell(self.cursor_position)
        self.draw()

    def move_cursor_down(self):
        original_cursor_position = self.cursor_position
        self.cursor_position += self.game_board.get_width()
        self.keep_cursor_within_bounds()
        self.draw_board_cell(original_cursor_position)
        self.draw_board_cell(self.cursor_position)
        self.draw()

    def move_cursor_left(self):
        original_cursor_position = self.cursor_position
        self.cursor_position -= 1
        self.keep_cursor_within_bounds()
        self.draw_board_cell(original_cursor_position)
        self.draw_board_cell(self.cursor_position)
        self.draw()

    def move_cursor_right(self):
        original_cursor_position = self.cursor_position
        self.cursor_position += 1
        self.keep_cursor_within_bounds()
        self.draw_board_cell(original_cursor_position)
        self.draw_board_cell(self.cursor_position)
        self.draw()

    def draw_board_cell(self, offset):
        board_width = self.game_board.get_width()
        cursor_x = self.cursor_position % board_width
        cursor_y = self.cursor_position // board_width
        x = offset % board_width
        y = offset // board_width

        cell = self.cell_rects[(x, y)]
        if cursor_x == x and cursor_y == y:
            cell.invert()
        else:
            cell.unset_invert()

        value = self.game_board.get_cell_value(x, y)
        #value = self.match_board.get_cell_value(x, y)
        if value == 2:
            cell_string = "#"
        elif value == 1:
            cell_string = "."
        else:
            cell_string = " "

        cell.set_string(0, 0, cell_string)

    def draw_game_board(self):
        row_guides = []
        max_row_guide_length = 0
        for y in range(self.match_board.get_height()):
            guide = self.match_board.get_row_guide(y)
            test_string = ""
            for n in guide:
                test_string += str(n) + " "
            test_string = test_string[0:-1]
            max_row_guide_length = max(len(test_string), max_row_guide_length)
            row_guides.append(guide)


        column_guides = []
        max_column_guide_length = 0
        for x in range(self.match_board.get_width()):
            guide = self.match_board.get_column_guide(x)
            max_column_guide_length = max(len(guide), max_column_guide_length)
            column_guides.append(guide)

        self.rect_row_guides.move(0, max_column_guide_length)
        self.rect_row_guides.resize(max_row_guide_length, (self.game_board.get_width() * 2) + 1)

        self.rect_column_guides.move(max_row_guide_length, 0)
        self.rect_column_guides.resize((self.game_board.get_width() * 2) + 1, max_column_guide_length)

        for y, guide in enumerate(row_guides):
            rect_row = self.rect_row_guides.new_rect()
            rect_row.resize(self.rect_row_guides.width, 1)
            rect_row.move(0, y)
            if y % 2 == 0:
                rect_row.invert()

            string = ""
            for n in guide:
                string += str(n) + " "
            string = string[0:-1]
            rect_row.set_string(rect_row.width - len(string), 0, string)

        for x, guide in enumerate(column_guides):
            rect_column = self.rect_column_guides.new_rect()
            rect_column.resize(2, max_column_guide_length)
            rect_column.move((x * 2), 0)
            if (x % 2 == 0):
                rect_column.invert()
            for _y, n in enumerate(guide):
                y = (max_column_guide_length - len(guide)) + _y
                rect_column.set_string(rect_column.width - len(str(n)), y, str(n))

        self.rect_board.move(max_row_guide_length, max_column_guide_length)
        self.rect_board.resize(1 + (2 * self.match_board.get_width()), self.match_board.get_height())
        for y in range(self.match_board.get_height()):
            for x in range(self.match_board.get_width() + 1):
                self.rect_board.set_string(2 * x, y, chr(9474))

        for (x, y), state in self.match_board.grid.items():
            self.cell_rects[(x, y)].move(1 + (2 * x), y)
    def quit(self):
        self.playing = False
        wrecked.kill()

    def play(self):
        self.draw_game_board()
        self.draw_board_cell(self.cursor_position)
        self.root.draw()

        interactor = Interactor()
        interactor.assign_sequence(
            "h",
            self.move_cursor_left
        )
        interactor.assign_sequence(
            "l",
            self.move_cursor_right
        )
        interactor.assign_sequence(
            "j",
            self.move_cursor_down
        )
        interactor.assign_sequence(
            "k",
            self.move_cursor_up
        )
        interactor.assign_sequence(
            "q",
            self.quit
        )
        interactor.assign_sequence(
            "b",
            self.set_board_cell,
            2
        )
        interactor.assign_sequence(
            "n",
            self.set_board_cell,
            1
        )
        interactor.assign_sequence(
            " ",
            self.set_board_cell,
            0
        )


        start = time.time()
        self.playing = True
        while self.playing:
            interactor.get_input()
        interactor.restore_input_settings()

        if self.complete:
            end  = time.time() - start
            print("Completed In %d" % end)

if __name__ == "__main__":
    session = Session(width=15, height=10, density=.65)
    session.play()

