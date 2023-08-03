from perlin_noise import PerlinNoise
import pygame
import WorldEvents
seed = 1


def Generate(x, y, Seed, block_size=50):
    if seed == 0:
        import Log
        Log.init()
        Log.log('\n\n\n\n--==Seed 0 Error==--\n\n\n\n')
        Log.close()
        return
    noise = PerlinNoise(octaves=2, seed=Seed)
    size = {'x': int(block_size), 'y': int(block_size)}
    List = [[noise([x + i/size['x'], y + j/size['y']]) for j in range(1, 1 + size['x'])] for i in range(1, 1 + size['y'])]
    for i in range(len(List)):
        TempVar = []
        for j in range(len(List[i])):
            List[i][j] = (List[i][j] + 0.5) * 100
            if int(List[i][j]) in range(42, 58): TempVar.append(1)
            else: TempVar.append(0)
        List[i] = TempVar
    return List


def draw():
    global seed, screen, Textures, Texture_Names
    screen.fill((255, 0, 0))
    List = Generate(0, 0, seed, 20)
    for i in range(len(List)):
        for j in range(len(List[i])):
            c, cval = [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0]
            for a in range(3):
                for b in range(3):
                    if (i == 19 and a == 2) or (i == 0 and a == 0): cval[0] = 0
                    else: cval[0] = a-1
                    if (j == 19 and b == 1) or (j == 0 and b == 0): cval[1] = 0
                    else: cval[1] = b-1
                    try:
                        if List[i+cval[0]][j+cval[1]]: c[a*3+b] = 1
                    except IndexError:
                        if j == 19 and b == 2: c[a*3+b] = 1
            if 0 not in c: screen.blit(Textures[Texture_Names.index('Flag.png')], (i*32, j*32))
            elif List[i][j]:
                WorldEvents.TileDecide(c)
                pygame.draw.rect(screen, (64, 64, 64), pygame.Rect(i*32, j*32, 32, 32), 0)
    pygame.display.flip()


pygame.init()
Textures, Texture_Names = WorldEvents.load_textures()
screen = pygame.display.set_mode((640, 640))
draw()
Run = True
while Run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); Run = False
        if event.type == pygame.MOUSEBUTTONDOWN: seed += 1; draw()
