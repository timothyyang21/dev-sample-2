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
    def __init__(self, board_size):

        if board_size > 14 or board_size < 2:
            print('board size must be between 2 and 14')
            return

        self.board_size = board_size
        self.level = 1 # Initially it's level 1.
        self.score = 0
        self.initialize_time = 100
        self.time = 0
        self.block_size = (cs.grid_right - cs.grid_left)//board_size - 2
        self.radius = int(self.block_size/3)
        self.random_game = False  # Initialize this value to false

    def init(self, board_size):

        self.board_size = board_size
        self.block_size = (cs.grid_right - cs.grid_left)//board_size - 2
        self.radius = int(self.block_size/3)


        self.grid = self.init_grid()
        self.buttons = self.init_buttons()
        self.texts = self.init_texts()

        self.step = 0
        self.chosen = []
        self.start_time = pygame.time.get_ticks()
        self.rand_grid()


        # Provide random theme
        self.theme_r = random.uniform(0, 1)

        # Give random color background
        rand_col = random.uniform(0, 1)
        if rand_col < 0.1:
            self.cs_color = cs.wood
        elif rand_col < 0.2:
            self.cs_color = cs.pink
        elif rand_col < 0.3:
            self.cs_color = cs.red
        elif rand_col < 0.4:
            self.cs_color = cs.green
        elif rand_col < 0.5:
            self.cs_color = cs.blue
        elif rand_col < 0.6:
            self.cs_color = cs.dark_blue
        elif rand_col < 0.7:
            self.cs_color = cs.milk_blue
        elif rand_col < 0.8:
            self.cs_color = cs.white
        elif rand_col < 0.9:
            self.cs_color = cs.black
        else:
            self.cs_color = cs.grey

        # Determine the scale
        if self.board_size == 2:
            scale = 0.4
        elif self.board_size == 3:
            scale = 0.27
        elif self.board_size == 4:
            scale = 0.2
        elif self.board_size == 5:
            scale = 0.16
        elif self.board_size == 6:
            scale = 0.14
        elif self.board_size == 7:
            scale = 0.11
        elif self.board_size == 8:
            scale = 0.09
        elif self.board_size == 9:
            scale = 0.08
        elif self.board_size == 10:
            scale = 0.075
        elif self.board_size == 11:
            scale = 0.07
        elif self.board_size == 12:
            scale = 0.065
        elif self.board_size == 13:
            scale = 0.06
        elif self.board_size == 14:
            scale = 0.055

        # List of playable_sprites
        self.AVATARS_SPRITE = [load_avatar("linear_resources/Princey.png", scale),
                          load_avatar("linear_resources/Tommy.png", scale),
                          load_avatar("linear_resources/Tree.png", scale),
                          load_avatar("linear_resources/Santa.png", scale),
                          load_avatar("linear_resources/Bad_apple.png", scale),
                          load_avatar("linear_resources/Good_apple.png", scale),
                          load_avatar("linear_resources/Vampire.png", scale),
                          load_avatar("linear_resources/Werewolf.png", scale),
                          load_avatar("linear_resources/Horror_white.png", scale),
                          load_avatar("linear_resources/Horror_black.png", scale),
                          load_avatar("linear_resources/White_sheep.png", scale),
                          load_avatar("linear_resources/Black_sheep.png", scale)]

    def start(self):

        pygame.init()

        ### Initialize Music For Each Theme ###
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("linear_resources/feels_good.mp3")
        pygame.mixer.music.play()

        # if self.theme_r < 0.167:
        #     pygame.mixer.music.load("linear_resources/hbd.mp3")
        # elif self.theme_r < 0.333:
        #     pygame.mixer.music.load("linear_resources/christmas.mp3")
        # elif self.theme_r < 0.499:
        #     pygame.mixer.music.load("linear_resources/feels_good.mp3")
        # elif self.theme_r < 0.667:
        #     pygame.mixer.music.load("linear_resources/hbd.mp3")
        # elif self.theme_r < 0.834:
        #     pygame.mixer.music.load("linear_resources/poisonous.mp3")
        # else:
        #     pygame.mixer.music.load("linear_resources/quiet_time.mp3")

        pygame.display.set_caption("game")
        self.screen = pygame.display.set_mode([cs.window_size, cs.window_size])

        self.init(self.level + 1)
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
                        self.texts[0][3] = 'Congratulations! You solved the level 1 puzzle!'

                        file = 'linear_resources/correct.wav'
                        pygame.mixer.music.load(file)
                        pygame.mixer.music.play()

                        ######################### Update score ###############################
                        self.score += self.time * pow(self.board_size, 2)
                        self.texts[1][3] = '                                               Score: ' + str(self.score)
                        self.draw(self.screen)

                        ######################### Update time ###############################
                        self.initialize_time = self.time
                        self.initialize_time += 10 * self.board_size

                        ######################### Update level ###############################
                        self.level += 1
                        self.init(self.level + 1)

                seconds_passed = int((pygame.time.get_ticks() - self.start_time)/1000)
                seconds_left = self.initialize_time - seconds_passed
                self.time = seconds_left

                if not solved:
                    self.texts[1][3] = 'Level: ' + str(self.level) + '     ' + 'Time: ' + str(seconds_left) + ' s     ' + \
                        'Steps: ' + str(self.step) + '      Score: ' + str(self.score)

                if self.time < 0:
                    file = 'linear_resources/wrong.mp3'
                    pygame.mixer.music.load(file)
                    pygame.mixer.music.play()
                    self.gameover()


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
                    elif color == 0:
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
                zero = 0
                first_black_found = False
                first_black_entry_place = 0
                all_zero_column = True
                zero_columns = []
                # starting_place = 0

                for row in range(self.board_size):

                    color = self.grid[row][col][2]
                    current_row_color.append(color) # Stores the color into the column for that specific row spot
                    zero_columns.append(0)

                    if color == 0:
                        all_zero_column = False
                        white += 1
                    elif color == 1:
                        all_zero_column = False
                        black += 1 # black are leading entries, should only have 1 in each column.

                        if not first_black_found:
                            first_black_entry_place = row # This keeps track of the first leading entry position
                            first_black_found = True
                    else:
                        zero += 1
                        # If it's an all-zero column
                        # if zero == self.board_size:
                        #    first_black_entry_place = starting_place

                    if all_zero_column == True:
                        zero_columns[row] += 1

                    # for col_num in range(row):
                        # if zero_columns[col_num] == 1:
                        #    starting_place += 1

                # The first leading entry (black) of the column should correspond to the right starting place
                # if first_black_entry_place != starting_place:
                #     return False

                # Should only have 1 or fewer black per column
                if black > 1:
                    return False

                # If there are a leading entry in one column, there should be no other white entries
                if black == 1 and white >= 1:
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

            self.init(self.level + 1)

        # Impossible - If it is possible, won't respond
        elif clicked == 2*self.board_size + 3:

            if self.random_game == True:
        	    self.init(self.level + 2)
            else:
                self.initialize_time -= 10
                file = 'linear_resources/wrong.mp3'
                pygame.mixer.music.load(file)
                pygame.mixer.music.play()

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

        # This gives the correct board_size for the correct level
        # if self.level == 1:
        #     self.board_size = 2
        # elif self.level == 2:
        #     self.board_size = 3
        # elif self.level == 3:
        #     self.board_size = 4
        # elif self.level == 4:
        #     self.board_size = 5
        # elif self.level == 5:
        #     self.board_size = 6
        # elif self.level == 6:
        #     self.board_size = 7
        # elif self.level == 7:
        #     self.board_size = 8
        # elif self.level == 8:
        #     self.board_size = 9
        # elif self.level == 9:
        #     self.board_size = 10
        # elif self.level == 10:
        #     self.board_size = 11
        # elif self.level == 11:
        #     self.board_size = 12
        # elif self.level == 12:
        #     self.board_size = 13
        # elif self.level == 13:
        #     self.board_size = 14

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
            buttons.append([cs.grid_right+int((1/8)*diff), \
                    cs.grid_top + y*(self.block_size+2)+12, cs.milk_blue, 'select', int(0.39*diff), 25])

        for y in range(self.board_size):
            buttons.append([cs.grid_right+int((4/7)*diff), \
                    cs.grid_top + y*(self.block_size+2)+12, cs.milk_blue, 'cancel', int(0.39*diff), 25])

        buttons.append([int(0.4 * cs.window_size), int(cs.grid_bottom + 0.3 * (cs.window_size - cs.grid_bottom)), \
            cs.milk_blue, 'swap', 60, 30])

        buttons.append([int(0.6 * cs.window_size), int(cs.grid_bottom + 0.3 * (cs.window_size - cs.grid_bottom)), \
            cs.milk_blue, 'add', 60, 30])

        buttons.append([int(0.8 * cs.window_size), int(cs.grid_bottom + 0.3 * (cs.window_size - cs.grid_bottom)), \
            cs.milk_blue, 'new game', 100, 30])

        buttons.append([int(0.1 * cs.window_size), int(cs.grid_bottom + 0.3 * (cs.window_size - cs.grid_bottom)), \
            cs.milk_blue, 'impossible', 100, 30])

        return buttons

    def init_texts(self):

        texts = [[int(0.5 * cs.window_size), int(0.3 * cs.grid_top), cs.pink, ''], \
        [int(0.5 * cs.window_size), int(0.6 * cs.grid_top), cs.pink, 'Time: ' + str(0) + ' s']]
        return texts

    def draw(self, screen):

        # for row in self.grid:
        #     for block in row:
        #         x, y, color = block
        #
        #         rect = pygame.Rect(x, y, self.block_size, self.block_size)
        #         pygame.draw.rect(screen, cs.wood, rect)
        #
        #         if color == 0:
        #             pygame.draw.circle(screen, cs.white, (x + int(0.5*self.block_size), \
        #                 y + int(0.5*self.block_size)), self.radius, 0)
        #         elif color == 1:
        #             pygame.draw.circle(screen, cs.black, (x + int(0.5*self.block_size), \
        #                 y + int(0.5*self.block_size)), self.radius, 0)

        ####### This part is for specializations of the images and personalizations, but for now this works best for 2x2, uncomment to use it & comment the above
        for row in self.grid:
            for block in row:
                x, y, color = block

                rect = pygame.Rect(x, y, self.block_size, self.block_size)

                pygame.draw.rect(screen, self.cs_color, rect)

                if self.theme_r < 0.167:
                    white_num = 0
                    black_num = 1
                elif self.theme_r < 0.333:
                    white_num = 2
                    black_num = 3
                elif self.theme_r < 0.499:
                    white_num = 4
                    black_num = 5
                elif self.theme_r < 0.667:
                    white_num = 6
                    black_num = 7
                elif self.theme_r < 0.834:
                    white_num = 8
                    black_num = 9
                else:
                    white_num = 10
                    black_num = 11

                if color == 0:
                    screen.blit(self.AVATARS_SPRITE[white_num], (x + int(0.1*self.block_size), y + int(0.1*self.block_size)))

                elif color == 1:
                    screen.blit(self.AVATARS_SPRITE[black_num], (x + int(0.1*self.block_size), y + int(0.1*self.block_size)))
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

    def gameover(self):
        color = (250, 250, 100)
        fontsize = 100
        font = pygame.font.Font("linear_resources/StardustAdventure.ttf", fontsize)
        text1 = font.render('GAME OVER', True, color)
        text1Rect = text1.get_rect()
        text1Rect.center = (300, 200)
        self.screen.blit(text1, text1Rect)

        color = (250, 250, 100)
        font = pygame.font.Font("linear_resources/StardustAdventure.ttf", 80)

        text2 = font.render("POINTS: " + str(self.score), True, color)
        text2Rect = text2.get_rect()
        text2Rect.center = (300, 300)
        self.screen.blit(text2, text2Rect)

        pause = True
        clock = pygame.time.Clock()

        while pause:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # gameDisplay.fill(white)

            pygame.display.flip()
            clock.tick(60)

def text_object(text, color):
    # font = pygame.font.Font("freesansbold.ttf",15)
    font = pygame.font.SysFont("comicsansms", 20)
    textSurface = font.render(text, True, color)
    return (textSurface, textSurface.get_rect())

def load_avatar(file, scale):
    return pygame.transform.scale((pygame.image.load(file).convert_alpha()), (int((cs.grid_right - cs.grid_left) * scale), int((cs.grid_bottom - cs.grid_top) * scale)))