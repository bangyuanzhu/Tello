import pygame

# Initialises a window, this needs to be open for the keyboard module to work
def init():
    pygame.init()
    win = pygame.display.set_mode((400, 400))


# Not very well explained in video, but gives TRUE if input keyName is pressed, else FALSE
def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans

# Main function in the module
#def main():


#Nothing here, not important to the module when called elsewhere

# To repeat main() until stopped
#if __name__ == '__main__':
#   init()
#    while True:  # Repeatedly runs main() until exit
#        main()
