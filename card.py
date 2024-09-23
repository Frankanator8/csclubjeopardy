import pygame.draw

import player
from screen import Screen
from text import Text


class Card:
    def __init__(self, cat, amount, question, answer):
        self.cat = cat
        self.amount = amount
        self.question = question
        self.answer = answer
        self.dailydouble = False
        self.shown = False

        self.stage = 0
        self.wager = self.amount
        self.index = 0
        self.questionTime = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 6, 149), pygame.Rect(self.cat*160, 100+(self.amount-1)*100, 160, 100))
        if not self.shown:
            pygame.draw.rect(screen, (0, 77, 255), pygame.Rect(self.cat*160, 100+(self.amount-1)*100, 160, 100))
            Text(f"{self.amount}\nshekels", ("Calibri", 18), (255, 255, 255), (0, 0)).centerAt(self.cat*160+80, 100+(self.amount-1)*100+50).render(screen)

        if self.shown:
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.cat*160, 100+(self.amount-1)*100, 160, 100), width=10)

        else:
            pygame.draw.rect(screen, (255, 208, 0), pygame.Rect(self.cat*160, 100+(self.amount-1)*100, 160, 100), width=10)

    def tick(self, dt, mouseClicked, mousePos, prevMouseClicked, keyPressed, prevKeyPressed):
        if self.stage == 0:
            if Screen.curr == Screen.BOARD:
                if not self.shown:
                    if mouseClicked and not prevMouseClicked:
                        if self.cat*160 <= mousePos[0] <= self.cat*160+160 and 100+(self.amount-1)*100 <= mousePos[1] <= 100+(self.amount-1)*100+100:
                            if self.dailydouble:
                                self.stage = 10
                                Screen.curr = Screen.TEXTANDINPUT
                                Screen.drawText = "Daily Double!\nHow much do you wager?"
                                Screen.input.text = ""

                            else:
                                self.stage = 1
                                Screen.curr = Screen.TEXT

        elif self.stage == 10:
            if keyPressed[pygame.K_RETURN] and not prevKeyPressed[pygame.K_RETURN]:
                self.wager = int(Screen.input.text)
                self.stage = 1

        elif self.stage == 1:
            Screen.drawText = f"{self.question}{'' if self.questionTime < 10 else '\nTime\'s up!'}"
            self.questionTime += dt
            if keyPressed[pygame.K_SPACE] and not prevKeyPressed[pygame.K_SPACE]:
                self.stage = 2


        elif self.stage == 2:
            Screen.drawText = self.answer
            if self.index == 3:
                self.stage = 3
                self.shown = True
                Screen.curr = Screen.BOARD

            else:
                if self.dailydouble:
                    if keyPressed[pygame.K_0] and not prevKeyPressed[pygame.K_0]:
                        player.Player.money[player.Player.turn] -= self.wager
                        self.index = 3


                    elif keyPressed[pygame.K_1] and not prevKeyPressed[pygame.K_1]:
                        player.Player.money[player.Player.turn] += self.wager
                        self.index = 3

                else:
                    if keyPressed[pygame.K_0] and not prevKeyPressed[pygame.K_0]:
                        player.Player.money[self.index] -= self.wager
                        self.index+=1

                    if keyPressed[pygame.K_1] and not prevKeyPressed[pygame.K_1]:
                        player.Player.money[self.index] += self.wager
                        player.Player.turn = self.index
                        self.index+=1

                    if keyPressed[pygame.K_2] and not prevKeyPressed[pygame.K_2]:
                        self.index+=1