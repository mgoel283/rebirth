import pygame
import yaml
import random


class Player:
    def __init__(self, num):
        self.num = num
        self.curr_pos = 24
        self.visited = set()


class Button:
    def __init__(self, name, rect, color, enabled):
        self.name = name
        self.rect = rect
        self.color = color
        self.enabled = enabled


# for each button check if it was pressed
def do_roll(mouse_pos):
    global scroll
    for b in buttons:
        if ((mouse_pos[0] > b.rect[0]) and
                (mouse_pos[0] < b.rect[0] + b.rect[2]) and
                (mouse_pos[1] > b.rect[1]) and
                (mouse_pos[1] < b.rect[1] + b.rect[3])):

            #Check win
            if player.curr_pos == 104:
                print('you won!')
            else:
                # change curr_pos here
                need = True
                while need:
                    num = roll()
                    if num in moves[player.curr_pos]:  # valid roll
                        need = False
                        player.curr_pos = moves[player.curr_pos][num]

            scroll = 0
            return b.name


def draw():
    screen.blit(bg_image, (0, 0))

    # Floating title
    text = my_font.render(titles[player.curr_pos], True, WHITE)
    screen.blit(text, [20, 20])

    # Main text
    draw_text(screen, texts[player.curr_pos], WHITE, [20, 50, 550, 300], scroll)

    block_size = 30
    # grid
    for y in range(13):
        for x in range(8):
            rect = pygame.Rect((x+18)*(block_size+4.15), (y+2.15)*(block_size+9), block_size, block_size)
            pos = (13-(y+1))*8 + (x+1)
            if pos == 104:  # Nirvana
                pygame.draw.rect(screen, (230, 184, 0), rect)
            elif pos == 1 or pos == 48:  # hells
                pygame.draw.rect(screen, (138, 21, 56), rect)
            elif pos == player.curr_pos:  # player
                pygame.draw.rect(screen, (57, 83, 189), rect)
            else:
                pygame.draw.rect(screen, (71, 72, 84), rect)

    for b in buttons:
        if b.enabled:
            pygame.draw.line(screen, b.color, [b.rect[0], int(0.5 * (2 * b.rect[1] + b.rect[3]))],
                             [b.rect[0] + b.rect[2], int(0.5 * (2 * b.rect[1] + b.rect[3]))], b.rect[3])  #
            text = my_font.render(b.name, True, [255, 255, 255])
            screen.blit(text, [b.rect[0] + 15, b.rect[1] + 15])


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return [' '] + result


def draw_text(surface, txt, color, rect, scr):
    y = rect[1]
    line_spacing = 2

    # get the height of the font
    font_height = my_font.size("Tg")[1]

    paras = intersperse(txt.split('\n'), ' ')
    for text in paras:
        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + font_height > rect[1] + rect[3]:
                break

            # determine maximum width of line
            while my_font.size(text[:i])[0] < rect[2] and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            if scr > 0:
                scr -= 1
            else:
                # render the line and blit it to the surface
                image = my_font.render(text[:i], True, color)

                surface.blit(image, (rect[0], y))
                y += font_height + line_spacing

            # remove the text we just blitted
            text = text[i:]

    return None


def load_conf():
    with open('titles.yaml') as title:
        ttls = yaml.load(title, Loader=yaml.FullLoader)
    with open('text.yaml') as text:
        txts = yaml.load(text, Loader=yaml.FullLoader)
    with open('moves.yaml') as move:
        mvs = yaml.load(move, Loader=yaml.FullLoader)

    return ttls, txts, mvs


def roll():
    return random.randint(1, 6)


if __name__ == "__main__":
    # setup and render
    player = Player(1)
    buttons = [
        Button('>ROLL AND BE REBORN', [20, 400, 260, 50], [125, 125, 125], True)
    ]

    background_colour = (0, 0, 0)
    WHITE = (255, 255, 255)
    (width, height) = (900, 600)
    screen = pygame.display.set_mode((width, height))
    screen.fill(background_colour)
    pygame.display.set_caption('Rebirth: The Tibetan Game of Liberation')
    pygame.font.init()

    my_font = pygame.font.SysFont("monospace", 20)
    bg_image = pygame.image.load('bg.png')

    titles, texts, moves = load_conf()

    # run game
    scroll = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_p = pygame.mouse.get_pos()
                # left click
                if event.button == 1:
                    do_roll(mouse_p)
                # scroll wheel
                if event.button == 4:
                    if scroll > 0:
                        scroll -= 1
                if event.button == 5:
                    if scroll < 70:
                        scroll += 1

        # game logic
        screen.fill(background_colour)
        draw()
        pygame.display.flip()
