from BinPackingEnv import BinPackingEnv
import pygame

pygame.init()
pygame.display.set_caption("2d Bin Circle Packing Simulation")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1560, 900))



circles = [20, 20, 10, 30, 20]
bin = BinPackingEnv(circles)


def update_display(): # regular display updater
    screen.fill((0, 0, 0))


# loop variables
started = False # status of running the simulation

# main loop
update_display()
running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not started:
            pass

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: # quit program
                running = False

            elif event.key == pygame.K_DELETE or event.key == pygame.K_c: # clear graph
                pass
                started = False
            
            elif (event.key == pygame.K_RETURN or event.key == pygame.K_s) and not started: # start simulation
                pass 
                started = False

            elif event.key == pygame.K_t: # for testing
                print("test started")

    #update_display()
    pygame.display.flip()

pygame.quit()

