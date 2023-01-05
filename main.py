import pygame
import time
import math
import random
import pygame_screen_recorder
gconst = 9.81
rpf = 150
eage = True


def supersimplify(input):
    if input == 0:
        return 0
    elif input > 0:
        return -1
    elif input < 0:
        return 1


def render():
    for obj in objlist:
        surface = pygame.Surface((obj["size"] * 2, obj["size"] * 2), pygame.SRCALPHA)
        surface.set_colorkey((0, 0, 0))
        surface.set_alpha(128)
        pygame.draw.circle(surface, obj["heat"], (obj["size"], obj["size"]), obj["size"])
        print(campos)
        window.blit(surface, [obj["pos"][0] + campos[0], obj["pos"][1] + campos[1]])
    pygame.display.update()


def physics():
    global objlist
    for obj in objlist:
        obj["heat"][0] += (255 - obj["heat"][0])/1000
        obj["heat"][1] += (255 - obj["heat"][1])/1000
        obj["heat"][2] += (255 - obj["heat"][2])/1000
        if obj["heat"][0] > 255:
            obj["heat"][0] = 255
        if obj["heat"][1] > 255:
            obj["heat"][1] = 255
        if obj["heat"][2] > 255:
            obj["heat"][2] = 255
        if obj["heat"][0] < 0:
            obj["heat"][0] = 0
        if obj["heat"][1] < 0:
            obj["heat"][1] = 0
        if obj["heat"][2] < 0:
            obj["heat"][2] = 0
        for obj2 in objlist:
            if obj == obj2:
                continue

            o1minuso2x = (obj["pos"][0] - obj2["pos"][0])
            o1minuso2y = (obj["pos"][1] - obj2["pos"][1])
            distance = math.sqrt(((o1minuso2x ** 2)+(o1minuso2y ** 2)))
            if distance ** 2 == 0:
                continue
            if distance <= obj["size"] + obj2["size"] or obj["pos"][1] <= 0 or\
                    (eage and (obj["pos"][1] >= size[1] or obj["pos"][0] <= 0 or obj["pos"][0] >= size[0])):
                org = obj["speed"][1]
                obj["speed"][1] = obj["speed"][1] * -1
                obj["pos"][1] += obj["speed"][1]
                o1minuso2x = obj["pos"][0] - obj2["pos"][0]
                o1minuso2y = obj["pos"][1] - obj2["pos"][1]
                distance = math.sqrt(((o1minuso2x ** 2) + (o1minuso2y ** 2)))
                if distance <= obj["size"] + obj2["size"] or obj["pos"][1] <= 0 or\
                        (eage and (obj["pos"][1] >= size[1] or obj["pos"][0] <= 0 or obj["pos"][0] >= size[0])):
                    obj["pos"][1] -= obj["speed"][1]
                    obj["speed"][1] = org
                    org = obj["speed"][0]
                    obj["speed"][0] = obj["speed"][0] * -1
                    obj["pos"][0] += obj["speed"][0]
                    o1minuso2x = obj["pos"][0] - obj2["pos"][0]
                    o1minuso2y = obj["pos"][1] - obj2["pos"][1]
                    distance = math.sqrt(((o1minuso2x ** 2) + (o1minuso2y ** 2)))
                    if distance <= obj["size"] + obj2["size"]:
                        obj["pos"][0] -= obj["speed"][0]
                        obj["speed"][0] = org
                        while distance <= obj["size"] + obj2["size"]:
                            o1minuso2x = obj["pos"][0] - obj2["pos"][0]
                            o1minuso2y = obj["pos"][1] - obj2["pos"][1]
                            distance = math.sqrt(((o1minuso2x ** 2) + (o1minuso2y ** 2)))
                            obj["pos"][0] += o1minuso2x / 1000
                            obj["pos"][1] += o1minuso2y / 1000
                obj["heat"][1] -= 1
                obj["heat"][2] -= 2
                if obj["heat"][0] > 255:
                    obj["heat"][0] = 255
                if obj["heat"][1] > 255:
                    obj["heat"][1] = 255
                if obj["heat"][2] > 255:
                    obj["heat"][2] = 255
                if obj["heat"][0] < 0:
                    obj["heat"][0] = 0
                if obj["heat"][1] < 0:
                    obj["heat"][1] = 0
                if obj["heat"][2] < 0:
                    obj["heat"][2] = 0
                if obj["fliction"]:
                    obj["speed"][0] = obj["speed"][0] * 0.9
                    obj["speed"][1] = obj["speed"][1] * 0.9
                continue
            obj["pos"][0] += obj["speed"][0] / len(objlist)
            obj["pos"][1] += obj["speed"][1] / len(objlist)
            force = ((gconst * ((math.pi*obj["size"]**2)*(math.pi*obj["size"]**2)*obj["mass"]*obj2["mass"])/10) /
                     (distance ** 2))
            angle = math.atan2(o1minuso2y, o1minuso2x)
            obj["speed"][0] += (force * (0-math.cos(angle)))
            obj["speed"][1] += (force * (0-math.sin(angle)))


def setup():
    global objlist
    for i in range(0):
        objlist.append({"pos": [random.randrange(10, size[0] - 10), random.randrange(10, size[1] - 10)],
                        "heat": [255, 255, 255],
                        "speed": [0, 0],
                        "size": 10,
                        "fliction": True,
                        "mass": 0.0025})


objlist = []
pygame.init()
size = (1366, 768)
window = pygame.display.set_mode((1376, 768))
running = True
setup()
click = False
fps = 60
lor = 10
recorded = False
fakeinit = pygame.time.get_ticks()
campos = [0, 0]
pressed = []
while running:
    window.fill((0, 0, 0))
    physics()
    render()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            objlist.append(
                {"pos": [pygame.mouse.get_pos()[0] - campos[0], pygame.mouse.get_pos()[1] - campos[1]],
                 "heat": [255, 255, 255],
                 "speed": [0, 0],
                 "size": lor,
                 "fliction": True,
                 "mass": 0.0025})
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and not recorded:
                recorder = pygame_screen_recorder.pygame_screen_recorder("output.mp4")
                recorded = True
                fakeinit = pygame.time.get_ticks()
            if event.key == pygame.K_w:
                campos[1] += 10
            if event.key == pygame.K_s:
                campos[1] -= 10
            if event.key == pygame.K_a:
                campos[0] += 10
            if event.key == pygame.K_d:
                campos[0] -= 10
    if recorded and recorder.file_count < (pygame.time.get_ticks() - fakeinit) // (rpf*100):
        recorder.click(window)
if recorded:
    recorder.save()
pygame.quit()
