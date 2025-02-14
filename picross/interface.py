import time
import sys
import wrecked
from .board import Board
from .interactor import Interactor

class Session:
    CHR_UNKNOWN = '  '
    #CHR_TRUE = chr(9632)
    CHR_TRUE_ODD = chr(9619) * 2
    CHR_TRUE_EVEN = chr(9618) * 2
    CHR_FALSE = '--'

    CTL_LEFT = "h"
    CTL_RIGHT = "l"
    CTL_UP = "k"
    CTL_DOWN = "j"
    CTL_SET = "x"
    CTL_BLOCK = "z"
    CTL_UNDO = "u"
    CTL_QUIT = "q"

    def __init__(self, **kwargs):
        self.root = wrecked.init()

        width = kwargs.get('width', 15)
        height = kwargs.get('height', 10)
        self.match_board = Board(width, height)
        self.match_board.populate(kwargs.get('density', .5))
        self.game_board = Board(width, height)
        self.playing = False
        self.complete = False

        self.start_time = 0
        self.end_time = 0

        self.cursor_position = 0

        self.rect_wrapper = self.root.new_rect()
        self.rect_row_guides = self.rect_wrapper.new_rect()
        self.rect_column_guides = self.rect_wrapper.new_rect()
        self.rect_board = self.rect_wrapper.new_rect()
        self._rect_guides = [ [], [] ]

        self.cell_rects = {}
        for y in range(height):
            for x in range(width):
                self.cell_rects[(x, y)] = self.rect_board.new_rect()

        self.undo_stack = []

    def undo(self):
        if self.undo_stack:
            x, y, value = self.undo_stack.pop()
            self.game_board.set_cell(x, y, value)
            self.draw_board_cell((y * self.game_board.get_width()) + x)
            self.draw()

    def draw(self):
        self.root.draw()

    def check_complete(self):
        if self.match_board.compare_board(self.game_board):
            self.complete = True
            self.end_time = time.time() - self.start_time

            for rect in self.cell_rects.values():
                rect.set_fg_color(wrecked.BLUE)

            for guide_rects in self._rect_guides:
                for rect in guide_rects:
                    rect.set_fg_color(wrecked.BLUE)

            self.rect_board.set_fg_color(wrecked.BLUE)
            self.draw()

    def set_board_cell(self, value):
        if self.complete:
            return

        board_width = self.game_board.get_width()
        x = self.cursor_position % board_width
        y = self.cursor_position // board_width
        current_value = self.game_board.get_cell_value(x, y)
        self.undo_stack.append((x, y, current_value))

        if current_value == 0 or current_value == value:
            if current_value == value:
                self.game_board.set_cell(x, y, 0)
            else:
                self.game_board.set_cell(x, y, value)
            self.draw_board_cell(self.cursor_position)
            self.draw()
            self.check_complete()

    def set_cursor_position(self, x, y):
        if self.complete:
            return

        original_cursor_position = self.cursor_position
        self.cursor_position = (y * self.game_board.get_width()) + x
        self.keep_cursor_within_bounds()
        self.draw_board_cell(original_cursor_position)
        self.draw_board_cell(self.cursor_position)
        self.draw()

    def move_cursor_up(self):
        if self.complete:
            return

        original_cursor_position = self.cursor_position

        if self.cursor_position < self.game_board.get_width():
            self.cursor_position += self.game_board.get_width() * self.game_board.get_height()
        self.cursor_position -= self.game_board.get_width()

        self.draw_board_cell(original_cursor_position)
        self.draw_board_cell(self.cursor_position)
        self.draw()

    def move_cursor_down(self):
        if self.complete:
            return

        original_cursor_position = self.cursor_position
        self.cursor_position += self.game_board.get_width()

        if self.cursor_position >= self.game_board.get_width() * self.game_board.get_height():
            self.cursor_position -= self.game_board.get_width() * self.game_board.get_height()

        self.draw_board_cell(original_cursor_position)
        self.draw_board_cell(self.cursor_position)
        self.draw()

    def move_cursor_left(self):
        if self.complete:
            return

        original_cursor_position = self.cursor_position
        self.cursor_position -= 1

        if original_cursor_position // self.game_board.get_width() != self.cursor_position // self.game_board.get_width():
            self.cursor_position += self.game_board.get_width()

        self.draw_board_cell(original_cursor_position)
        self.draw_board_cell(self.cursor_position)
        self.draw()

    def move_cursor_right(self):
        if self.complete:
            return

        original_cursor_position = self.cursor_position
        self.cursor_position += 1

        if original_cursor_position // self.game_board.get_width() != self.cursor_position // self.game_board.get_width():
            self.cursor_position -= self.game_board.get_width()

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
            cell.underline()
            self._rect_guides[0][x].set_fg_color(wrecked.BRIGHTWHITE)
            self._rect_guides[1][y].set_fg_color(wrecked.BRIGHTWHITE)
            self._rect_guides[0][x].set_bg_color(wrecked.BRIGHTBLACK)
            self._rect_guides[1][y].set_bg_color(wrecked.BRIGHTBLACK)
        else:
            cell.unset_underline()
            self._rect_guides[0][x].unset_fg_color()
            self._rect_guides[1][y].unset_fg_color()
            self._rect_guides[0][x].unset_bg_color()
            self._rect_guides[1][y].unset_bg_color()

        value = self.game_board.get_cell_value(x, y)
        if value == 2:
            if y % 2 == 0:
                cell_string = self.CHR_TRUE_EVEN
            else:
                cell_string = self.CHR_TRUE_ODD
        elif value == 1:
            cell_string = self.CHR_FALSE
        else:
            cell_string = self.CHR_UNKNOWN

        cell.set_string(0, 0, cell_string)

    def draw_game_board(self):
        border_buffer = 1
        self.rect_wrapper.resize(self.root.width, self.root.height)
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

        self.rect_row_guides.move(border_buffer, max_column_guide_length + border_buffer)
        self.rect_row_guides.resize(max_row_guide_length, self.game_board.get_height())

        self.rect_column_guides.move(border_buffer + max_row_guide_length, border_buffer)
        self.rect_column_guides.resize((self.game_board.get_width() * 3) + 1, max_column_guide_length)

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
            self._rect_guides[1].append(rect_row)

        for x, guide in enumerate(column_guides):
            rect_column = self.rect_column_guides.new_rect()
            rect_column.resize(2, max_column_guide_length)
            rect_column.move(1 + (x * 3), 0)
            if (x % 2 == 0):
                rect_column.invert()
            for _y, n in enumerate(guide):
                y = (max_column_guide_length - len(guide)) + _y
                rect_column.set_string(rect_column.width - len(str(n)), y, str(n))
            self._rect_guides[0].append(rect_column)

        self.rect_board.move(border_buffer + max_row_guide_length, border_buffer + max_column_guide_length)
        self.rect_board.resize(1 + (3 * self.match_board.get_width()), self.match_board.get_height())
        for y in range(self.match_board.get_height()):
            for x in range(self.match_board.get_width() + 1):
                self.rect_board.set_string(3 * x, y, chr(9474))

        for (x, y), state in self.match_board.grid.items():
            self.cell_rects[(x, y)].move(1 + (3 * x), y)
            self.cell_rects[(x, y)].resize(2, 1)
            self.cell_rects[(x, y)].set_string(0, 0, self.CHR_UNKNOWN)

        self.rect_wrapper.resize(
            self.rect_row_guides.width + self.rect_board.width + 2,
            self.rect_column_guides.height + self.rect_board.height + 2
        )

        self.rect_wrapper.move(
            (self.root.width - self.rect_wrapper.width) // 2,
            (self.root.height - self.rect_wrapper.height) // 2
        )

        for x in range(self.rect_wrapper.width - 2):
            self.rect_wrapper.set_string(1 + x, 0, chr(9552))
            self.rect_wrapper.set_string(1 + x, self.rect_wrapper.height - 1, chr(9552))

        for y in range(self.rect_wrapper.height - 2):
            self.rect_wrapper.set_string(0, 1 + y, chr(9553))
            self.rect_wrapper.set_string(self.rect_wrapper.width - 1, 1 + y, chr(9553))

        self.rect_wrapper.set_string(0, 0, chr(9556))
        self.rect_wrapper.set_string(0, self.rect_wrapper.height - 1, chr(9562))
        self.rect_wrapper.set_string(self.rect_wrapper.width - 1, self.rect_wrapper.height - 1, chr(9565))
        self.rect_wrapper.set_string(self.rect_wrapper.width - 1, 0, chr(9559))

    def quit(self):
        self.playing = False
        wrecked.kill()

    def play(self):
        self.draw_game_board()
        self.draw_board_cell(self.cursor_position)
        self.root.draw()

        interactor = Interactor()
        interactor.assign_sequence(
            Session.CTL_LEFT,
            self.move_cursor_left
        )
        interactor.assign_sequence(
            Session.CTL_RIGHT,
            self.move_cursor_right
        )
        interactor.assign_sequence(
            Session.CTL_DOWN,
            self.move_cursor_down
        )
        interactor.assign_sequence(
            Session.CTL_UP,
            self.move_cursor_up
        )
        interactor.assign_sequence(
            Session.CTL_QUIT,
            self.quit
        )
        interactor.assign_sequence(
            Session.CTL_SET,
            self.set_board_cell,
            2
        )
        interactor.assign_sequence(
            Session.CTL_BLOCK,
            self.set_board_cell,
            1
        )
        interactor.assign_sequence(
            Session.CTL_UNDO,
            self.undo
        )


        self.playing = True
        self.start_time = time.time()
        while self.playing:
            interactor.get_input()
        interactor.restore_input_settings()

        if self.complete:
            friendly_time = "%02d:%02d:%02d" % (
                self.end_time // (60 * 60),
                (self.end_time // 60) % 60,
                self.end_time % 60
            )
            print("Completed In %s" % friendly_time)
