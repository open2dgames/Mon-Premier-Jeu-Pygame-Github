import math 

def normalize(vector):
    x, y = vector
    magnitude = math.sqrt(x**2 + y**2)

    if magnitude == 0:
        return (0, 0)
    
    return (x / magnitude, y / magnitude)

def draw_text(screen, text, font, color, pos):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = pos
    screen.blit(textobj, textrect)