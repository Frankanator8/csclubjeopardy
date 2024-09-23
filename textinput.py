import pygame
import itertools

from text import Text


class TextInput:
    def __init__(self, x, y, textObj, maxLen=None, subchar=""):
        self.x = x
        self.y = y
        self.active = False
        self.text = ""
        self.textObj = textObj
        self.cursor = 0
        self.cursorFlash = False
        self.cursorDelay = 0
        self.maxLen = maxLen
        self.subchar = subchar


    @staticmethod
    def keyPressed(id, keys, prevKeys):
        if keys[id] and not prevKeys[id]:
            return True

        else:
            return False

    def insertAtCursor(self, text):
        self.text = self.text[:self.cursor] + text + self.text[self.cursor:]

    def deleteAtCursor(self):
        if self.cursor != 0:
            self.text = self.text[:self.cursor-1] + self.text[self.cursor:]

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        keyP = lambda x: self.keyPressed(x, keys, prevKeys)
        if mouseClicked and not prevClicked:
            if self.x <= mousePos[0] <= self.x + self.textObj.w + 10 and self.y <= mousePos[1] <= self.y + self.textObj.h + 5:
                self.active = True
                self.cursorFlash = True
                self.cursorDelay = 0

            else:
                self.active = False
                self.cursorFlash = False

        if self.active:
            self.cursorDelay += dt
            if self.maxLen is None:
                maxLen = len(self.text) + 1

            else:
                maxLen = self.maxLen
            if len(self.text) < maxLen:
                if keyP(pygame.K_SPACE):
                    self.insertAtCursor(" ")
                    if self.cursor == len(self.text)-1:
                        self.cursor+=1
                        self.cursorDelay = 0
                        self.cursorFlash = True

                for i in itertools.chain(range(48, 58), range(65, 91), range(97, 123)):
                    if keyP(i):
                        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                            char = chr(i).upper()

                        else:
                            char= chr(i)
                        self.insertAtCursor(char)
                        self.cursor+=1
                        self.cursorDelay = 0
                        self.cursorFlash = True

                if keyP(pygame.K_UNDERSCORE):
                    self.insertAtCursor("_")
                    self.cursor+=1
                    self.cursorDelay = 0
                    self.cursorFlash = True

            if keyP(pygame.K_BACKSPACE):
                self.deleteAtCursor()
                self.cursor -= 1
                self.cursorDelay = 0
                self.cursorFlash = True

            if keyP(pygame.K_LEFT):
                self.cursor -= 1
                self.cursorDelay = 0
                self.cursorFlash = True

            if keyP(pygame.K_RIGHT):
                self.cursor += 1
                self.cursorDelay = 0
                self.cursorFlash = True

            if self.cursorDelay > 0.5:
                self.cursorDelay = 0
                self.cursorFlash = not self.cursorFlash

        if self.cursor < 0:
            self.cursor = 0

        if self.cursor > len(self.text):
            self.cursor = len(self.text)


    def setSubchar(self, char):
        self.subchar = char

    def draw(self, screen):
        renderText = self.text
        if self.subchar != "":
            renderText = self.subchar * (len(self.text))

        self.textObj.set_text(renderText)
        whereCursor = self.textObj.pos[0] + Text(renderText[:self.cursor], self.textObj.font, (0, 0, 0), self.textObj.pos).w

        pygame.draw.rect(screen, (195, 215, 255) if self.active else (255, 255, 255), pygame.Rect(self.x, self.y, self.textObj.w + 10, self.textObj.h + 5))
        self.textObj.render(screen)
        if self.active:
            if self.cursorFlash:
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(whereCursor, self.y+2, 2, self.textObj.h-2))