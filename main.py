import requests
import pygame
import json
import os
import sys
from pygame.locals import *


def create_object(id, x, y):
    global all_sprites
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.transform.scale(load_image(f"./icons/{id}.png", "white"), (
        SPRITE_SIZE, SPRITE_SIZE))
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = x
    sprite.rect.y = y
    all_sprites.add(sprite)
    return sprite

def find_reciepe(ingredient1, ingredient2):
    global recipes
    needed = sorted([int(ingredient1), int(ingredient2)])
    for r in recipes:
        if r['ingredients'] == needed:
            return r['results'][0]
    return "-1"

def stack(ingredient1, ingredient2):
    global recipes
    global found
    res = find_reciepe(ingredient1, ingredient2)
    if res != "-1":
        found.add(res)
    return res

with open('data.json') as f:
    data = json.load(f)
    names = data['names']
    recipes = data['recipes']

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    starterpack_font = pygame.font.SysFont('Comic Sans MS', 13)
    found_font = pygame.font.SysFont('Comic Sans MS', 20)
    # переменные
    running = True
    go = False
    holding = None
    SPRITE_SIZE = 55
    prev = False
    programIcon = pygame.image.load('./images/icon.png')

    pygame.display.set_icon(programIcon)
    found = {"1", "2", "3", "4"}

    # функции и подготовка
    def load_image(name, colorkey=None):
        # если файл не существует, то выходим
        if not os.path.isfile(name):
            print(f"Файл с изображением '{name}' не найден")
            sys.exit()
        image = pygame.image.load(name)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    pygame.display.set_caption('PyAlchemy')
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    starter_pack = {"1": ((500, 0, 100, 100), "water", "#779DCA"), "2": ((500, 100, 100, 100), "fire", "#FFB347"), "3": ((500, 200, 100, 100), "earth", "#523A34"), "4": ((500, 300, 100, 100), "air", "#A0E8FF")}
    #x1,x2
    field = {}
    PLAYBOARD_SIZE = 600
    for i in range(0, PLAYBOARD_SIZE):
        field[i] = ["empty"] * PLAYBOARD_SIZE

    all_sprites = pygame.sprite.Group()

    sprite1 = create_object("1", 10, 20)
    sprite2 = create_object("2", 100, 100)
    sprite3 = create_object("3", 80, 200)

    # запуск игры
    objects = {"id1": (10, 20, sprite1, "1", "water"), "id2": (100, 100, sprite2, "2", "fire"), "id3": (80, 200, sprite3, "3", "earth")}
    for y in range(20, 60):
        new_s = ["empty"] * PLAYBOARD_SIZE
        for x in range(10, 50):
            new_s[x] = "id1"
        field[y] = new_s

    for y in range(100, 140):
        new_s = ["empty"] * PLAYBOARD_SIZE
        for x in range(100, 140):
            new_s[x] = "id2"
        field[y] = new_s

    for y in range(200, 240):
        new_s = field[y]
        for x in range(80, 120):
            new_s[x] = "id3"
        field[y] = new_s


    # статусбар
    f1 = pygame.font.Font(None, 36)
    text1 = f1.render('Hello Привет', True,
                      (180, 0, 0))


    def start_screen():
        intro_text = ["Добро пожаловать!", "",
                      "В этой игре вы должны соединять элементы между собой,",
                      "чтобы получать новые"
                      "Цель игры - собрать все 898 элементов",""
                      "Правила:",
                      "1) Соединять можно только два предмета",
                      "(даже если они одинаковые)",
                      "2) В панели слева вы всегда можете получить базовые элементы:",
                      "огонь, вода, земля, воздух",
                      "3) Если при соединении не образуется нового элемента,",
                      "то два элемента пропадают",
                      "Удачной игры!",
                      "Для продолжения нажмите на любую клавишу"]
        fon = pygame.transform.scale(load_image('./images/start-background.jpg'), (600, 600))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 25)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()


    start_screen()

    pygame.mixer.music.load("music/theme.mp3")
    pygame.mixer.music.play(-1, 0.0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_c = event.pos[0]
                y_c = event.pos[1]
                if x_c > (PLAYBOARD_SIZE - 100) and y_c < (PLAYBOARD_SIZE - 100):
                    if field[y_c][x_c] != 'empty':
                        holding = field[y_c][x_c]
                        go = True
                        continue
                    if 0 <= y_c < 100:
                        new_sprite = create_object("1", 540, 40)
                        n_i = len(objects) + 1
                        objects[f"id{n_i}"] = (540, 40, new_sprite, "1")
                        print(objects)
                        # добавляем полученный объект на поле
                        for yy in range(40, 40 + SPRITE_SIZE):
                            new_s = field[yy]
                            for xx in range(540, 540 + SPRITE_SIZE):
                                new_s[xx] = f"id{n_i}"
                            field[yy] = new_s
                    elif 100 <= y_c < 200:
                        new_sprite = create_object("2", 540, 140)
                        n_i = len(objects) + 1
                        objects[f"id{n_i}"] = (540, 140, new_sprite, "2")
                        print(objects)
                        # добавляем полученный объект на поле
                        for yy in range(140, 140 + SPRITE_SIZE):
                            new_s = field[yy]
                            for xx in range(540, 540 + SPRITE_SIZE):
                                new_s[xx] = f"id{n_i}"
                            field[yy] = new_s
                    elif 200 <= y_c < 300:
                        new_sprite = create_object("3", 540, 240)
                        n_i = len(objects) + 1
                        objects[f"id{n_i}"] = (540, 240, new_sprite, "3")
                        print(objects)
                        # добавляем полученный объект на поле
                        for yy in range(240, 240 + SPRITE_SIZE):
                            new_s = field[yy]
                            for xx in range(540, 540 + SPRITE_SIZE):
                                new_s[xx] = f"id{n_i}"
                            field[yy] = new_s
                    elif 300 <= y_c < 400:
                        new_sprite = create_object("4", 540, 340)
                        n_i = len(objects) + 1
                        objects[f"id{n_i}"] = (540, 340, new_sprite, "4")
                        print(objects)
                        # добавляем полученный объект на поле
                        for yy in range(340, 340 + SPRITE_SIZE):
                            new_s = field[yy]
                            for xx in range(540, 540 + SPRITE_SIZE):
                                new_s[xx] = f"id{n_i}"
                            field[yy] = new_s
                else:
                    print(f"Grabbed: {field[y_c][x_c]}")
                    if field[y_c][x_c] != 'empty':
                        holding = field[y_c][x_c]
                        go = True
            elif event.type == pygame.MOUSEBUTTONUP:
                go = False
                holding = None
                prev = 0
                now = 0
            if go:
                y_start = objects[holding][1]
                x_start = objects[holding][0]
                if not prev:
                    prev = event.pos
                else:
                    try:
                        # узнаём насколько и в какую сторону изменилось положение объекта
                        now = event.pos
                        x_change = now[0] - prev[0]
                        y_change = now[1] - prev[1]
                        prev_obj = objects[holding]
                        new_obj = (prev_obj[0] + x_change, prev_obj[1] + y_change, prev_obj[2], prev_obj[3])
                        if new_obj[0] + SPRITE_SIZE > (PLAYBOARD_SIZE - 100) - 1 or new_obj[1] + SPRITE_SIZE > (PLAYBOARD_SIZE - 100) - 1 or new_obj[0] < 1 or new_obj[1] < 0:
                            print('out of zone')
                            continue
                        prev_obj[2].rect.x = prev_obj[2].rect.x + x_change
                        prev_obj[2].rect.y = prev_obj[2].rect.y + y_change
                        objects[holding] = new_obj
                        if prev[1] > now[1]:
                            y_coef = -1
                        else:
                            y_coef = 1
                        if prev[0] > now[0]:
                            x_coef = -1
                        else:
                            x_coef = 1

                        # очищение предыдущих пикселей, которые раньше занимал объект
                        for y in range(prev_obj[1], prev_obj[1] + SPRITE_SIZE):
                            new_s = field[y]
                            for x in range(prev_obj[0], prev_obj[0] + SPRITE_SIZE):
                                # проверка на столкновение с другим объектом
                                new_s[x] = "empty"
                            field[y] = new_s

                        # перенос объекта на новые пиксели
                        for y in range(objects[holding][1], objects[holding][1] + SPRITE_SIZE):
                            new_s = field[y]
                            for x in range(objects[holding][0], objects[holding][0] + SPRITE_SIZE):
                                # проверка на столкновение с другим объектом
                                if field[y][x] == holding or field[y][x] == "empty":
                                    new_s[x] = holding
                                else:
                                    # проверяем достаточно ли один объект находится на другом, чтобы не соединять при простом столкновении сторон
                                    second_obj = field[y][x]
                                    connector_x = objects[second_obj][0]
                                    connector_y = objects[second_obj][1]
                                    if connector_x + 20 <= x <= connector_x + (SPRITE_SIZE - 20) and connector_y + 20 <= y <= connector_y + (
                                            SPRITE_SIZE - 20):
                                        # очищаем поле от соединнёных спрайтов
                                        for y in range(objects[second_obj][1], objects[second_obj][1] + SPRITE_SIZE):
                                            new_s = field[y]
                                            for x in range(objects[second_obj][0], objects[second_obj][0] + SPRITE_SIZE):
                                                new_s[x] = "empty"
                                            field[y] = new_s
                                        for y in range(objects[holding][1], objects[holding][1] + SPRITE_SIZE):
                                            new_s = field[y]
                                            for x in range(objects[holding][0], objects[holding][0] + SPRITE_SIZE):
                                                new_s[x] = "empty"
                                            field[y] = new_s
                                        #соединяем спрайты
                                        all_sprites.remove(objects[second_obj][2])
                                        all_sprites.remove(objects[holding][2])
                                        res = str(stack(objects[second_obj][3], objects[holding][3]))
                                        print("RES IS", res)
                                        if res == "-1":
                                            pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/bad-eff.mp3'),
                                                                         maxtime=600)
                                            print("ERROR")
                                            go = 0
                                            holding = None
                                            prev = 0
                                            now = 0
                                            continue
                                        else:
                                            go = False
                                            holding = None
                                            prev = 0
                                            now = 0
                                            new_sprite = create_object(res, x, y)
                                            n_i = len(objects) + 1
                                            objects[f"id{n_i}"] = (x, y, new_sprite, res, names[res])
                                            print(objects)
                                            pygame.mixer.Channel(0).play(pygame.mixer.Sound('music/eff.mp3'),
                                                                         maxtime=600)
                                            # добавляем полученный объект на поле
                                            for yy in range(y, y + SPRITE_SIZE):
                                                new_s = field[yy]
                                                for xx in range(x, x + SPRITE_SIZE):
                                                    new_s[xx] = f"id{n_i}"
                                                field[yy] = new_s


                            field[y] = new_s
                        prev = event.pos
                    except Exception:
                        pass
        screen.fill(pygame.Color('#272727'))
        pygame.draw.rect(screen, (102,50,114), (0,0, PLAYBOARD_SIZE - 100, PLAYBOARD_SIZE - 100))
        for it in starter_pack:
            pygame.draw.rect(screen, starter_pack[it][2], starter_pack[it][0])
            textsurface = starterpack_font.render(starter_pack[it][1], False, (0, 0, 0))
            screen.blit(textsurface, (starter_pack[it][0][0] + 30, starter_pack[it][0][1] + 30))
        textsurface3 = found_font.render(f"Вы взяли {names[objects[holding][3]]}", False, (102,50,114)) if holding else found_font.render(f"Ждём вашего хода ;)", False, (102,50,114))
        textsurface2 = found_font.render(f"Найдено {len(found)} из 898", False, (102,50,114))
        screen.blit(textsurface3, (165, 510))
        screen.blit(textsurface2, (165, 540))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
