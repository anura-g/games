import pygame 

def load_image(sheet, x, y, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width, height))
    image = pygame.transform.scale(image, (width*scale, height*scale))
    image.set_colorkey((0, 0, 0))
    return image 

def load_animation(sheet, frame_width, frame_height, scale):
    frames = []
    sheet_width = sheet.get_width()

    for x in range(0, sheet_width, frame_width):
        frame = load_image(sheet, x, 0, frame_width, frame_height, scale)
        frames.append(frame)
    return frames

def load_character_animations():
    animation_types = ["idle", "run"]
    character_types = ["player"]

    character_animations = []
    for character in character_types:
        animation_list = []
        for animation in animation_types:
            sheet = pygame.image.load(f"assets/images/characters/{character}/{animation}.png").convert_alpha()
            frames = load_animation(sheet, 100, 100, 2) 
            animation_list.append(frames)
        character_animations.append(animation_list)
    
    return character_animations 