import pygame

pygame.init()
pygame.display.set_caption('Pixel Blitz')
Icon = pygame.image.load('Assets/Images/Pistol.png')
pygame.display.set_icon(Icon)
screen = pygame.display.set_mode((640, 360))
pygame.draw.rect(screen, (64, 64, 64), pygame.Rect(220, 200, 200, 5))
pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(220, 200, 20, 5))
pygame.display.flip()

import math
import os
import random
import sys
import time
from tkinter import messagebox
import WorldEvents as World
import Log as Log
import JsonHandler
from pygame import mixer

mixer.init()
Running = True
Track = 3
pygame.mixer.set_num_channels(8)
music = pygame.mixer.Channel(5)
sfx = pygame.mixer.Channel(4)
Track1 = pygame.mixer.Sound('Assets/Fonts And Sounds/Track1.mp3')
Track2 = pygame.mixer.Sound('Assets/Fonts And Sounds/Track2.mp3')
Track3 = pygame.mixer.Sound('Assets/Fonts And Sounds/Track3.mp3')
ShootSound = pygame.mixer.Sound('Assets/Fonts And Sounds/Shoot.mp3')
pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(220, 200, 140, 5))
pygame.display.flip()
Settings_Data = JsonHandler.getdata('/Assets/Settings.json')
BlackoutBorder = pygame.image.load('Assets/Images/Blackout-Border.png')
font = pygame.font.Font('Assets/Fonts And Sounds/sofachrome.ttf', 64)
background = pygame.image.load('Assets/Images/RedBackground.jpg')
background = pygame.transform.scale(background, (640, 360))
bullet = pygame.image.load('Assets/Images/Bullet.png')
bullet = pygame.transform.rotate(bullet, 90)
clock = pygame.time.Clock()
Degrees = 0
angle = 0
Ammo = 0
Shoot = False
Bullets_x = [0]
Bullets_y = [0]
Bullets_angle = [180]
DIRECTORY = os.getcwd()
mouse_x, mouse_y = pygame.mouse.get_pos()
screen.blit(background, (0, 0))
pygame.draw.rect(screen, (0, 0, 0), (131, 141, 378, 77), 0)
pygame.draw.rect(screen, (255, 0, 0), (131, 141, 378, 77), 5)
text = font.render('Start', True, (255, 0, 0))
screen.blit(text, (141, 138))
pygame.display.flip()
font16 = pygame.font.Font('Assets/Fonts And Sounds/sofachrome.ttf', 16)
Pause = Settings = click = debug = Left = Right = Up = False
pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(220, 200, 50, 5))
pygame.display.flip()
import LevelEditor


def init():
    global screen, Settings, bullet, Settings_Data, BlackoutBorder, font16, background, Ammo,  clock, music, ShootSound, Track1, Track2, Track3, Icon
    pygame.init()
    pygame.display.set_caption('Pixel Blitz')
    Icon = pygame.image.load('Assets/Images/Pistol.png')
    pygame.display.set_icon(Icon)
    screen = pygame.display.set_mode((640, 360))
    pygame.draw.rect(screen, (64, 64, 64), pygame.Rect(220, 200, 200, 5))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(220, 200, 20, 5))
    pygame.display.flip()
    mixer.init()
    Settings_Data = JsonHandler.getdata('/Assets/Settings.json')
    BlackoutBorder = pygame.image.load('Assets/Images/Blackout-Border.png')
    background = pygame.image.load('Assets/Images/RedBackground.jpg')
    background = pygame.transform.scale(background, (640, 360))
    clock = pygame.time.Clock()
    pygame.mixer.set_num_channels(8)
    music = pygame.mixer.Channel(5)
    Track1 = pygame.mixer.Sound('Assets/Fonts And Sounds/Track1.mp3')
    Track2 = pygame.mixer.Sound('Assets/Fonts And Sounds/Track2.mp3')
    Track3 = pygame.mixer.Sound('Assets/Fonts And Sounds/Track3.mp3')
    ShootSound = pygame.mixer.Sound('Assets/Fonts And Sounds/Shoot.mp3')
    Settings = False
    Ammo = 0
    font16 = pygame.font.Font('Assets/Fonts And Sounds/sofachrome.ttf', 8)
    bullet = pygame.image.load('Assets/Images/Bullet.png')
    bullet = pygame.transform.rotate(bullet, 90)


def new_track():
    if random.randint(0, 10000):
        return
    global Track, Track1, Track2, Track3
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




class Player:
    def __init__(self):
        self.image = pygame.image.load('Assets/Images/Pistol.png')
        self.Bullets_Image = pygame.image.load('Assets/Images/Bullet.png')
        self.imageRotated = self.image
        self.font = pygame.font.Font('Assets/Fonts And Sounds/sofachrome.ttf', 16)

    def update(self):
        global mouse_x, mouse_y, debug, Bullets_x, Bullets_y, Bullets_angle, angle
        Degrees = (mouse_x-320), (mouse_y-180)
        angle = math.atan2(Degrees[1], Degrees[0])*-60
        self.imageRotated = pygame.transform.rotate(self.image, angle)
        filler1, filler2, ImgWidth, ImgHeight = self.imageRotated.get_rect()
        x_change, y_change = self.step(0, 0, 20, angle)
        x_change2, y_change2 = self.step(0, 0, -6, angle+90)
        x_change += x_change2
        y_change += y_change2
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(304, 164, 32, 32), 1)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(305, 165, 30, 30), 0)
        screen.blit(self.imageRotated, (320-(ImgWidth//2)+x_change, 180-(ImgHeight//2)+y_change))
        if debug:
            pygame.draw.rect(screen, (255, 120, 0), pygame.Rect(320-2+x_change, 178+y_change, 4, 4))
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(320-2, 178, 4, 4))
        if len(Bullets_x):
            for i in range(len(Bullets_x)):
                Bullets_data = self.step(Bullets_x[i], Bullets_y[i], 10, Bullets_angle[i])
                Bullets_x[i] = Bullets_data[0]
                Bullets_y[i] = Bullets_data[1]
                Bullets_Image_Rotated = pygame.transform.rotate(self.Bullets_Image, Bullets_angle[i])
                Bullets_data = Bullets_Image_Rotated.get_rect()
                screen.blit(Bullets_Image_Rotated, (Bullets_x[i]-(Bullets_data[2]//2), Bullets_y[i]-(Bullets_data[3]//2)))
                i += 1

            for i in range(len(Bullets_x)):
                try:
                    if (not -10 < Bullets_x[i] < 650) and (not -10 < Bullets_y[i] < 370):
                        Bullets_x.pop(i)
                        Bullets_y.pop(i)
                        Bullets_angle.pop(i)
                except IndexError:
                    pass

    def draw(self):
        global angle, click, Pause, Running, Settings
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.imageRotated = pygame.transform.rotate(self.image, angle)
        filler1, filler2, ImgWidth, ImgHeight = self.imageRotated.get_rect()
        x_change, y_change = self.step(0, 0, 20, angle)
        x_change2, y_change2 = self.step(0, 0, -6, angle + 90)
        x_change += x_change2
        y_change += y_change2
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(304, 164, 32, 32), 1)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(305, 165, 30, 30), 0)
        screen.blit(self.imageRotated, (320-(ImgWidth//2)+x_change, 180-(ImgHeight//2)+y_change))
        global Bullets_x, Bullets_y, Bullets_angle
        if len(Bullets_x):
            for i in range(len(Bullets_x)):
                Bullets_Image_Rotated = pygame.transform.rotate(self.Bullets_Image, Bullets_angle[i])
                Bullets_data = Bullets_Image_Rotated.get_rect()
                screen.blit(Bullets_Image_Rotated, (Bullets_x[i]-(Bullets_data[2]//2), Bullets_y[i]-(Bullets_data[3]//2)))
        #Draw Pause Screen
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 10, 200, 30), 0)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, 200, 30), 2)
        text = self.font.render('Resume', True, (255, 0, 0))
        textrect = text.get_rect()
        screen.blit(text, (110 - textrect[2] // 2, 10 + 5))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 45, 200, 30), 0)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 45, 200, 30), 2)
        text = self.font.render('Settings', True, (255, 0, 0))
        textrect = text.get_rect()
        screen.blit(text, (110 - textrect[2] // 2, 45 + 5))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 80, 200, 30), 0)
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 80, 200, 30), 2)
        text = self.font.render('Main Menu', True, (255, 0, 0))
        textrect = text.get_rect()
        screen.blit(text, (110 - textrect[2] // 2, 80 + 5))
        #Pause Screen Buttons collisions
        if mouse_x in range(10, 210) and mouse_y in range(10, 40) and click:
            Pause = False
        if mouse_x in range(10, 210) and mouse_y in range(45, 75) and click:
            Settings = True
        if mouse_x in range(10, 210) and mouse_y in range(80, 110) and click:
            Running = Pause = False


    def fire(self):
        global Bullets_x, Bullets_y, Bullets_angle, angle, Ammo, sfx, ShootSound
        if Ammo:
            sfx.play(ShootSound)
            Bullets_data = self.step(320, 180, 10, angle)
            Bullets_x.append(Bullets_data[0])
            Bullets_y.append(Bullets_data[1])
            Bullets_angle.append(angle)
            Ammo -= 1

    @staticmethod
    def step(x_pos, y_pos, distance, Angle, Dont_Add=False):
        if Dont_Add:
            new_x = distance * math.cos(Angle/-60)
            new_y = distance * math.sin(Angle/-60)
        else:
            new_x = x_pos + (distance * math.cos(Angle/-60))
            new_y = y_pos + (distance * math.sin(Angle/-60))
        return new_x, new_y




def home_screen():
    music.set_volume(int(Settings_Data['Volume'])/100)
    # noinspection PyGlobalUndefined
    global mouse_x, mouse_y, clock, click, background, font, Running, Settings, Icon
    icon = pygame.image.load('Assets/Images/settings.png')
    Running = True
    while Running:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Log.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                if mouse_x in range(131, 509) and mouse_y in range(141, 218):
                    Running = False

        if mouse_x in range(600, 632) and mouse_y in range(320, 352):
            if click:
                Settings = True
                settings_menu()

        if not music.get_busy():
            new_track()
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (131, 141, 378, 77), 0)
        pygame.draw.rect(screen, (255, 0, 0), (131, 141, 378, 77), 5)
        text = font.render('Start', True, (255, 0, 0))
        text = pygame.transform.scale(text, (358, 77))
        screen.blit(text, (141, 138))
        screen.blit(icon, (600, 320))
        pygame.display.flip()
        clock.tick(30)

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (64, 64, 64), pygame.Rect(230, 200, 180, 5), 0)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(230, 200, 45, 5), 0)
    pygame.display.flip()


def get_levels():
    # noinspection PyGlobalUndefined
    global Levels_List
    Levels_List = []
    for i in range(len(os.listdir('Levels'))):
        if os.path.isdir('Levels/' + os.listdir('Levels')[i]):
            Levels_List.append(os.listdir('Levels')[i])


def draw_menu():
    # noinspection PyGlobalUndefined
    global click, Level, Levels_List
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
                        if answer == 'yes': Level = LevelEditor.New_Level(screen); return True
    return False


def level_select():
    # noinspection PyGlobalUndefined
    global Difficulty, DifficultyText, Level, click, Levels_List, Level_Folder
    # noinspection PyPep8Naming
    Level = False
    Done = False
    # get setup
    World.init()
    get_levels()
    Title_Font = pygame.font.Font('Assets/Fonts And Sounds/NineTsukiRegular.ttf', 64)
    Title = Title_Font.render('Level Select', True, (255, 0, 0))
    DoneText = Title_Font.render('Done', True, (255, 0, 0))
    Levels_List = []
    for i in range(len(os.listdir('Levels'))):
        if os.path.isdir('Levels/' + os.listdir('Levels')[i]):
            if os.listdir('Levels')[i] == 'DefaultLevels' and os.getlogin() == 'chloe': Levels_List.append(os.listdir('Levels')[i])
            elif os.listdir('Levels')[i] != 'DefaultLevels': Levels_List.append(os.listdir('Levels')[i])
    Running = True
    for loading in range(50, 180):
        time.sleep(random.randint(1, 10) * 0.00005)
        pygame.draw.rect(screen, (64, 64, 64), pygame.Rect(230, 200, 180, 5))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(230, 200, loading, 5))
        pygame.display.flip()
    while Running:

        click = False
        MousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Log.close()
                JsonHandler.savedata(Settings_Data, '/Assets/Settings.json')
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MousePos[0] in range(540, 640):
                    if MousePos[1] in range(10, 45): Done = True
                click = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: Done = True

        if Level and Done:
            Level_Folder = Level
            World.load_level(str(Level))
            Settings_Data['LatestLevel'] = str(Level)
            Running = False
        elif Done:
            messagebox.showinfo(title='Pixel Blitz', message='You Need To Select A Level')


        level_editor = Done = draw_menu()
        if level_editor:
            pygame.quit()
            if LevelEditor.run(Level):
                Log.close()
                JsonHandler.savedata(Settings_Data, '/Assets/Settings.json')
                sys.exit()
            else:
                init()
        screen.blit(Title, (0, 0))
        screen.blit(DoneText, (540, 0))
        '''
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 315, 97, 35), 1)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 10, 272, 38), 1)
        pygame.draw.rect(screen, (0, 255, 0), Title.get_rect(), 1)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 60, 204, 29), 1)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 65, 204, 19), 1)
        '''
        clock.tick(20)
        pygame.display.flip()


def main():
    # noinspection PyGlobalUndefined
    global screen, Level_Folder
    for loading in range(50, 180):
        time.sleep(random.randint(1, 10) * 0.00005)
        pygame.draw.rect(screen, (64, 64, 64), pygame.Rect(230, 200, 180, 5))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(230, 200, loading, 5))
        pygame.display.flip()
    # noinspection PyGlobalUndefined
    global Ammo, Pause, Icon, mouse_x, mouse_y, Bullets_x, Bullets_y, Bullets_angle, Degrees, angle, Shoot, clock, click, background, font, Running, Left, Right, Up, Level
    Running = True
    while Running:

        fire = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Log.close()
                JsonHandler.savedata(Settings_Data, '/Assets/Settings.json')
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: Left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: Right = False
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w: Up = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a: Left = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: Right = True
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w: Up = True
                elif event.key == pygame.K_ESCAPE: Pause = True
                elif event.key == pygame.K_r:
                    Ammo = (JsonHandler.getdata('/Levels/'+Level_Folder+'/Files/Level.json'))['AmmoSize']
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                if event.button == 1 and Ammo:
                    Player().fire()
                    fire = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = False

        if not music.get_busy():
            new_track()
        screen.fill((0, 0, 0))
        output = World.update(screen, Left, Right, Up, Bullets_x, Bullets_y, Bullets_angle, fire, angle, Ammo)
        if output:
            screen.blit(pygame.image.load('Assets/Images/Pistol.png'), (304, 164))
            pygame.display.flip()
            if output == 'Home':
                Running = False
                Settings_Data['LatestLevel'] = 'NoLevel'
            elif output == 'pause':
                pass
            for fill in range(0, 99):
                time.sleep(random.randint(1, 2) * 0.00005)
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 200, fill * 6.4, 5))
                screen.blit(Icon, (304, 164))
                pygame.display.flip()
            screen.fill((0, 0, 0))
        music.set_volume(int(Settings_Data['Volume'])/100)
        screen.blit(BlackoutBorder, (0, 0))
        Player().update()
        draw_GUI()
        pygame.display.flip()
        clock.tick(60)


        while Pause:
            music.set_volume(int(Settings_Data['Volume'])/100)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    Log.close()
                    JsonHandler.savedata(Settings_Data, '/Assets/Settings.json')
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Pause = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    click = False

            if not music.get_busy():
                new_track()
            screen.fill((0, 0, 0))
            World.draw(screen)
            screen.blit(BlackoutBorder, (0, 0))
            if Settings:
                settings_menu()
            Player().draw()
            draw_GUI()
            pygame.display.flip()
            clock.tick(60)


def settings_menu():
    # noinspection PyGlobalUndefined
    global Settings, click, screen
    settings_font = pygame.font.Font('Assets/Fonts And Sounds/sofachrome.ttf', 16)
    hold = [False, False]
    red = 0
    red_bool = True
    while Settings:
        music.set_volume(int(Settings_Data['Volume'])/100)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                Log.close()
                JsonHandler.savedata(Settings_Data, '/Assets/Settings.json')
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: Settings = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.MOUSEBUTTONUP:
                click = hold[0] = False

        if red_bool:
            if red == 255: red_bool = False; red -= 1
            else: red += 1
        else:
            if red == 0: red_bool = True; red += 1
            else: red -= 1

        if mouse_x in range(420, 620) and mouse_y in range(20, 30) or hold[0]:
            if click or hold[0]:
                click = False
                hold[0] = True
                Settings_Data['Volume'] = str(round((mouse_x - 420) * 0.5))
                if int(Settings_Data['Volume']) > 100:
                    Settings_Data['Volume'] = 100
                if int(Settings_Data['Volume']) < 0:
                    Settings_Data['Volume'] = 0
            else:
                hold[0] = False

        if mouse_x in range(600, 620) and mouse_y in range(37, 48):
            if click:
                Settings_Data['OpenLatestLevel'] = not Settings_Data['OpenLatestLevel']
                click = False

        if mouse_x in range(20, 224) and mouse_y in range(330, 345):
            if click:
                click = False
                pygame.quit()
                if LevelEditor.run():
                    Log.close()
                    JsonHandler.savedata(Settings_Data, '/Assets/Settings.json')
                    sys.exit()
                else:
                    init()
                    return

        screen.fill((int(red * 0.1), 0, 0))
        draw_line(screen, (64, 64, 64), (420, 20), (620, 20), 5)
        draw_line(screen, (255, 255, 255), (420, 20), (420 + int(Settings_Data['Volume']) * 2, 20), 5)
        draw_line(screen, (64, 64, 64), (600, 42.5), (620, 42.5), 11)
        if Settings_Data['OpenLatestLevel']:
            pygame.draw.circle(screen, (255, 255, 255), (620, 42.5), 8)
        else:
            pygame.draw.circle(screen, (255, 255, 255), (602, 42.5), 8)
        text = settings_font.render('Volume', True, (255, 255, 255))
        textrect = text.get_rect()
        screen.blit(text, (20, 22.5 - (textrect[3] // 2)))
        text = settings_font.render('Resume level on startup', True, (255, 255, 255))
        textrect = text.get_rect()
        screen.blit(text, (20, 42.5 - (textrect[3] // 2)))
        text = settings_font.render('Level Editor', True, (255, 255, 255))
        textrect = text.get_rect()
        screen.blit(text, (20, 337.5 - (textrect[3] // 2)))
        pygame.display.flip()
        clock.tick(30)


def draw_GUI():
    global screen, bullet, font16, Ammo
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 340, 100, 20), 3, 3)
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(3, 343, 94, 14), 0)
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(3, 343, 94, 14), 0, 3)
    screen.blit(bullet, (100, 340))
    screen.blit(bullet, (105, 340))
    screen.blit(bullet, (110, 340))
    bullet_text = font16.render(str(Ammo), True, (255, 255, 255))
    screen.blit(bullet_text, (125, 338))



def draw_line(surface, color, start, end, width):
    pygame.draw.line(surface, color, start, end, width)
    pygame.draw.circle(surface, color, start, width / 2)
    pygame.draw.circle(surface, color, end, width / 2)


def save(Data):
    # noinspection PyGlobalUndefined
    global Folder, Settings_Data
    try:
        File = open(Folder + '/' + Settings_Data['CurrentLevel'], 'x')
    except FileExistsError:
        File = open(Folder + '/' + Settings_Data['CurrentLevel'], 'r')
    File.writelines(Data)
    File.close()


Log.init()
if Settings_Data['OpenLatestLevel'] and Settings_Data['LatestLevel'] != 'NoLevel':
    World.init()
    World.load_level(Settings_Data['LatestLevel'])
    main()
while True:
    home_screen()
    level_select()
    main()
