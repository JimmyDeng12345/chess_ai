import os
from typing import List

import pygame


class Pieces:
    info = []  # png_name, white or black
    board_position = []

    #  physical_position = []

    def __init__(self, board_position: List[int], physical_position: List[int], info):
        self.board_position = board_position
        self.physical_position = physical_position
        self.info = info


    def load_image(self, screen, square_width, square_height):
        png_name = self.info[0]
        phy_position_x = self.physical_position[0]
        phy_position_y = self.physical_position[1]
        pieces_image = pygame.image.load(os.path.join('Resources', png_name)).convert_alpha()
        pieces_image = pygame.transform.scale(pieces_image, (int(square_width), int(square_height)))
        screen.blit(pieces_image, (phy_position_x, phy_position_y))



class Rook(Pieces):
    info = []
