# import pygame
# from pygame.locals import *

# def name():
#     pygame.init()
#     screen = pygame.display.set_mode((480, 360))
#     name = ""
#     font = pygame.font.Font(None, 50)
#     while True:
#         for evt in pygame.event.get():
#             if evt.type == KEYDOWN:
#                 if evt.unicode.isalpha():
#                     name += evt.unicode
#                 elif evt.key == K_BACKSPACE:
#                     name = name[:-1]
#                 elif evt.key == K_RETURN:
#                     name = ""
#             elif evt.type == QUIT:
#                 return
#         screen.fill((0, 0, 0))
#         block = font.render(name, True, (255, 255, 255))
#         rect = block.get_rect()
#         rect.center = screen.get_rect().center
#         screen.blit(block, rect)
#         pygame.display.flip()

# if __name__ == "__main__":
#     name()
#     pygame.quit()



# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame
from pygame.locals import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == pygame.KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,42)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = ''
  display_box(screen, question + ": " + str.join(current_string,''))
  while 1:
    inkey = get_key()
    if inkey == pygame.K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == pygame.K_RETURN:
      break
    elif inkey == pygame.K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string = current_string + chr(inkey)
    display_box(screen, question + ": " + current_string)
  try:
    val = int(current_string)
  except ValueError:
    print("That's not an integer!")

  return current_string

def main():
  screen = pygame.display.set_mode((1020,800))
  print(ask(screen, "Name") + " was entered")

if __name__ == '__main__': 
    main()