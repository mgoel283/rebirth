import pygame
import yaml
import random
import io, sys, os
import tkinter
from tkinter import messagebox

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


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


def display_help():
    tkinter.Tk().wm_withdraw()
    messagebox.showinfo("How to Play",
                        'You start in "The Heavenly Highway"!\n\nPick an available action or tempt fate and '
                        'press >ROLL to take the next step in your journey to Nirvana.\n\nReference the map on the '
                        'right to see your progress (you are the green square). Scroll through the text box to learn '
                        'more about your current status. \n\nIf you end up in "Vajra Hell" or "Cessation'
                        '", certain conditions must be met before you can leave.')


def do_press(mouse_pos):
    global scroll
    global hell_rolls
    for b in buttons:
        if ((mouse_pos[0] > b.rect[0]) and
                (mouse_pos[0] < b.rect[0] + b.rect[2]) and
                (mouse_pos[1] > b.rect[1]) and
                (mouse_pos[1] < b.rect[1] + b.rect[3])):

            opt_btns = ('>1', '>2', '>3', '>4', '>5', '>6')

            if b.name in opt_btns:
                picked = int(b.name[1])
                if picked in moves[player.curr_pos]:
                    player.curr_pos = moves[player.curr_pos][picked]
                    return
                else:  # invalid
                    return
            elif b.name == ">HOW TO PLAY":
                display_help()
                return

            if player.curr_pos == 1 or player.curr_pos == 48:  # hell conditions
                num = roll()
                hell_rolls.append(num)

                if hell_rolls.count(1) >= 1 and hell_rolls.count(2) >= 2 and hell_rolls.count(3) >= 3 and \
                        hell_rolls.count(4) >= 4 and hell_rolls.count(5) >= 5 and hell_rolls.count(6) >= 6:
                    if player.curr_pos == 1:
                        player.curr_pos = 9
                    else:
                        player.curr_pos = 52
                    hell_rolls = []
                return num
            elif player.curr_pos == 104:  # Check win
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


def draw(num):
    screen.blit(bg_image, (0, 0))

    # Floating title
    text = my_font.render(titles[player.curr_pos], True, WHITE)
    screen.blit(text, [20, 20])

    # Main text
    draw_text(screen, texts[player.curr_pos], WHITE, [20, 50, 550, 300], scroll)

    # progress grid
    draw_grid()

    # option buttons
    if player.curr_pos != 1 and player.curr_pos != 48:
        draw_options()

    # Roll and help button/ Win text rendering
    for b in (buttons[0], buttons[1]):
        if b.enabled:
            if player.curr_pos != 104:
                pygame.draw.line(screen, b.color, [b.rect[0], int(0.5 * (2 * b.rect[1] + b.rect[3]))],
                                 [b.rect[0] + b.rect[2], int(0.5 * (2 * b.rect[1] + b.rect[3]))], b.rect[3])  #
                text = my_font.render(b.name, True, [255, 255, 255])
                screen.blit(text, [b.rect[0] + 15, b.rect[1] + 15])
            elif b.name == ">ROLL AND BE REBORN":
                text = my_font.render("You've attained Nirvana!", True, BLACK)
                text2 = my_font.render("Generate a new soul to play again", True, BLACK)
                text3 = my_font.render("(restart the game)", True, BLACK)
                screen.blit(text, [b.rect[0] + 140, b.rect[1] + 45])
                screen.blit(text2, [b.rect[0] + 90, b.rect[1] + 90])
                screen.blit(text3, [b.rect[0] + 170, b.rect[1] + 110])

    # Hell Logic
    if player.curr_pos == 1 or player.curr_pos == 48:
        need_1 = 1 - hell_rolls.count(1)
        if need_1 < 0:
            need_1 = 0

        need_2 = 2 - hell_rolls.count(2)
        if need_2 < 0:
            need_2 = 0

        need_3 = 3 - hell_rolls.count(3)
        if need_3 < 0:
            need_3 = 0

        need_4 = 4 - hell_rolls.count(4)
        if need_4 < 0:
            need_4 = 0

        need_5 = 5 - hell_rolls.count(5)
        if need_5 < 0:
            need_5 = 0

        need_6 = 6 - hell_rolls.count(6)
        if need_6 < 0:
            need_6 = 0

        roll_text = my_font.render("You rolled " + str(num), True, BLACK)
        one_text = my_font.render("You need " + str(need_1) + " more 1's", True, BLACK)
        two_text = my_font.render("You need " + str(need_2) + " more 2's", True, BLACK)
        thr_text = my_font.render("You need " + str(need_3) + " more 3's", True, BLACK)
        four_text = my_font.render("You need " + str(need_4) + " more 4's", True, BLACK)
        five_text = my_font.render("You need " + str(need_5) + " more 5's", True, BLACK)
        six_text = my_font.render("You need " + str(need_6) + " more 6's", True, BLACK)

        screen.blit(one_text, [b.rect[0] - 265, b.rect[1] + 110])
        screen.blit(two_text, [b.rect[0] - 265, b.rect[1] + 135])
        screen.blit(thr_text, [b.rect[0] - 265, b.rect[1] + 160])
        screen.blit(four_text, [b.rect[0] + 15, b.rect[1] + 110])
        screen.blit(five_text, [b.rect[0] + 15, b.rect[1] + 135])
        screen.blit(six_text, [b.rect[0] + 15, b.rect[1] + 160])

        screen.blit(roll_text, [b.rect[0] - 80, b.rect[1] + 75])


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return [' '] + result


def draw_grid():
    block_size = 30
    # grid
    for y in range(13):
        for x in range(8):
            rect = pygame.Rect((x + 18) * (block_size + 4.15), (y + 2.15) * (block_size + 9), block_size, block_size)
            pos = (13 - (y + 1)) * 8 + (x + 1)

            if player.curr_pos == 104:  # flood screen
                pygame.draw.rect(screen, (230, 184, 0), rect)
            else:
                if pos == player.curr_pos:  # player
                    pygame.draw.rect(screen, (40, 128, 60), rect)
                elif pos == 104:  # Nirvana
                    pygame.draw.rect(screen, (230, 184, 0), rect)
                elif pos == 1 or pos == 48:  # hells
                    pygame.draw.rect(screen, (138, 21, 56), rect)
                elif pos == 54:  # checkpoint
                    pygame.draw.rect(screen, (57, 83, 189), rect)
                else:
                    pygame.draw.rect(screen, (71, 72, 84), rect)


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


def draw_options():
    for b in buttons[2:]:
        if b.enabled:
            if player.curr_pos != 104:
                pygame.draw.line(screen, b.color, [b.rect[0], int(0.5 * (2 * b.rect[1] + b.rect[3]))],
                                 [b.rect[0] + b.rect[2], int(0.5 * (2 * b.rect[1] + b.rect[3]))], b.rect[3])
                picked = int(b.name[1])
                opt_text = '-----'
                if picked in moves[player.curr_pos]:
                    opt_text = options[moves[player.curr_pos][picked]]
                text = my_font.render(b.name + ' ' + opt_text, True, [255, 255, 255])
                screen.blit(text, [b.rect[0] + 15, b.rect[1] + 15])


def load_conf():
    with io.open('titles.yaml', mode='r', encoding='utf-8') as title:
        ttls = yaml.load(title, Loader=yaml.FullLoader)
    with io.open('text.yaml', mode='r', encoding='utf-8') as text:
        txts = yaml.load(text, Loader=yaml.FullLoader)
    with io.open('moves.yaml', mode='r', encoding='utf-8') as move:
        mvs = yaml.load(move, Loader=yaml.FullLoader)
    with io.open('options.yaml', mode='r', encoding='utf-8') as opt:
        opts = yaml.load(opt, Loader=yaml.FullLoader)

    return ttls, txts, mvs, opts


def roll():
    return random.randint(1, 6)


if __name__ == "__main__":
    # setup and render
    player = Player(1)
    buttons = [
        Button('>ROLL AND BE REBORN', [15, 370, 280, 50], [90, 90, 90], True),
        Button('>HOW TO PLAY', [305, 370, 285, 50], [90, 90, 90], True),
        Button('>1', [15, 430, 280, 50], [125, 125, 125], True),
        Button('>2', [15, 485, 280, 50], [125, 125, 125], True),
        Button('>3', [15, 540, 280, 50], [125, 125, 125], True),
        Button('>4', [305, 430, 285, 50], [125, 125, 125], True),
        Button('>5', [305, 485, 285, 50], [125, 125, 125], True),
        Button('>6', [305, 540, 285, 50], [125, 125, 125], True),
    ]

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    (width, height) = (900, 600)
    screen = pygame.display.set_mode((width, height))
    screen.fill(BLACK)
    pygame.display.set_caption('Rebirth: The Tibetan Game of Liberation')
    pygame.font.init()

    my_font = pygame.font.SysFont("monospace", 20)
    bg_image = pygame.image.load('bg.png')

    titles, texts, moves, options = load_conf()

    # run game
    scroll = 0
    running = True
    wait = False
    hell_rolls = []
    num = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_p = pygame.mouse.get_pos()
                # left click
                if event.button == 1:
                    num = do_press(mouse_p)
                # scroll wheel
                if event.button == 4:
                    if scroll > 0:
                        scroll -= 1
                if event.button == 5:
                    if scroll < 70:
                        scroll += 1

        # game logic
        screen.fill(BLACK)
        draw(num)
        pygame.display.flip()
