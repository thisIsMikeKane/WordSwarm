import pygame, pygame.examples, time, os
pygame.init()
main_dir = os.path.split(os.path.abspath(pygame.examples.__file__))[0]
data_dir = os.path.join(main_dir, 'data')
image_path = os.path.join(data_dir, "arraydemo.bmp")

screen = pygame.display.set_mode((640, 480), 0, 32)
slice_h = 40
test_tile = pygame.image.load(image_path).convert()
slicescaled = pygame.Surface((1, slice_h))

going = True
while going:
    going = pygame.QUIT not in [e.type for e in pygame.event.get()]

    screen.fill((0, 0, 0)) #clear screen
    for x in xrange(100):
        texoffset = x
        slicepiece = pygame.Surface((1, 128))
        slicepiece.blit(test_tile, (0,0), (texoffset, 0, 1, 128))
        pygame.transform.scale(slicepiece, (1, slice_h), slicescaled)
        screen.blit(slicescaled, (x, 10))
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()