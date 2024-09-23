import random
import sys

import pygame

from card import Card
from player import Player
from screen import Screen
from text import Text

pygame.init()
Screen.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeopardy")
cards = []
questions = ["The study of the principles and use of computers.",
             "The theory and dev of computer systems \nable to perform tasks that normally \nrequire human intelligence",
             "The most popular programming language \n(TIOBE index)",
             "Computers, at their most basic level, \noperate in this system.",
             "OOP's 4 principles.",
             "A function that calls itself",
             "Notation that tells you the time complexity \nof an algorithm",
             "An algorithm for finding the shortest path on \na non-looping weighted edge graph.",
             "The default sort for Python",
             "Mathematical method of securely generating a \nsymmetric cryptographic key over public channels",
             "The pointy thing",
             "The part that powers AI and graphics",
             "Part of computer that acts as quicker memory \naccess to run apps",
             "Senior school laptop model",
             "The most recent wifi standard \n(in 802.11xx form)",
             "Former CEO of Apple, launched iPhone in 2007",
             "Founder of NVIDIA, first-gen \nTaiwanese immigrant",
             "Creator of Linux and Git",
             "Designer and implementer of C++",
             "First programmer",
             "Gray and maroon",
             "Completion of the lyrics: _ _ _ _ _ _ _ \nyou can take me ___ __ __",
             "The powerhouse of the cell",
             "An indie video game about farming in a \npixelated world.",
             "A flowering plant belonging to the \nPoeceae family and has narrow, blade-like leaves"]

answers = ["What is Computer Science?",
           "What is Artificial Intelligence?",
           "What is Python?",
           "What is binary?",
           "What is encapsulation, inheritance, \npolymorphism, and abstraction?",
           "What is recursion?",
           "What is Big O Notation?",
           "What is Dijkstra's Algorithm?",
           "What is TimSort?",
           "What is the Diffie-Hellman Key Exchange?",
           "What is a cursor/mouse?",
           "What is a GPU?",
           "What is RAM?",
           "What is a Latitude 3190?",
           "What is 802.11ax?",
           "Who is Steve Jobs?",
           "Who is Jensen Huang?",
           "Who is Linus Torvalds?",
           "Who is Bjarne Stroustrup?",
           "Who is Ada Lovelace?",
           "What are Conestoga's colors?",
           "What is H O T T O G O, Hot to go?",
           "What is the mitochondria?",
           "What is Stardew Valley?",
           "What is grass?"]
clock = pygame.time.Clock()

for j in range(5):
    for i in range(1, 6):
        cards.append(Card(j, i, questions[j*5+(i-1)], answers[j*5+(i-1)]))

for i in range(2):
    random.choice(cards).dailydouble = True


running = True
prevClicked = False
prevKeys = pygame.key.get_pressed()
stage = 0
questionTime = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    dt = clock.get_time()/1000
    clicked = pygame.mouse.get_pressed()[0]
    keys = pygame.key.get_pressed()
    mousePos = pygame.mouse.get_pos()
    if stage == 0:
        [card.tick(dt, clicked, mousePos, prevClicked, keys, prevKeys) for card in cards]

    elif stage == 1:
        Screen.drawText = "Topic: debugging. Make your wagers!"
        if keys[pygame.K_SPACE] and not prevKeys[pygame.K_SPACE]:
            stage = 2
            pygame.mixer.Sound("jeopardy.mp3").play()


    else:
        Screen.drawText = f"What is it called \nwhen you talk to an inanimate\nobject like a rubber duck and\nexplain your code to debug?{'' if questionTime < 30 else '\nTime\'s up!'}"
        questionTime += dt

    if Screen.curr == Screen.BOARD:
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, 267, 50))
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(267, 0, 267, 50))
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(534, 0, 267, 50))
        Text(f"{Player.money[0]} shekels", ("Calibri", 30), (255, 255, 255) if Player.turn == 0 else (0, 0, 0), (0, 0)).centerAt(133, 25).render(screen)
        Text(f"{Player.money[1]} shekels", ("Calibri", 30), (255, 255, 255) if Player.turn == 1 else (0, 0, 0), (0, 0)).centerAt(400, 25).render(screen)
        Text(f"{Player.money[2]} shekels", ("Calibri", 30), (255, 255, 255) if Player.turn == 2 else (0, 0, 0), (0, 0)).centerAt(666, 25).render(screen)
        Text("Gen CS", ("Calibri", 20), (255, 255, 255), (0, 0)).centerAt(80, 75).render(screen)
        Text("Algorithms", ("Calibri", 20), (255, 255, 255), (0, 0)).centerAt(240, 75).render(screen)
        Text("Computer Parts", ("Calibri", 20), (255, 255, 255), (0, 0)).centerAt(400, 75).render(screen)
        Text("Famous People", ("Calibri", 20), (255, 255, 255), (0, 0)).centerAt(560, 75).render(screen)
        Text("Not CS", ("Calibri", 20), (255, 255, 255), (0, 0)).centerAt(720, 75).render(screen)
        [card.draw(screen) for card in cards]
        alldone = True
        for card in cards:
            if not card.shown:
                alldone = False

        if alldone:
            stage = 1
            Screen.curr = Screen.TEXT

    elif Screen.curr == Screen.TEXT:
        screen.fill((0, 6, 149))
        Text(Screen.drawText, ("Calibri", 40), (255, 255, 255), (0, 0)).centerAt(400, 300).render(screen)

    else:
        screen.fill((0, 6, 149))
        Text(Screen.drawText, ("Calibri", 40), (255, 255, 255), (0, 0)).centerAt(400, 300).render(screen)
        Screen.input.draw(screen)
        Screen.input.tick(dt, mousePos, clicked, prevClicked, keys, prevKeys)

    clock.tick()
    pygame.display.flip()
    prevKeys = keys
    prevClicked = clicked

pygame.quit()
sys.exit()