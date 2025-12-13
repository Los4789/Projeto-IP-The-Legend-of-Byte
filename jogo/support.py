import pygame
from os import walk
def import_folder(path):
    surface_list = []
    for _, __, img_files in walk(path):
        img_files = sorted(img_files)
        for image_name in img_files:
            full_path = path + '/' + image_name
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
