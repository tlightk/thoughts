import sys  # allows things like create platform independent file paths
import pygame   # import pygame package
from pygame.locals import *     # import constants and functions
import tkinter  # this is for messagebox
from tkinter import messagebox
import random   # this is the randomizer

if not pygame.font: print('Warning, fonts disabled')    # print warning messages if font or mixer modules not available
if not pygame.mixer: print('Warning, sound disabled')

# Setup pygame
mainClock = pygame.time.Clock()
pygame.init()
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1900, 1000))
pygame.display.set_caption('thoughts')

# Game Font
font = pygame.font.SysFont(None, 72)
main_font = pygame.font.SysFont(None, 108)
next_font = pygame.font.SysFont(None, 72)

# Draws text at top left corner
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# # Click detection
click = False

# Global variables
seconds_passed = 0
all_letters = ''
wpm = 0
missed_words = 0
correct_words = 1

# This is the game loop
def game():
    # Import and Create the background
    game_bg = pygame.image.load('game_screen.png')
    game_bg = pygame.transform.scale(game_bg, (1900, 1000))

    # Game setup functions

    # This gets a random sentence from the text file provided
    def randomSentence():
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    # This checks if the typed words are correct, then adds to total_words
    def check_accuracy(arr1,arr2):
        global missed_words
        global correct_words
        index = 0
        if len(arr1) < len(arr2):   # If user input words < current words, loop up to length of user input
            for word in range(0, len(arr1)):
                if arr2[word] == arr1[index]:
                    total_words.append(arr2[word])
                    correct_words += 1
                    index += 1
                else:
                    missed_words += 1
                    index += 1
        if len(arr1) >= len(arr2):   # If user input words >= current words, loop up to length of current words
            for word in range(0, len(arr2)):
                if arr2[word] == arr1[index]:
                    total_words.append(arr2[word])
                    correct_words += 1
                    index += 1
                else:
                    missed_words += 1
                    index += 1

    # Tracks all letters from total_words
    def calculate_avg_word():
        global all_letters
        all_letters = ''.join(total_words)

    # Game variables and initialization
    global missed_words      # Let python know we are referencing this global variable
    global correct_words    # Let python know we are referencing this global variable
    current_sentence = 'release your thoughts!'
    next_sentence = randomSentence()
    color_yes = (0, 0, 0)
    color_next = (150, 150, 150)
    total_words = []    # This keeps track of all the letters typed
    # word_accuracy = 100 - ((missed_words/correct_words) * 100)

    # Event functions
    # Count up every second
    def add_second():
        global seconds_passed
        seconds_passed += 1
        # print(seconds_passed)

    # Calculates the wpm
    def calculate_wpm():
        global all_letters
        global seconds_passed
        global wpm
        wpm = (len(all_letters) / 5) / (seconds_passed / 60)


    # User event for time passing
    SECONDSEVENT = pygame.USEREVENT
    WPMEVENT = pygame.USEREVENT+1

    pygame.time.set_timer(SECONDSEVENT, 1000)
    pygame.time.set_timer(WPMEVENT, 5000)


    # Displays main text to type on the screen
    # def print_main_text():
    #     show = main_font.render(current_sentence, True, (0, 0, 0))
    #     screen.blit(show, (100, 100))
    def print_main_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    # Displays next text to type on the screen
    # def print_next_text():
    #     show = next_font.render('Next thought: ' + next_sentence, True, color_next)
    #     screen.blit(show, (100, 200))
    def print_next_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    # Displays wpm on the screen after converting to int and string
    def display_wpm():
        show = font.render('Gross WPM: ' + str(int(wpm)), True, (0, 0, 0))
        screen.blit(show, (750, 925))

    # Displays word accuracy on the screen after calculations and converting to string
    def display_accuracy():
        show = font.render('Word accuracy: ' + '%.2f' % (100 - ((missed_words/correct_words) * 100)) + '%', True, (0, 0, 0))
        screen.blit(show, (1200, 925))

    # Setup user input
    user_text = ''
    input_rect = pygame.Rect(150, 600, 256, 72) # Rect coordinates, width, height
    input_rect_color = pygame.Color('lightskyblue3')


    running = True
    while running:
        # Display background/Create a screen for this loop
        screen.blit(game_bg, (0, 0))
        # screen.fill((250,250,250))

        # Display user input
        pygame.draw.rect(screen, input_rect_color, input_rect, 3)   #  Last argument is border width
        text_surface = font.render(user_text + '|', True, color_yes)    # Surface that the text will sit on
        user_text_rec = text_surface.get_rect(center=(955,632))     # Get the text, make a rec, set the center of the rect
        screen.blit(text_surface, user_text_rec)    # Blit text on screen with its rec-centered property
        input_rect.w = max(1600,text_surface.get_width() + 10)  # Set max size of rec with optional option to expand it

        # Display text on screen
        print_main_text(current_sentence, main_font, (0, 0, 0), screen, 950, 250)
        print_next_text('next thought: ' + next_sentence, next_font, color_next, screen, 950, 450)
        display_wpm()
        display_accuracy()

        # Handle input events
        click = False  # Click detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Reset all global variables
                global seconds_passed
                global all_letters
                global wpm
                global missed_words
                global correct_words
                seconds_passed = 0
                all_letters = ''
                wpm = 0
                correct_words = 1
                missed_words = 0
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                else:
                    user_text += event.unicode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if user_text != '':   # Check to make sure input isn't empty
                    typed_words = ' '.join(user_text.split()).split()   # removes leading spaces, then splits
                    current_words = ' '.join(current_sentence.split()).split()  # Get this from current_sentence
                    # print(typed_words)
                    check_accuracy(typed_words, current_words)
                    # print(total_words)
                    calculate_avg_word()
                    # print(all_letters)
                    # print('Correct words: ', correct_words)
                    # print('Missed words: ', missed_words)
                    current_sentence = next_sentence
                    next_sentence = randomSentence()
                    user_text = ''
                else:
                    print('Error! Must have some input!')
            if event.type == SECONDSEVENT:  # Adds 1 to seconds_passed every second
                add_second()
            if event.type == WPMEVENT:  # Calculate wpm every 5 seconds
                calculate_wpm()
                # print(wpm)

        # Events to happen during gameplay

        # Draw everything
        # draw_text('Game Screen', font, (0, 0, 0), screen, 20, 20)

        # Frame rate
        pygame.display.update()
        mainClock.tick(60)


# This function is called when the program starts
def main():
    click = False
    # Import and Create the background
    background = pygame.image.load('main_screen.png')
    background = pygame.transform.scale(background, (1900, 1000))
    # background = pygame.Surface(screen.get_size())
    # background = background.convert()
    # background.fill((250, 250, 250))

    # Display the background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Main loop
    going = True
    while going:

        mx, my = pygame.mouse.get_pos()

        # main menu
        button_1 = pygame.Rect(800, 660, 300, 100)
        button_2 = pygame.Rect(800, 775, 300, 100)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                going = False   # Quits the game
        pygame.draw.rect(screen, (255, 255, 255), button_1, 3)
        pygame.draw.rect(screen, (255, 255, 255), button_2, 3)
        screen.blit(font.render('Start Game', True, (0, 0, 0)), (815, 685))
        screen.blit(font.render('Quit Game', True, (0, 0, 0)), (817, 800))

        # Handle input events
        click = False   # Click detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                root = tkinter.Tk()
                root.withdraw()     # this hides the main tkinter messagebox
                msg_box = messagebox.askokcancel('Exit Game', 'Quit the game?')
                if msg_box:
                    going = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        # Frame rate
        pygame.display.update()
        mainClock.tick(60)

        # Draw everything
        screen.blit(background, (0,0))
        # draw_text('Main Menu', font, (0, 0, 0), screen, 20, 20)
        # pygame.display.flip() # this updates the entire screen as opposed to display.update

    pygame.quit()

main()