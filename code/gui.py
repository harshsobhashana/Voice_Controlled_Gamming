import pygame, chess
from random import choice
from traceback import format_exc
from sys import stderr
from time import strftime
from copy import deepcopy
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

pygame.init()

SQUARE_SIDE = 80
AI_SEARCH_DEPTH = 2

RED_CHECK = (240, 150, 150)
WHITE = (255, 255, 255)
BLUE_LIGHT = (140, 184, 219)
BLUE_DARK = (91, 131, 159)
GRAY_LIGHT = (240, 240, 240)
GRAY_DARK = (200, 200, 200)
CHESSWEBSITE_LIGHT = (212, 202, 190)
CHESSWEBSITE_DARK = (100, 92, 89)
LICHESS_LIGHT = (240, 217, 181)
LICHESS_DARK = (181, 136, 99)
LICHESS_GRAY_LIGHT = (164, 164, 164)
LICHESS_GRAY_DARK = (136, 136, 136)

BOARD_COLORS = [(GRAY_LIGHT, GRAY_DARK),
                (BLUE_LIGHT, BLUE_DARK),
                (WHITE, BLUE_LIGHT),
                (CHESSWEBSITE_LIGHT, CHESSWEBSITE_DARK),
                (LICHESS_LIGHT, LICHESS_DARK),
                (LICHESS_GRAY_LIGHT, LICHESS_GRAY_DARK)]
BOARD_COLOR = choice(BOARD_COLORS)

BLACK_KING = pygame.image.load('../data/black_king.png')
BLACK_QUEEN = pygame.image.load('../data/black_queen.png')
BLACK_ROOK = pygame.image.load('../data/black_rook.png')
BLACK_BISHOP = pygame.image.load('../data/black_bishop.png')
BLACK_KNIGHT = pygame.image.load('../data/black_knight.png')
BLACK_PAWN = pygame.image.load('../data/black_pawn.png')
BLACK_JOKER = pygame.image.load('../data/black_joker.png')

WHITE_KING = pygame.image.load('../data/white_king.png')
WHITE_QUEEN = pygame.image.load('../data/white_queen.png')
WHITE_ROOK = pygame.image.load('../data/white_rook.png')
WHITE_BISHOP = pygame.image.load('../data/white_bishop.png')
WHITE_KNIGHT = pygame.image.load('../data/white_knight.png')
WHITE_PAWN = pygame.image.load('../data/white_pawn.png')
WHITE_JOKER = pygame.image.load('../data/white_joker.png')
ONE = pygame.image.load('../data/one.png')
TWO = pygame.image.load('../data/two.png')
THREE = pygame.image.load('../data/three.png')
FOUR = pygame.image.load('../data/four.jpg')
FIVE = pygame.image.load('../data/five.jpg')
SIX = pygame.image.load('../data/six.jpg')
SEVEN = pygame.image.load('../data/seven.jpg')
EIGHT = pygame.image.load('../data/eight.jpg')
a = pygame.image.load('../data/a.jpg')
b = pygame.image.load('../data/b.jpg')
c = pygame.image.load('../data/c.jpg')
d = pygame.image.load('../data/d.jpg')
e = pygame.image.load('../data/e.jpg')
f = pygame.image.load('../data/f.jpg')
g = pygame.image.load('../data/g.jpg')
h = pygame.image.load('../data/h.jpg')

CLOCK = pygame.time.Clock()
CLOCK_TICK = 15

SCREEN = pygame.display.set_mode((int(8.5 * SQUARE_SIDE), int(8.5 * SQUARE_SIDE)), pygame.RESIZABLE)
SCREEN_TITLE = 'Chess Game'

pygame.display.set_icon(pygame.image.load('../data/chess_icon.ico'))
pygame.display.set_caption(SCREEN_TITLE)


def resize_screen(square_side_len):
    global SQUARE_SIDE
    global SCREEN
    SCREEN = pygame.display.set_mode((8 * square_side_len, 8 * square_side_len), pygame.RESIZABLE)
    SQUARE_SIDE = square_side_len


def print_empty_board():
    SCREEN.fill(BOARD_COLOR[0])
    paint_dark_squares(BOARD_COLOR[1])


def paint_square(square, square_color):
    col = chess.FILES.index(square[0])
    row = 7 - chess.RANKS.index(square[1])
    pygame.draw.rect(SCREEN, square_color, (SQUARE_SIDE * col, SQUARE_SIDE * row, SQUARE_SIDE, SQUARE_SIDE), 0)


def paint_dark_squares(square_color):
    for position in chess.single_gen(chess.DARK_SQUARES):
        paint_square(chess.bb2str(position), square_color)


def get_square_rect(square):
    col = chess.FILES.index(square[0])
    row = 7 - chess.RANKS.index(square[1])
    return pygame.Rect((col * SQUARE_SIDE, row * SQUARE_SIDE), (SQUARE_SIDE, SQUARE_SIDE))


def coord2str(position, color=chess.WHITE):
    # print(position[0],position[1])
    if color == chess.WHITE:
        file_index = int(position[0] / SQUARE_SIDE)
        rank_index = 7 - int(position[1] / SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]
    if color == chess.BLACK:
        file_index = 7 - int(position[0] / SQUARE_SIDE)
        rank_index = int(position[1] / SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]


def print_board(board, color=chess.WHITE):
    if color == chess.WHITE:
        printed_board = board
    if color == chess.BLACK:
        printed_board = chess.rotate_board(board)
    SQUARE_SIDE1 = int(SQUARE_SIDE / 2)
    print_empty_board()
    SCREEN.blit(pygame.transform.scale(ONE, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((8 * SQUARE_SIDE, int(0.25 * SQUARE_SIDE)), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(TWO, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((8 * SQUARE_SIDE, int(1.25 * SQUARE_SIDE)), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(THREE, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((8 * SQUARE_SIDE, int(2.25 * SQUARE_SIDE)), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(FOUR, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((8 * SQUARE_SIDE, int(3.25 * SQUARE_SIDE)), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(FIVE, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((8 * SQUARE_SIDE, int(4.25 * SQUARE_SIDE)), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(SIX, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((8 * SQUARE_SIDE, int(5.25 * SQUARE_SIDE)), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(SEVEN, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((8 * SQUARE_SIDE, int(6.25 * SQUARE_SIDE)), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(EIGHT, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((8 * SQUARE_SIDE, int(7.25 * SQUARE_SIDE)), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(a, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((int(0.25 * SQUARE_SIDE), 8 * SQUARE_SIDE), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(b, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((int(1.25 * SQUARE_SIDE), 8 * SQUARE_SIDE), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(c, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((int(2.25 * SQUARE_SIDE), 8 * SQUARE_SIDE), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(d, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((int(3.25 * SQUARE_SIDE), 8 * SQUARE_SIDE), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(e, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((int(4.25 * SQUARE_SIDE), 8 * SQUARE_SIDE), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(f, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((int(5.25 * SQUARE_SIDE), 8 * SQUARE_SIDE), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(g, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((int(6.25 * SQUARE_SIDE), 8 * SQUARE_SIDE), (SQUARE_SIDE1, SQUARE_SIDE1)))
    SCREEN.blit(pygame.transform.scale(h, (SQUARE_SIDE1, SQUARE_SIDE1)),
                pygame.Rect((int(7.25 * SQUARE_SIDE), 8 * SQUARE_SIDE), (SQUARE_SIDE1, SQUARE_SIDE1)))

    if chess.is_check(board, chess.WHITE):
        paint_square(chess.bb2str(chess.get_king(printed_board, chess.WHITE)), RED_CHECK)
    if chess.is_check(board, chess.BLACK):
        paint_square(chess.bb2str(chess.get_king(printed_board, chess.BLACK)), RED_CHECK)

    for position in chess.colored_piece_gen(printed_board, chess.KING, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_KING, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.QUEEN, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_QUEEN, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.ROOK, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_ROOK, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.BISHOP, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_BISHOP, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.KNIGHT, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_KNIGHT, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.PAWN, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_PAWN, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.JOKER, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(BLACK_JOKER, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))

    for position in chess.colored_piece_gen(printed_board, chess.KING, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_KING, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.QUEEN, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_QUEEN, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.ROOK, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_ROOK, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.BISHOP, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_BISHOP, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.KNIGHT, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_KNIGHT, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.PAWN, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_PAWN, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.JOKER, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_JOKER, (SQUARE_SIDE, SQUARE_SIDE)),
                    get_square_rect(chess.bb2str(position)))

    pygame.display.flip()


def set_title(title):
    pygame.display.set_caption(title)
    pygame.display.flip()


def make_AI_move(game, color):
    set_title(SCREEN_TITLE + ' - Calculating move...')
    new_game = chess.make_move(game, chess.get_AI_move(game, AI_SEARCH_DEPTH))
    set_title(SCREEN_TITLE)
    print_board(new_game.board, color)
    return new_game


def try_move(game, attempted_move):
    for move in chess.legal_moves(game, game.to_move):
        if move == attempted_move:
            game = chess.make_move(game, move)
    return game


def play_as(game, color):
    run = True
    ongoing = True
    joker = 0

    try:
        while run:
            CLOCK.tick(CLOCK_TICK)
            print_board(game.board, color)

            if chess.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
                ongoing = False

            if ongoing and game.to_move == chess.opposing_color(color):
                game = make_AI_move(game, color)

            if chess.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
                ongoing = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                myText1 = "make your move"
                if event.type == pygame.MOUSEBUTTONDOWN:

                    r = sr.Recognizer()
                    print("Please Talk")
                    language = 'en'

                    output = gTTS(text=myText1, lang=language, slow=False)

                    output.save("Output.mp3")
                    playsound("Output.mp3")
                    os.remove("Output.mp3")
                    with sr.Microphone() as source:
                        try:
                            audio_data = r.record(source, duration=5)
                            print("Recognising...")
                            text = r.recognize_google(audio_data)
                            text = text.replace(" ", "")
                            print(text)
                        except sr.UnknownValueError:
                            language = 'en'
                            output = gTTS(text="I didn't get that. Say again", lang=language, slow=False)
                            output.save("Output.mp3")
                            playsound("Output.mp3")
                            os.remove("Output.mp3")
                            print("I didn't get that. Say again")
                            continue
                    l = ['1', '2', '3', '4', '5', '6', '7', '8']
                    k = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
                    flag = True
                    if len(text)!=4:
                        flag = False

                    if text[1] not in l:
                        flag = False
                    if text[-1] not in l:
                        flag = False

                    text = text.replace("A", "1")
                    text = text.replace("a", "1")
                    text = text.replace("B", "2")
                    text = text.replace("b", "2")
                    text = text.replace("C", "3")
                    text = text.replace("c", "3")
                    text = text.replace("D", "4")
                    text = text.replace("d", "4")
                    text = text.replace("E", "5")
                    text = text.replace("e", "5")
                    text = text.replace("F", "6")
                    text = text.replace("f", "6")
                    text = text.replace("G", "7")
                    text = text.replace("g", "7")
                    text = text.replace("H", "8")
                    text = text.replace("h", "8")


                    if flag:
                        leaving_square = coord2str(((int(text[0]) - 1) * SQUARE_SIDE, (int(text[1]) - 1) * SQUARE_SIDE),color)
                        arriving_square = coord2str(((int(text[-2]) - 1) * SQUARE_SIDE, (int(text[-1]) - 1) * SQUARE_SIDE), color)

                    myText = "Please make a valid move"
                    if ongoing and game.to_move == color:
                        if flag == True and len(text) == 4:
                            move = (chess.str2bb(leaving_square), chess.str2bb(arriving_square))
                            if move not in chess.legal_moves(game, game.to_move):
                                language = 'en'
                                output = gTTS(text=myText, lang=language, slow=False)
                                output.save("Output.mp3")
                                playsound("Output.mp3")
                                os.remove("Output.mp3")
                                print("Please make a valid move")
                            else:
                                game = try_move(game, move)
                                print_board(game.board, color)


                        else:
                            language = 'en'
                            output = gTTS(text=myText, lang=language, slow=False)
                            output.save("Output.mp3")
                            playsound("Output.mp3")
                            os.remove("Output.mp3")
                            # print_board(game.board, color)
                            print("Please make a valid move")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == 113:
                        run = False
                    if event.key == 104 and ongoing:  # H key
                        game = make_AI_move(game, color)
                    if event.key == 117:  # U key
                        game = chess.unmake_move(game)
                        game = chess.unmake_move(game)
                        set_title(SCREEN_TITLE)
                        print_board(game.board, color)
                        ongoing = True
                    if event.key == 99:  # C key
                        global BOARD_COLOR
                        new_colors = deepcopy(BOARD_COLORS)
                        new_colors.remove(BOARD_COLOR)
                        BOARD_COLOR = choice(new_colors)
                        print_board(game.board, color)
                    if event.key == 114:
                        os.system("start Rulebook.pdf")

                    if event.key == 112 or event.key == 100:  # P or D key
                        print(game.get_move_list() + '\n')
                        print('\n'.join(game.position_history))
                    if event.key == 101:  # E key
                        print('eval = ' + str(chess.evaluate_game(game) / 100))
                    if event.key == 106:  # J key
                        joker += 1
                        if joker == 13 and chess.get_queen(game.board, color):
                            queen_index = chess.bb2index(chess.get_queen(game.board, color))
                            game.board[queen_index] = color | chess.JOKER
                            print_board(game.board, color)

                if event.type == pygame.VIDEORESIZE:
                    if SCREEN.get_height() != event.h:
                        resize_screen(int(event.h / 8.0))
                    elif SCREEN.get_width() != event.w:
                        resize_screen(int(event.w / 8.0))
                    print_board(game.board, color)
    except:
        print(format_exc(), file=stderr)
        bug_file = open('bug_report.txt', 'a')
        bug_file.write('----- ' + strftime('%x %X') + ' -----\n')
        bug_file.write(format_exc())
        bug_file.write('\nPlaying as WHITE:\n\t' if color == chess.WHITE else '\nPlaying as BLACK:\n\t')
        bug_file.write(game.get_move_list() + '\n\t')
        bug_file.write('\n\t'.join(game.position_history))
        bug_file.write('\n-----------------------------\n\n')
        bug_file.close()


def play_as_white(game=chess.Game()):
    return play_as(game, chess.WHITE)


def play_as_black(game=chess.Game()):
    return play_as(game, chess.BLACK)


def play_random_color(game=chess.Game()):
    color = choice([chess.WHITE, chess.BLACK])
    play_as(game, color)


# chess.verbose = True
play_random_color()
