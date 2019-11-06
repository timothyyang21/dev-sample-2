'''
Author: Timothy Yang
Date: October 2019
Project: Improved Row Reduction game
'''

# Black represents leading entry (1)
# White represents non-leading entry (2)
# This game is designed to teach people to row-reduce to row-reduced echelon form
# This game would 

# Usage:
# python3 start_game.py x
#
# Example:
# python3 start_game.py 2

import pygame
import constants as cs
import math, random
import numpy

class Game:
    def __init__(self, board_size=4):

        if board_size > 14 or board_size < 2:
            print('board size must be between 2 and 14')
            return

        self.board_size = board_size
        self.block_size = (cs.grid_right - cs.grid_left)//board_size - 2
        self.radius = int(self.block_size/3)
        self.random_game = False  # Initialize this value to false
        

    def init(self):

        self.grid = self.init_grid()
        self.buttons = self.init_buttons()
        self.texts = self.init_texts()

        self.step = 0
        self.chosen = []
        self.start_time = pygame.time.get_ticks()
        self.rand_grid()

    def start(self):

        pygame.init()
        pygame.display.set_caption("game")
        self.screen = pygame.display.set_mode([cs.window_size, cs.window_size])

        self.init()
        clock = pygame.time.Clock()

        done = False
        solved = False
        
        while not done:

            self.screen.fill(cs.grey)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.click_button(pos)

                    if self.is_goal():
                        self.texts[0][3] = 'Congratulations! You solved the puzzle!'
                        solved = True

                if not solved:
                    self.texts[1][3] = 'Time: ' + str(int((pygame.time.get_ticks() - self.start_time)/1000)) + ' s, ' + \
                        'Steps: ' + str(self.step)
                self.draw(self.screen)
                
                # pygame.display.update()
                pygame.display.flip()
                clock.tick(60)

        pygame.quit()

    def is_goal(self):

        count = 0
        goal = False # Initializes a local variable of the goal itself

        # This is the checking condition for normal game
        if not self.random_game:
            for row in range(self.board_size):
                for col in range(self.board_size):

                    color = self.grid[row][col][2]
                    # the original goal
                    if color == 0:
                        return False # whenever there is white, this is false.
                    elif color == 1:
                        count += 1

                    # if color != -1:
                    #     count += 1

            if count <= self.board_size:
                goal = True
            else:
                goal = False

        # This is the checking condition for random game
        # -1 is zero, 0 is white, 1 is black
        if self.random_game:

            current_row_color = []
            prev_row_color = []

            current_leading_entry_place = 0
            prev_leading_entry_place = 0


            all_0_row_example = []
            already_done_once = False
            nonzero_entries = 0

            ##### This checks the rows for row related conditions
            for row in range(self.board_size):

                first_black_found = False
                first_white_found = False
                first_black_entry_place = 0
                first_white_entry_place = 0
                black = 0
                white = 0

                for col in range(self.board_size):

                    color = self.grid[row][col][2]
                    current_row_color.append(color) # Stores the color into the row for that specific column spot
                    if color == 1:
                        count += 1
                        black += 1 # black are leading entries, should only have 1 in each row.
                        
                        if not first_black_found:
                            first_black_entry_place = col # This keeps track of the first leading entry position
                            first_black_found = True
                        
                    if color == 0:
                        white += 1
                        
                        if not first_white_found:
                            first_white_entry_place = col # This keeps track of the first non-leading entry position
                            first_white_found = True

                # Should only have 1 or fewer leading entry (black per row
                if black > 1:
                    return False

                # Cannot have a row with only white entries and no black entries
                if black == 0 and white >= 1:
                    return False

                # The first leading entry (black) should always go before the first nonleading_entry
                if first_white_entry_place > 0:
                    if first_black_entry_place > first_white_entry_place:
                        return False

            ##### This checks the columns for column related conditions
            for col in range(self.board_size):

                black = 0
                white = 0
                first_black_found = False
                first_black_entry_place = 0

                for row in range(self.board_size):

                    color = self.grid[row][col][2]
                    current_row_color.append(color) # Stores the color into the column for that specific row spot
                    if color == 1:
                        black += 1 # black are leading entries, should only have 1 in each column.

                        if not first_black_found:
                            first_black_entry_place = row # This keeps track of the first leading entry position

                            # The first leading entry (black) of the column should correspond to the column # itself
                            if first_black_entry_place != col:
                                return False

                            first_black_found = True
                        
                    if color == 0:
                        white += 1

                # Should only have 1 or fewer black per column
                if black > 1:
                    return False

                # If there are a leading entry in one column or no leading entries at all, there should be no other white entries
                if black <= 1 and white >= 1:
                	return False

            if count <= self.board_size:
                goal = True
            else:
                goal = False

        return (goal)

    def click_button(self, pos):

        px, py = pos
        clicked = -1
        for i in range(len(self.buttons)):
            x, y, color, text, width, height = self.buttons[i]
            if x <= px <= x + width and y <= py <= y + height:
                clicked = i
                # print('clicked: ', clicked)
                break

        # Select
        if 0 <= clicked < self.board_size:

            if not self.chosen:
                self.chosen.append(clicked)
                self.buttons[clicked] = [x, y, cs.green, '1', width, height]

            elif len(self.chosen) == 1:
                if clicked == self.chosen[0]:
                    self.buttons[clicked][3] = '1 & 2'
                else:
                    self.buttons[clicked] = [x, y, cs.green, '2', width, height]
                self.chosen.append(clicked)

        # Cancel
        elif self.board_size <= clicked < 2*self.board_size:

            clicked = clicked - self.board_size
            x, y, color, text, width, height = self.buttons[clicked]

            if len(self.chosen) == 1 and clicked == self.chosen[0]:
                self.buttons[clicked] = [x, y, cs.milk_blue, 'select', width, height]
                self.chosen = []

            elif len(self.chosen) == 2:
                if clicked == self.chosen[0]:
                    if self.chosen[0] == self.chosen[1]:
                        self.buttons[clicked] = [x, y, cs.milk_blue, 'select', width, height]
                        self.chosen = []
                    else:
                        self.buttons[clicked] = [x, y, cs.milk_blue, 'select', width, height]
                        prev2 = self.chosen[1]
                        self.buttons[prev2][3] = '1'
                        self.chosen = [prev2]
                elif clicked == self.chosen[1]:
                    self.buttons[clicked] = [x, y, cs.milk_blue, 'select', width, height]
                    self.chosen = [self.chosen[0]]

        # Swap
        elif clicked == 2*self.board_size:

            if len(self.chosen) != 2:

                self.texts[0][3] = 'please select exactly two rows'

            else:
                self.swap_rows(self.chosen[0], self.chosen[1])
                self.texts[0][3] = ''
                self.step += 1

        # Add
        elif clicked == 2*self.board_size + 1:

            if len(self.chosen) != 2:
                if not self.texts:
                    self.texts.append([])
                self.texts[0][3] = 'please select exactly two rows'

            else:
                self.add_rows(self.chosen[0], self.chosen[1])
                self.texts[0][3] = ''
                self.step += 1

        # New game
        elif clicked == 2*self.board_size + 2:

            self.init()

        # Impossible - If it is possible, won't respond
        elif clicked == 2*self.board_size + 3:

            if self.random_game == True:
        	    self.init()        

    def add_init(self, row1, row2):
        # add rows
        # -1: empty, 0: white, 1: black 
        for i in range(self.board_size):
            c1, c2 = self.grid[row1][i][2], self.grid[row2][i][2]
            if c1 == -1:
                continue
            elif c1 == c2:
                self.grid[row2][i][2] = 1 - c2
            elif c2 == -1:
                self.grid[row2][i][2] = c1
            else: # 1 black 1 white
                self.grid[row2][i][2] = -1

    def add_rows(self, row1, row2):
        # add rows
        # -1: empty, 0: white, 1: black 
        for i in range(self.board_size):
            c1, c2 = self.grid[row1][i][2], self.grid[row2][i][2]
            if c1 == -1:
                continue
            elif c1 == c2:
                self.grid[row2][i][2] = 1 - c2
            elif c2 == -1:
                self.grid[row2][i][2] = c1
            else: # 1 black 1 white
                self.grid[row2][i][2] = -1
        
        # change buttons
        self.buttons[self.chosen[0]][2] = cs.milk_blue
        self.buttons[self.chosen[0]][3] = 'select'
        self.buttons[self.chosen[1]][2] = cs.milk_blue
        self.buttons[self.chosen[1]][3] = 'select'
        self.chosen = []

    def swap_init(self, row1, row2):
        # swap rows
        for i in range(self.board_size):
            self.grid[row1][i][2], self.grid[row2][i][2] = self.grid[row2][i][2], self.grid[row1][i][2]


    def swap_rows(self, row1, row2):
        # swap rows
        for i in range(self.board_size):
            self.grid[row1][i][2], self.grid[row2][i][2] = self.grid[row2][i][2], self.grid[row1][i][2]
        
        # change buttons
        self.buttons[self.chosen[0]][2] = cs.milk_blue
        self.buttons[self.chosen[0]][3] = 'select'
        self.buttons[self.chosen[1]][2] = cs.milk_blue
        self.buttons[self.chosen[1]][3] = 'select'
        self.chosen = []

    # [x, y, color]
    # -1: empty, 0: white, 1: black 
    def init_grid(self):

        grid = []

        rand_1 = random.uniform(0, 1)

        # 60% of the time there's a diagonal, 40% of the time completely random.
        # basically have a random thingy to give two conditions.
        if rand_1 <= 0.6:

            print("We are in normal game.")
            self.random_game = False
            for y in range(self.board_size):
                grid.append([])
                for x in range(self.board_size):
                    if x == y: # diagonal: black
                        color = 1
                    elif x > y:
                        rand = random.uniform(0, 1)

                        if rand <= 1/4:
                            color = 1
                        elif rand <= 2/3:
                            color = 0
                        else:
                            color = -1
                    else:
                        color = -1

                    grid[y].append([cs.grid_left + x* (self.block_size + 2), \
                        cs.grid_top + y* (self.block_size + 2), color])

        # 40% of the time completely random.
        else:

            print("We are in random game. ####################################")
            self.random_game = True
            for y in range(self.board_size):
                grid.append([])
                for x in range(self.board_size):

                    rand = random.uniform(0, 1)

                    # completely random, equally divided among the 3 values
                    if rand <= 1/3:
                        color = 1
                    elif rand > 1/3 and rand <= 2/3:
                        color = 0
                    else:
                        color = -1

                    grid[y].append([cs.grid_left + x * (self.block_size + 2), \
                                    cs.grid_top + y * (self.block_size + 2), color])

        return grid

    def rand_grid(self):

        l = list(range(self.board_size))

        for i in range(2*self.board_size):
            rand = random.uniform(0, 1)
            random.shuffle(l)
            row1, row2 = l[0], l[1]
            # print (row1, row2)
            if rand <= 0.5:
                self.add_init(row1, row2)
            else:
                self.swap_init(row1, row2)

    # [x, y, color, string, width, height]
    def init_buttons(self):

        buttons = []
        diff = cs.window_size-cs.grid_right
        for y in range(self.board_size):
            buttons.append([cs.grid_right+int((1/6)*diff), \
                    cs.grid_top + y*(self.block_size+2)+12, cs.milk_blue, 'select', int(0.28*diff), 25])
        
        for y in range(self.board_size):
            buttons.append([cs.grid_right+int((1/2)*diff), \
                    cs.grid_top + y*(self.block_size+2)+12, cs.milk_blue, 'cancel', int(0.28*diff), 25])

        buttons.append([int(0.4 * cs.window_size), int(cs.grid_bottom + 0.3 * (cs.window_size - cs.grid_bottom)), \
            cs.milk_blue, 'swap', 60, 30])

        buttons.append([int(0.6 * cs.window_size), int(cs.grid_bottom + 0.3 * (cs.window_size - cs.grid_bottom)), \
            cs.milk_blue, 'add', 60, 30])

        buttons.append([int(0.8 * cs.window_size), int(cs.grid_bottom + 0.3 * (cs.window_size - cs.grid_bottom)), \
            cs.milk_blue, 'new game', 80, 30])

        buttons.append([int(0.1 * cs.window_size), int(cs.grid_bottom + 0.3 * (cs.window_size - cs.grid_bottom)), \
            cs.milk_blue, 'impossible', 100, 30])

        return buttons

    def init_texts(self):

        texts = [[int(0.5 * cs.window_size), int(0.3 * cs.grid_top), cs.pink, ''], \
        [int(0.5 * cs.window_size), int(0.6 * cs.grid_top), cs.pink, 'Time: ' + str(0) + ' s']]
        return texts

    def draw(self, screen):

        for row in self.grid:
            for block in row:
                x, y, color = block
        
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(screen, cs.wood, rect)
        
                if color == 0:
                    pygame.draw.circle(screen, cs.white, (x + int(0.5*self.block_size), \
                        y + int(0.5*self.block_size)), self.radius, 0)
                elif color == 1:
                    pygame.draw.circle(screen, cs.black, (x + int(0.5*self.block_size), \
                        y + int(0.5*self.block_size)), self.radius, 0)

        ####### This part is for specializations of the images and personalizations, but for now this works best for 2x2, uncomment to use it & comment the above
        # for row in self.grid:
        #     for block in row:
        #         x, y, color = block

        #         rect = pygame.Rect(x, y, self.block_size, self.block_size)
        #         pygame.draw.rect(screen, cs.wood, rect)

        #         if color == 0:
        #             white_sprite = pygame.transform.scale((pygame.image.load("Princey.png").convert_alpha()),
        #                                     (int((cs.grid_right - cs.grid_left) * 0.4), int((cs.grid_bottom - cs.grid_top) * 0.4)))
        #             screen.blit(white_sprite, (x + int(0.1*self.block_size), \
        #                 y + int(0.1*self.block_size)))

        #         elif color == 1:
        #             black_sprite = pygame.transform.scale((pygame.image.load("Tommy.png").convert_alpha()),
        #                                    (int((cs.grid_right-cs.grid_left) * 0.4), int((cs.grid_bottom -cs.grid_top) * 0.4)))
        #             screen.blit(black_sprite, (x + int(0.1*self.block_size), \
        #                 y + int(0.1*self.block_size)))
        #######

        for button in self.buttons:

            x, y, color, text, width, height = button
            # rect
            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(screen, color, rect)
            # text
            textSurf, textRect = text_object(text, cs.black)
            textRect.center = (x + int(width/2), y + int(height/2))
            screen.blit(textSurf, textRect)

        for t in self.texts:
            
            x, y, color, text = t
            textSurf, textRect = text_object(text, color)
            textRect.center = (x, y)

            screen.blit(textSurf, textRect)

def text_object(text, color):
    # font = pygame.font.Font("freesansbold.ttf",15)
    font = pygame.font.SysFont("comicsansms", 20)
    textSurface = font.render(text, True, color)
    return (textSurface, textSurface.get_rect())
