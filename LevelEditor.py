import math
import os
import sys
from tkinter import messagebox
import pygame
from pygame import mixer
import JsonHandler
import Log
import WorldEvents
import random
# I ain't documenting this code so you better be able to understand this future me.


def run(Level=''):
    # noinspection PyGlobalUndefined
    global screen, font, DIRECTORY, click, clock, Running, Settings_Data, Folder, Pause, music, Track, Track1, Track2, Track3, color, Textures, Texture_Names, x, y, World_Data, scroll
    Log.log('Opened Level Editor')
    pygame.init()
    mixer.init()
    pygame.mixer.set_num_channels(8)
    music = pygame.mixer.Channel(5)
    Track1 = pygame.mixer.Sound('Assets/Fonts And Sounds/Track1.mp3')
    Track2 = pygame.mixer.Sound('Assets/Fonts And Sounds/Track2.mp3')
    Track3 = pygame.mixer.Sound('Assets/Fonts And Sounds/Track3.mp3')
    font = pygame.font.Font('Assets/Fonts And Sounds/sofachrome.ttf', 16)
    screen = pygame.display.set_mode((640, 360))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Pixel Blitz - Level Editor')
    Textures, Texture_Names = WorldEvents.load_textures()
    Icon = pygame.image.load('Assets/Images/Pistol.png')
    pygame.display.set_icon(Icon)
    if Level == '':
        if level_select(): return True
    else:
        WorldEvents.init()
        World_Data = WorldEvents.load_level(str(Level))
        Settings_Data = JsonHandler.getdata('Levels/' + str(Level) + '/Files/Level.json')
        Folder = 'Levels/' + str(Level)
        Running = False
    UP = DOWN = LEFT = RIGHT = Pause = False
    DIRECTORY = os.getcwd()
    Running = True
    Track = 3
    color = 0
    x, y = 0, 0
    scroll = 1
    while Running:
        mouse_pos = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                save(World_Data)
                return True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP: UP = False
                if event.key == pygame.K_DOWN: DOWN = False
                if event.key == pygame.K_LEFT: LEFT = False
                if event.key == pygame.K_RIGHT: RIGHT = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Pause = True
                if event.key == pygame.K_UP: UP = True
                if event.key == pygame.K_DOWN: DOWN = True
                if event.key == pygame.K_LEFT: LEFT = True
                if event.key == pygame.K_RIGHT: RIGHT = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: click = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: click = True
            if event.type == pygame.MOUSEWHEEL: scroll += event.y

        if UP: y += 3
        if DOWN: y -= 3
        if LEFT: x += 3
        if RIGHT: x -= 3

        screen.fill((32, 32, 32))
        color += 1
        if color == 400: color = 0
        Block = False
        Data = ['', '', '', '']
        Remove = 'False'

        if scroll >= len(Texture_Names):
            scroll -= len(Texture_Names)
        if scroll < 0:
            scroll += len(Texture_Names)

        for i in range(len(World_Data)):
            if len(World_Data[i]) >= 8:
                item = World_Data[i]
                j = 0; Data = ['', '', '', '']
                while item[j] != ';': Data[0] = Data[0] + item[j]; j += 1
                j += 1
                while item[j] != ';': Data[1] = Data[1] + item[j]; j += 1
                j += 1
                while item[j] != ';': Data[2] = Data[2] + item[j]; j += 1
                j += 1
                while item[j] != ';': Data[3] = Data[3] + item[j]; j += 1
                Data[1] = int(Data[1]) * 32; Data[2] = int(Data[2]) * 32
                if click and mouse_pos[1] < 320:
                    if mouse_pos[0] - (int(Data[1]) + x) in range(0, 32) and mouse_pos[1] - (int(Data[2]) + y) in range(0, 32):
                        if pygame.mouse.get_pressed()[0]:
                            World_Data[i] = Data[0] + ';' + str(Data[1]//32) + ';' + str(Data[2]//32) + ';' + str(int(Data[3])-1) + ';\n'
                        elif pygame.mouse.get_pressed()[2]: Remove = i
                        Block = True

        if Remove != 'False': World_Data.pop(Remove)
        if not Block and click and mouse_pos[1] < 320:
            Data[0] = str(Texture_Names[scroll])
            Data[1] = str(math.floor((mouse_pos[0] - x) / 32))
            Data[2] = str(math.floor((mouse_pos[1] - y) / 32))
            Data[3] = '0'
            World_Data.append(Data[0] + ';' + Data[1] + ';' + Data[2] + ';' + Data[3] + ';' + '\n')


        draw()
        draw_menu_bar()
        pygame.display.flip()
        if Pause:
            if pause():
                save(World_Data)
                pygame.quit()
                return True
        clock.tick(60)
    save(World_Data)
    pygame.quit()
    return False


def pause():
    # noinspection PyGlobalUndefined
    global font, click, Running, Pause, screen, color, Textures, x, y, World_Data
    while Pause:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: save(World_Data); return True
            if event.type == pygame.MOUSEBUTTONDOWN: click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: Pause = False

        mouse_pos = pygame.mouse.get_pos()
        screen.fill((32, 32, 32))
        draw()
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 10, 230, 30), 0)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, 230, 30), 2)
        text = font.render('Resume', True, (255, 0, 0))
        screen.blit(text, (10 + 5, 10 + 5))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 45, 230, 30), 0)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 45, 230, 30), 2)
        text = font.render('Change Level', True, (255, 0, 0))
        screen.blit(text, (10 + 5, 45 + 5))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 80, 230, 30), 0)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 80, 230, 30), 2)
        text = font.render('Quit Editor', True, (255, 0, 0))
        screen.blit(text, (10 + 5, 80 + 5))
        if mouse_pos[0] in range(10, 240) and mouse_pos[1] in range(10, 40) and click: Pause = False
        if mouse_pos[0] in range(10, 240) and mouse_pos[1] in range(45, 75) and click: save(World_Data); level_select(); Pause = False
        if mouse_pos[0] in range(10, 240) and mouse_pos[1] in range(80, 110) and click: Running = Pause = False
        pygame.display.flip()


def new_track():
    # noinspection PyGlobalUndefined
    global music, Track, Track1, Track2, Track3
    if random.randint(0, 10000):
        return
    if Track == 1:
        if random.randint(0, 1):
            music.play(Track2)
        else:
            music.play(Track3)
    if Track == 2:
        if random.randint(0, 1):
            music.play(Track1)
        else:
            music.play(Track3)
    if Track == 3:
        if random.randint(0, 1):
            music.play(Track1)
        else:
            music.play(Track2)


def draw_menu():
    # noinspection PyGlobalUndefined
    global click, Level, Levels_List, screen, DIRECTORY, New_Button
    sub_offset = -5
    x_offset = 60
    pygame.draw.rect(screen, (32, 0, 0), pygame.Rect(0, 0, 640, (x_offset+sub_offset)))
    pygame.draw.rect(screen, (16, 0, 0), pygame.Rect(0, x_offset+sub_offset, 640, 360-(x_offset+sub_offset)), 0)
    pygame.draw.line(screen, (255, 0, 0), (0, x_offset+sub_offset), (640, x_offset+sub_offset), 3)
    pygame.draw.circle(screen, (64, 0, 0), (620, 340), 20)
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(617, 325, 6, 30))
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(605, 337, 30, 6))
    Font = pygame.font.Font('Assets/Fonts And Sounds/NineTsukiRegular.ttf', 32)
    if Levels_List:
        for i in range(len(Levels_List)):
            if Levels_List[i] == Level: pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(50, (i * 50) + x_offset, 200, 45), 3)
            else: pygame.draw.rect(screen, (127, 127, 127), pygame.Rect(50, (i*50)+x_offset, 200, 45), 1)
            if len(Levels_List[i]) > 15: Text = Font.render(Levels_List[i][0:12] + str('...'), True, (255, 255, 255))
            else: Text = Font.render(Levels_List[i], True, (255, 255, 255))
            screen.blit(Text, (55, (i*50)+x_offset+5))
            if click:
                if pygame.mouse.get_pos()[0] in range(50, 250):
                    if pygame.mouse.get_pos()[1] in range((i*50)+x_offset, (i*50)+x_offset+45):
                        if Level == Levels_List[i]: Level = False
                        else: Level = Levels_List[i]
                if pygame.mouse.get_pos()[0] in range(600, 640):
                    if pygame.mouse.get_pos()[1] in range(320, 360):
                        answer = messagebox.askquestion('Pixel Blitz - Level Editor', 'Do you want to make a new level?')
                        if answer == 'yes': Level = New_Level(); return True
    return False


def level_select():
    # noinspection PyGlobalUndefined
    global Difficulty, DifficultyText, Level, click, Levels_List, screen, World_Data, Settings_Data, Folder
    Level = False
    Levels_List = []
    for i in range(len(os.listdir('Levels'))):
        if os.path.isdir('Levels/' + os.listdir('Levels')[i]):
            if os.listdir('Levels')[i] == 'DefaultLevels' and os.getlogin() == 'chloe': Levels_List.append(os.listdir('Levels')[i])
            elif os.listdir('Levels')[i] != 'DefaultLevels': Levels_List.append(os.listdir('Levels')[i])
    WorldEvents.init()
    Title_Font = pygame.font.Font('Assets/Fonts And Sounds/NineTsukiRegular.ttf', 64)
    Title = Title_Font.render('Level Select', True, (255, 0, 0))
    DoneText = Title_Font.render('Done', True, (255, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(230, 200, 45, 5))
    pygame.display.flip()
    Done = False
    Running = True
    while Running:
        click = False
        MousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MousePos[0] in range(540, 640):
                    if MousePos[1] in range(10, 45):
                        Done = True
                click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    Done = True

        if Level and Done:
            World_Data = WorldEvents.load_level(str(Level))
            Settings_Data = JsonHandler.getdata('/Levels/' + str(Level) + '/Files/Level.json')
            Folder = 'Levels/' + str(Level)
            Running = False
        elif Done:
            messagebox.showinfo(title='Pixel Blitz - Level Editor', message='You Need To Select A Level')

        Done = draw_menu()
        screen.blit(Title, (0, 0))
        screen.blit(DoneText, (540, 0))
        pygame.display.flip()


def draw():
    # noinspection PyGlobalUndefined
    global World_Data, x, y, Textures, Texture_Names
    for i in range(len(World_Data)):
        item = World_Data[i]
        j = 0; Data = ['', '', '', '']
        while item[j] != ';': Data[0] = Data[0] + item[j]; j += 1
        j += 1
        while item[j] != ';': Data[1] = Data[1] + item[j]; j += 1
        j += 1
        while item[j] != ';': Data[2] = Data[2] + item[j]; j += 1
        j += 1
        while item[j] != ';': Data[3] = Data[3] + item[j]; j += 1
        Texture_Rotated = pygame.transform.rotate(Textures[Texture_Names.index(Data[0])], 90 * int(Data[3]))
        screen.blit(Texture_Rotated, (int(Data[1]) * 32 + x, int(Data[2]) * 32 + y))


def draw_menu_bar():
    # noinspection PyGlobalUndefined
    global screen, Textures, Texture_Names, scroll, click, Settings_Data, World_Data
    pygame.draw.rect(screen, (127, 0, 0), pygame.Rect(0, 320, 640, 40))
    screen.blit(Textures[scroll], (4, 324))
    font = pygame.font.Font('Assets/Fonts And Sounds/NineTsukiRegular.ttf', 16)
    text = font.render('Previous Level', True, (255, 255, 255))
    screen.blit(text, (40, 322))
    text = font.render('Next Level', True, (255, 255, 255))
    screen.blit(text, (40, 342))
    mouse_pos = pygame.mouse.get_pos()
    if click:
        if mouse_pos[0] in range(40, 130):
            if mouse_pos[1] in range(322, 338):
                if Settings_Data['LevelOrder'].index(Settings_Data['CurrentLevel']):
                    save(World_Data)
                    World_Data = WorldEvents.next_level(direction=-1)
                    Settings_Data['CurrentLevel'] = Settings_Data['LevelOrder'][Settings_Data['LevelOrder'].index(Settings_Data['CurrentLevel']) - 1]
            elif mouse_pos[1] in range(342, 358):
                if Settings_Data['LevelOrder'].index(Settings_Data['CurrentLevel']) < len(Settings_Data['LevelOrder']) - 1:
                    save(World_Data)
                    World_Data = WorldEvents.next_level()
                    Settings_Data['CurrentLevel'] = Settings_Data['LevelOrder'][Settings_Data['LevelOrder'].index(Settings_Data['CurrentLevel']) + 1]


def save(Data):
    # noinspection PyGlobalUndefined
    global Folder, Settings_Data
    try:
        File = open(Folder + '/' + Settings_Data['CurrentLevel'], 'x')
    except FileExistsError:
        File = open(Folder + '/' + Settings_Data['CurrentLevel'], 'r')
    File.writelines(Data)
    File.close()


def New_Level():
    # noinspection PyGlobalUndefined
    global clock, screen
    sfont = pygame.font.Font('Assets/Fonts And Sounds/NineTsukiRegular.ttf', 24)
    mfont = pygame.font.Font('Assets/Fonts And Sounds/NineTsukiRegular.ttf', 32)
    Name = ''
    input_rect = pygame.Rect(55, 0, 265, 32)
    color_active = pygame.Color((128, 0, 0))
    color_passive = pygame.Color((64, 0, 0))
    text = mfont.render('Name', True, (255, 255, 255))
    active = False
    end = False
    levels = 1
    MinusRect = pygame.Rect(0, 45, 12, 16)
    PlusRect = pygame.Rect(16, 45, 12, 16)
    while not end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos): active = True
                else: active = False
                if MinusRect.collidepoint(event.pos): levels = max(1, levels-1)
                if PlusRect.collidepoint(event.pos): levels += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: Name = Name[:-1]
                elif event.key == pygame.K_RETURN: end = True
                else: Name += event.unicode
        screen.fill((0, 0, 0))
        if active: color = color_active
        else: color = color_passive
        pygame.draw.rect(screen, color, input_rect)
        pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(1, 51, 14, 4))
        pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(17, 51, 14, 4))
        pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(22, 46, 4, 14))
        text_surface = mfont.render(Name, True, (255, 255, 255))
        LevelsText = sfont.render('Levels:' + str(levels), True, (128, 128, 128))
        screen.blit(text, (0, 0))
        screen.blit(text_surface, (input_rect.x, input_rect.y))
        screen.blit(LevelsText, (35, 41))
        input_rect.w = max(270, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)
    os.mkdir(str(os.getcwd()) + '\\Levels\\' + Name)
    os.mkdir(str(os.getcwd()) + '\\Levels\\' + Name + '\\Files')
    Settings_Data = JsonHandler.getdata('/Levels/DefaultLevels/Files/Level.json')
    LevelOrder = []
    for i in range(levels):
        LevelOrder.append('Level'+str(1+i)+'.txt')
        open(os.getcwd() + '\\Levels\\' + Name + '\\' + LevelOrder[i], 'w').close()
    open(os.getcwd() + '\\Levels\\' + Name + '\\Files\\Level.json', 'w').close()
    Settings_Data['LevelOrder'] = LevelOrder
    JsonHandler.savedata(Settings_Data, os.getcwd() + '\\Levels\\' + Name + '\\Files\\Level.json')

    return Name


if __name__ == "__main__": Log.init(); run()
