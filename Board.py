import copy
import os

import pygame

from Pieces import Pieces


class Board:
    board = []

    def __init__(self):
        self.board = [['Rb', 'Hb', 'Bb', 'Qb', 'Kb', 'Bb', 'Hb', 'Rb'],  # 8
                      ['Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb', 'Pb'],  # 7
                      [0000, 0000, 0000, 0000, 0000, 0000, 0000, 0000],  # 6
                      [0000, 0000, 0000, 0000, 0000, 0000, 0000, 0000],  # 5
                      [0000, 0000, 0000, 0000, 0000, 0000, 0000, 0000],  # 4
                      [0000, 0000, 0000, 0000, 0000, 0000, 0000, 0000],  # 3
                      ['Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw', 'Pw'],  # 2
                      ['Rw', 'Hw', 'Bw', 'Qw', 'Kw', 'Bw', 'Hw', 'Rw']]  # 1
        # a      b     c     d     e     f     g     h

    def print_board(self):
        for temp in self.board:
            print(temp)

    def getPieceString(self, position):
        # in row and col
        return self.board[position[0]][position[1]]

    def remove_from_coord(self, position):
        # in row and col
        self.board[position[0]][position[1]] = 0000

    def move_to_coord(self, from_pos, to_pos):
        # print(self.getPieceString(from_pos))
        # print(self.getPieceString(to_pos))
        self.board[to_pos[0]][to_pos[1]] = self.board[from_pos[0]][from_pos[1]]
        self.remove_from_coord(from_pos)

    def loadAll(self, screen, width, height):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                thing = self.board[row][col]
                if thing != 0:
                    temp = Pieces([row, col], self.board_to_physical(width, height, row, col), self.str_to_info(thing))
                    temp.load_image(screen, width, height)
    def load_check(self,screen,width,height,coord):
        row = coord[0]
        col = coord[1]
        phy_position_x = self.board_to_physical(width, height, row, col)[0]
        phy_position_y = self.board_to_physical(width, height, row, col)[1]
        # if thing == 0:
        pieces_image = pygame.image.load(os.path.join('Resources', "red_circle_big.png")).convert_alpha()
        pieces_image = pygame.transform.scale(pieces_image, (int(width), int(height)))
        screen.blit(pieces_image, (phy_position_x, phy_position_y))

    def load_dots(self, screen, width, height, possible_moves):
        for posn in possible_moves:
            row = posn[0]
            # print(i)
            # print(width)
            col = posn[1]
            phy_position_x = self.board_to_physical(width, height, row, col)[0]
            phy_position_y = self.board_to_physical(width, height, row, col)[1]
            # if thing == 0:
            pieces_image = pygame.image.load(os.path.join('Resources', "green_circle_small.png")).convert_alpha()
            pieces_image = pygame.transform.scale(pieces_image, (int(width), int(height)))
            screen.blit(pieces_image, (phy_position_x, phy_position_y))

    def str_to_info(self, name):
        is_white = True
        if name[1] == "b":
            is_white = False
        if is_white:
            png = "w" + name[:1] + ".png"
            return [png, "w"]
        else:
            png = "b" + name[:1] + ".png"
            return [png, "b"]

    def board_to_physical(self, square_width, square_height, row, col):
        # takes in row and col returns x and y
        # x is row
        # y is col
        # if self.board[x][y] != 0:
        return square_width * col, square_height * row

    def physical_to_board(self, square_width, square_height, x, y):
        # takes in x and y, return row and col
        return int(y / square_width), int(x / square_height)

    def insideBoard(self, row, col):
        return 0 <= row <= 7 and 0 <= col <= 7

    def isOccupied(self, row, col):
        if not self.insideBoard(row, col):
            return True
        if self.board[row][col] == 0:
            # The square has nothing on it.
            return False
        return True

    def isOccupiedColor(self, row, col, color):
        if not self.insideBoard(row, col):
            return False
        if self.board[row][col] == 0:
            # the square has nothing on it.
            return False
        return self.board[row][col][1:] == color

    def get_opposite_color(self, color):
        if color == "w":
            return "b"
        return "w"

    def get_possible_moves(self, position):
        possible_moves = []
        row = position[0]
        col = position[1]
        #if the position is empty, return an empty array
        if not self.isOccupied(row, col):
            return []
        piece_str = self.board[row][col]
        piece_name = piece_str[:1]
        piece_color = piece_str[1:]
        # print(piece_name)
        # print(piece_color)
        if piece_name == "P":
            possible_moves = self.get_pawn_moves(row, col, piece_color)
        elif piece_name == "R":
            possible_moves = self.get_rook_moves(row, col, piece_color)
        elif piece_name == "B":
            possible_moves = self.get_bishop_moves(row, col, piece_color)
        elif piece_name == "Q":
            possible_moves = self.get_queen_moves(row, col, piece_color)
        elif piece_name == "H":
            possible_moves = self.get_horse_moves(row, col, piece_color)
        elif piece_name == "K":
            possible_moves = self.get_king_moves(row, col, piece_color)

        new_list = []
        temp_board = copy.deepcopy(self.board)
        print(possible_moves)
        for temp_move in possible_moves:
            self.board = copy.deepcopy(temp_board)
            #print(temp_move)
            self.move_to_coord(position,temp_move)
            print(piece_color)
            print(self.isCheck(piece_color))
            print(self.lookfor("Kb"))
            #...
            if self.isCheck(piece_color):
                print("CHECK!")
            else:
                new_list.append(temp_move)
        self.board = copy.deepcopy(temp_board)
        possible_moves = new_list
        print(possible_moves)
        return possible_moves


    def get_possible_attacks(self, position):
        possible_attacks= ()
        row = position[0]
        col = position[1]
        # if the position is empty, return an empty array
        if not self.isOccupied(row, col):
            return []
        piece_str = self.board[row][col]
        piece_name = piece_str[:1]
        piece_color = piece_str[1:]
        # print(piece_name)
        # print(piece_color)
        if piece_name == "P":
            return self.get_pawn_attacks(row, col, piece_color)
        elif piece_name == "R":
            return self.get_rook_moves(row, col, piece_color)
        elif piece_name == "B":
            return self.get_bishop_moves(row, col, piece_color)
        elif piece_name == "Q":
            return self.get_queen_moves(row, col, piece_color)
        elif piece_name == "H":
            return self.get_horse_moves(row, col, piece_color)
        elif piece_name == "K":
            return self.get_king_moves(row, col, piece_color)


    def get_king_moves(self, row, col, color):
        possible_moves = []
        for row_change in [-1, 0, 1]:
            for col_change in [-1, 0, 1]:
                if not self.isOccupied(row + row_change, col + col_change):
                    possible_moves.append((row + row_change, col + col_change))
                elif self.isOccupiedColor(row + row_change, col + col_change, self.get_opposite_color(color)):
                    possible_moves.append((row + row_change, col + col_change))
        return possible_moves

    def get_horse_moves(self, row, col, color):
        possible_moves = []
        total = 3
        for row_change in [-1, 1, -2, 2]:
            dif = total - abs(row_change)
            for col_change in [-dif, dif]:
                if not self.isOccupied(row + row_change, col + col_change):
                    possible_moves.append((row + row_change, col + col_change))
                elif self.isOccupiedColor(row + row_change, col + col_change, self.get_opposite_color(color)):
                    possible_moves.append((row + row_change, col + col_change))
        return possible_moves

    def get_queen_moves(self, row, col, color):
        return self.get_rook_moves(row, col, color) + self.get_bishop_moves(row, col, color)

    def get_bishop_moves(self, row, col, color):
        possible_moves = []
        for row_change in [-1, 1]:
            for col_change in [-1, 1]:
                row_copy = row
                col_copy = col
                while True:
                    row_copy += row_change
                    col_copy += col_change
                    if not self.isOccupied(row_copy, col_copy):
                        # The square is empty, so our bishop can go there.
                        possible_moves.append((row_copy, col_copy))
                    elif self.isOccupiedColor(row_copy, col_copy, self.get_opposite_color(color)):
                        possible_moves.append((row_copy, col_copy))
                        break
                    else:
                        break
        return possible_moves

    def get_rook_moves(self, row, col, color):
        possible_moves = []

        for temp in [-1, 1]:
            # horizontal search! col is fixed
            row_copy = row
            while True:
                row_copy += temp
                if self.insideBoard(row_copy, col) and not self.isOccupied(row_copy, col):
                    possible_moves.append((row_copy, col))
                elif self.insideBoard(row_copy, col) and self.isOccupiedColor(row_copy, col,
                                                                              self.get_opposite_color(color)):
                    possible_moves.append((row_copy, col))
                    break
                else:
                    break

            col_copy = col
            while True:
                col_copy += temp
                if self.insideBoard(row, col_copy) and not self.isOccupied(row, col_copy):
                    possible_moves.append((row, col_copy))
                elif self.insideBoard(row, col_copy) and self.isOccupiedColor(row, col_copy,
                                                                              self.get_opposite_color(color)):
                    possible_moves.append((row, col_copy))
                    break
                else:
                    break
        return possible_moves

    def get_pawn_moves(self, row, col, piece_color):
        possible_moves = []
        # x here is actually row number
        if piece_color == 'w':
            if not self.isOccupied(row - 1, col):
                # print("1")
                possible_moves.append((row - 1, col))
            if row == 6 and not self.isOccupied(row - 2, col) and not self.isOccupied(row - 1, col):
                possible_moves.append((row - 2, col))
            if col != 0 and self.isOccupiedColor(row - 1, col - 1, 'b'):
                # The piece diagonally up and left of this pawn is a black piece.
                # Also, this is not an 'a' file pawn (left edge pawn)
                possible_moves.append((row - 1, col - 1))
            if col != 7 and self.isOccupiedColor(row - 1, col + 1, 'b'):
                # The piece diagonally up and right of this pawn is a black one.
                # Also, this is not an 'h' file pawn.
                possible_moves.append((row - 1, col + 1))

        elif piece_color == 'b':  # The piece is black, same as above but opposite side.
            if not self.isOccupied(row + 1, col):
                possible_moves.append((row + 1, col))
            if row == 1 and not self.isOccupied(row + 2, col) and not self.isOccupied(row + 1, col):
                possible_moves.append((row + 2, col))
            if col != 0 and self.isOccupiedColor(row + 1, col - 1, 'w'):
                possible_moves.append((row + 1, col - 1))
            if col != 7 and self.isOccupiedColor(row + 1, col + 1, 'w'):
                possible_moves.append((row + 1, col + 1))
        return possible_moves

    def get_pawn_attacks(self, row, col, piece_color):
        possible_attacks = []
        # x here is actually row number
        if piece_color == 'w':
            if col != 0 and self.isOccupiedColor(row - 1, col - 1, 'b'):
                # The piece diagonally up and left of this pawn is a black piece.
                # Also, this is not an 'a' file pawn (left edge pawn)
                possible_attacks.append((row - 1, col - 1))
            if col != 7 and self.isOccupiedColor(row - 1, col + 1, 'b'):
                # The piece diagonally up and right of this pawn is a black one.
                # Also, this is not an 'h' file pawn.
                possible_attacks.append((row - 1, col + 1))

        elif piece_color == 'b':  # The piece is black, same as above but opposite side.
            if col != 0 and self.isOccupiedColor(row + 1, col - 1, 'w'):
                possible_attacks.append((row + 1, col - 1))
            if col != 7 and self.isOccupiedColor(row + 1, col + 1, 'w'):
                possible_attacks.append((row + 1, col + 1))
        return possible_attacks



    def isAttacked(self,board_position, color):
        # Get board
        board = self.board
        # Get b from black or w from white

        # Get all the squares that are attacked by the particular side:
        listofAttackedSquares = []
        enemy_color = self.get_opposite_color(color);
        for row in range(8):
            for col in range(8):
                if board[row][col] != 0 and board[row][col][1] == enemy_color:
                    listofAttackedSquares.extend(
                        self.get_possible_attacks([row,col]))
        # The true argument
                    # prevents infinite recursion.
        # Check if the target square falls under the range of attack by the specified
        # side, and return it:

        return (board_position[0], board_position[1]) in listofAttackedSquares

    def lookfor(self, piece):
        listofLocations = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == piece:
                    listofLocations.append([row, col])
        return listofLocations


    def isCheck(self, color):
        # Get data:
        new_board = self.board.copy()
        enemy_color = self.get_opposite_color(color)
        piece = 'K' + color
        # Get the coordinates of the king:
        position = self.lookfor(piece)[0]
        # Check if the position of the king is attacked by
        # the enemy and return the result:
        return self.isAttacked(position,color)

# x = Board()
# print(x.get_possible_moves([6, 1]))
