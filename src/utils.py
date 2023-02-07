def convert_to_pygame_coord(coord, display_height):
    return int(coord[0]), int(display_height - coord[1])
