import os

import pygame

from Board import Board
from Pieces import Pieces


class GameThread:

    def loadGame(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        background = pygame.image.load(os.path.join('Resources', 'board.png')).convert()
        # pieces_image = pygame.image.load(os.path.join('Resources', 'wQ.png')).convert_alpha()
        size_of_bg = background.get_rect().size
        square_width = size_of_bg[0] / 8
        square_height = size_of_bg[1] / 8
        # pieces_image = pygame.transform.scale(pieces_image, (int(square_width), int(square_height)))
        # moved into UI
        screen = pygame.display.set_mode(size_of_bg)
        screen.blit(background, (0, 0))
        # screen.blit(pieces_image, (200,0))
        game_running = True
        dummy = Board()
        clicked = False
        possible_moves = []
        last_turn = "b"
        while game_running:
            screen.blit(background, (0, 0))
            # screen.blit(pieces_image, (200, 0))
            dummy.loadAll(screen, square_width, square_height)
            dummy.load_dots(screen, square_width, square_height, possible_moves)
            pygame.display.update()
            # dummy.load_dots(screen,square_width,square_height,possible_moves)
            # print(possible_moves)
            for event in pygame.event.get():
                # Handle the events while in menu:
                if event.type == pygame.QUIT:
                    # Window was closed.
                    game_running = False
                    pygame.quit()
                    break

                if event.type == pygame.MOUSEBUTTONUP:
                    print("clicked")
                    # The mouse was clicked somewhere.
                    position = pygame.mouse.get_pos()
                    coord = dummy.physical_to_board(square_width, square_height, position[0], position[1])
                    selected = dummy.getPieceString(coord)
                    this_turn = dummy.get_opposite_color(last_turn)
                    if clicked is False and selected == 0: #didnt select a piece, and clicked on empty
                        continue
                    elif clicked is False and selected != 0: #didnt select a piece, and clicked on a piece
                        #check if it is the correct color
                        color = selected[1:]
                        if this_turn == color:
                            # print(coord)
                            possible_moves = dummy.get_possible_moves(coord)
                            dummy.load_dots(screen, square_width, square_height, possible_moves)
                            # dummy.remove_from_coord(coord)
                            # dummy.print_board()
                            if selected != 0:
                                clicked = True
                            from_coord = coord
                    else:
                        # print(possible_moves)
                        if coord in possible_moves:
                            # print("moved")
                            dummy.move_to_coord(from_coord, coord)
                            # dummy.print_board()
                            possible_moves = []
                            clicked = False
                            last_turn = this_turn
                        else:
                            clicked = False
                            possible_moves = []


