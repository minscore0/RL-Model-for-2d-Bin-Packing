from BinPackingEnv import BinPackingEnv
import pygame
import pygame.gfxdraw

pygame.init()
pygame.display.set_caption("2d Bin Circle Packing Simulation")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1560, 900))


circle_radii = [20, 20, 10, 30, 20]
packing_bin = BinPackingEnv(circle_radii)


def update_display(screen, circles, index):  # regular display updater
    screen.fill((0, 0, 0))
    for r, pos in circles[:index]:
        pygame.gfxdraw.circle(screen, 100+pos[0], 800-pos[1], r, (255, 255, 255))

    return None


# active variables
started = False  # status of running the simulation

# main loop
update_display(screen, packing_bin.circles, packing_bin.index)
running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not started:
            pass

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # quit program
                running = False

            elif event.key == pygame.K_DELETE or event.key == pygame.K_c:  # clear graph
                pass
                started = False
            
            elif (event.key == pygame.K_RETURN or event.key == pygame.K_s) and not started:  # start simulation
                pass 
                started = False

            elif event.key == pygame.K_t:  # for testing
                print("test started")

    update_display(screen, packing_bin.circles, packing_bin.index)
    pygame.display.flip()

pygame.quit()

