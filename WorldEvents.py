import math
import os
import pygame.draw
import JsonHandler
import Log


def init():
    # noinspection PyGlobalUndefined
    global x, y, xv, yv, Flag, pause, gun
    x, y, xv, yv, jump = 16, 16, 0, 0, 0
    pause = False
    gun = pygame.image.load('Assets/Images/Pistol.png')
    Flag = pygame.image.load('Assets/TileTextures/Flag.png')
    List = os.listdir('Levels')
    load_textures()
    return List


def get_size(Folderpath):
    DIRECTORY = os.getcwd(); size = 0
    for path, dirs, files in os.walk(DIRECTORY + Folderpath):
        for f in files: fp = os.path.join(path, f); size += os.path.getsize(fp)
    return size


def next_level(direction=1):
    # noinspection PyGlobalUndefined
    global Level, folder, Level_Data, pause
    pause = True
    if folder == '':
        return 'Go To Home Screen'
    else:
        if Level_Data['LevelOrder'].index(Level_Data['CurrentLevel']) + direction == len(Level_Data['LevelOrder']):
            Level_Data['CurrentLevel'] = Level_Data['LevelOrder'][0]
            JsonHandler.savedata(Level_Data, 'Levels/' + folder + '/Files/Level.json')
            return 'Go To Home Screen'
        else:
            Data = Level_Data['LevelOrder'].index(Level_Data['CurrentLevel']) + direction
            Level_Data['CurrentLevel'] = Level_Data['LevelOrder'][Data]
            Log.log('Level ' + str(Data)); Log.log(Level_Data['CurrentLevel'])
            try:
                Level_File = open('Levels/' + folder + '/' + Level_Data['CurrentLevel'], 'x')
                Level_File.close()
                Level_File = open('Levels/' + folder + '/' + Level_Data['CurrentLevel'], 'r')
            except FileExistsError:  Level_File = open('Levels/' + folder + '/' + Level_Data['CurrentLevel'], 'r')
            Level = []
            Level = Level_File.readlines()
            Level_File.close()
            for i in range(len(Level)):
                try:
                    end = False
                    while not end:
                        if '#' in Level[i]: Level.pop(i)
                        else: end = True
                        if not ('\n' in Level[i]): Level[i] = Level[i] + '\n'
                except IndexError: pass
    Log.log('next level : Levels/' + folder + '/' + Level_Data['CurrentLevel'])
    return Level


def load_level(Folder):
    # noinspection PyGlobalUndefined
    global Level, folder, Level_Data
    folder = Folder
    Level_Data = JsonHandler.getdata('\\Levels\\' + Folder + '\\Files\\Level.json')
    try:
        Level_File = open('Levels/' + Folder + '/' + Level_Data['CurrentLevel'], 'x')
        Level_File.close()
        Level_File = open('Levels/' + Folder + '/' + Level_Data['CurrentLevel'], 'r')
    except FileExistsError: Level_File = open('Levels/' + Folder + '/' + Level_Data['CurrentLevel'], 'r')
    Level = Level_File.readlines()
    Level_File.close()
    for i in range(len(Level)):
        try:
            end = False
            while not end:
                if '#' in Level[i]: Level.pop(i)
                else: end = True
                if not ('\n' in Level[i]): Level[i] = Level[i] + '\n'
        except IndexError: pass
    return Level


def load_textures():
    # noinspection PyGlobalUndefined
    global Textures, Texture_Names
    Textures = []
    Texture_Names = []
    for i in range(len(os.listdir('Assets/TileTextures/'))):
        Textures.append(pygame.image.load('Assets/TileTextures/' + str(os.listdir('Assets/TileTextures/')[i])))
        Texture_Names.append(str(os.listdir('Assets/TileTextures')[i]))
    return Textures, Texture_Names


def draw(screen):
    # noinspection PyGlobalUndefined
    global World_Data, x, y, Textures, Texture_Names
    for i in range(len(Level)):
        item = Level[i]
        j = 0; Data = ['', '', '', '']
        while item[j] != ';': Data[0] = Data[0] + item[j]; j += 1
        j += 1
        while item[j] != ';': Data[1] = Data[1] + item[j]; j += 1
        j += 1
        while item[j] != ';': Data[2] = Data[2] + item[j]; j += 1
        j += 1
        while item[j] != ';': Data[3] = Data[3] + item[j]; j += 1
        screen.blit(pygame.transform.rotate(Textures[Texture_Names.index(Data[0])], 90 * int(Data[3])), (int(Data[1]) * 32 - x + 320, (int(Data[2]) * 32 - y + 180)))


def update(screen, Left, Right, Up, Bullet_x, Bullet_y, Bullet_angle, fire, angle, Ammo):
    draw(screen)
    # noinspection PyGlobalUndefined
    global x, xv, y, yv, Level, Flag, pause, gun, Textures, Texture_Names, jumps
    if pause: pause = False; return
    yv += 1
    if fire: xv += math.cos((angle-190)/-60)*20; yv += math.sin((angle-190)/-60)*20
    if Left: xv -= 1
    if Right: xv += 1
    if Up and jumps: yv = -40; jumps = 0

    for i in range(len(Level)):
        item = Level[i]
        j = 0; Data = ['', '', '', '']
        while item[j] != ';': Data[0] = Data[0] + item[j]; j += 1
        j += 1
        while item[j] != ';': Data[1] = Data[1] + item[j]; j += 1
        j += 1
        while item[j] != ';': Data[2] = Data[2] + item[j]; j += 1
        j += 1
        while item[j] != ';': Data[3] = Data[3] + item[j]; j += 1
        for j in range(1, 4): Data[j] = int(Data[j])
        Data[1] = Data[1] * 32; Data[2] = Data[2] * 32
        X_Condition = Y_Condition = False
        if Data[0] != 'Flag.png':
            if Data[1] - 16 < x + (xv*0.1) < Data[1] + 32 + 15:
                if Data[2] - 16 < y < Data[2] + 32 + 15: X_Condition = True
            if Data[1] - 16 < x < Data[1] + 32 + 15:
                if Data[2] - 16 < y + (yv*0.1) < Data[2] + 32 + 15: Y_Condition = True
        else:
            if Data[1] - 12 < x + (xv*0.1) < Data[1] + 32 + 11:
                if Data[2] - 12 < y < Data[2] + 32 + 11: X_Condition = True
            if Data[1] - 12 < x < Data[1] + 32 + 11:
                if Data[2] - 12 < y + (yv * 0.1) < Data[2] + 32 + 11: Y_Condition = True
        if X_Condition and Y_Condition:
            jumps = 1
            if Data[0] != 'Flag.png': yv = 0; xv = 0
            else:
                if next_level() == 'Go To Home Screen': return 'Home'
                else: x = y = 16; xv = yv = 0
                Log.log('Change Level')
                screen.fill((0, 0, 0))
                screen.blit(gun, (306, 164))
                pygame.display.flip()
                return 'pause'
        elif Left or Right:
            if Y_Condition and Data[0] != 'Flag.png': yv = 0; jumps = 1
            if X_Condition and Data[0] != 'Flag.png': xv = 0
        else:
            if Y_Condition and Data[0] != 'Flag.png': yv = 0; xv = 0.9 * xv; jumps = 1
            if X_Condition and Data[0] != 'Flag.png': xv = 0; yv = 0.9 * yv
        for j in range(len(Bullet_x)):
            end = False
            while not end:
                try:
                    if Data[1] - x + 304 < Bullet_x[j] < Data[1] - x + 336:
                        if Data[2] - y + 164 < Bullet_y[j] < Data[2] - y + 192:
                            Bullet_x.pop(j); Bullet_y.pop(j); Bullet_angle.pop(j)
                        else:
                            end = True
                    else:
                        end = True
                except IndexError: end = True

    xv = xv * 0.99; yv = yv * 0.99
    x += xv * 0.1; y += yv * 0.1
    if -0.5 < xv < 0.5: xv = 0


def TileDecide(Tiles):
    pass
