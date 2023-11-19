import pygame
import glm
from pygame.locals import *

from Renderer import Renderer
from Model import Model
from Shaders import *
from obj import Obj
import math


width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.mixer.music.load("music/skeleton.mp3")
pygame.mixer.music.play(-1)
renderer = Renderer(screen)
actual_Vertex_shader = vertex_shader
actual_Fragment_shader = fragment_shader
renderer.setShader(actual_Vertex_shader, actual_Fragment_shader)
is_dragging = False
old_position = None

comand_list = """c - Command List
r - Reset Shaders
1 - Gourad Fragment Shader
2 - Cell Fragment Shader
3 - Multicolor Fragment Shader
4 - Noise Fragment Shader
5 - Fire Fragment Shader
6 - Heat Vertex Shader
Right Arrow - Next Model
Left Arrow - Previous Model
Mouse Drag - Rotate Model
Mouse Wheel - Zoom Model
w - Move Camera Up
s - Move Camera Down
a - Rotate Camera Arround Left
d - Rotate Camera Arround Right"""
print(comand_list)

modelIndex = 0
models = []
def modelChange(direction):
    global modelIndex
    global models
    if direction == "R":
        if modelIndex == len(models) - 1:
            modelIndex = 0
        else:
            modelIndex += 1
    else:
        if modelIndex == 0:
            modelIndex = len(models) - 1
        else:
            modelIndex -= 1

    renderer.scene.clear()
    renderer.scene.append(models[modelIndex]['model'])
    renderer.lightIntensity = models[modelIndex]['lightIntensity']
    renderer.heatIntensity = models[modelIndex]['heatIntensity']
    renderer.target = models[modelIndex]['lookAt']
    renderer.cameraPosition = glm.vec3(0.0, 0.0, 0.0)
    renderer.dirLight = models[modelIndex]['dirLight']
    if modelIndex == 0:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

#Model loading
#Skull
obj_data = Obj("models/skull/object.obj").parse_data()
model = Model(obj_data)
model.loadTexture("models/skull/texture.bmp")
model.loadNoiseTexture("noises/fire.jpg")
model.position.z = -10
model.position.y = -3
model.rotation.x = -90
model.scale = glm.vec3(0.20, 0.20, 0.20)
modelData = {"model": model, 
             "lightIntensity": 5.0, 
             "heatIntensity": 0.3, 
             "lookAt": glm.vec3(model.position.x, model.position.y + 2 , model.position.z),
             "dirLight": glm.vec3(0, 0, -1)}
models.append(modelData)

#Cone
obj_data = Obj("models/cone/object.obj").parse_data()
model = Model(obj_data)
model.loadTexture("models/cone/texture.bmp")
model.loadNoiseTexture("noises/fire.jpg")
model.position.z = -1
model.position.y = -2
model.scale = glm.vec3(7, 7, 7)
modelData = {"model": model, 
             "lightIntensity": 1.0, 
             "heatIntensity": 0.005, 
             "lookAt": glm.vec3(model.position.x, model.position.y + 0.5 , model.position.z),
             "dirLight": glm.vec3(0, 0, -1)}
models.append(modelData)

#Books
obj_data = Obj("models/books/object.obj").parse_data()
model = Model(obj_data)
model.loadTexture("models/books/texture.bmp")
model.loadNoiseTexture("noises/fire.jpg")
model.position.z = -4
model.position.y = -2
model.scale = glm.vec3(0.1, 0.1, 0.1)
modelData = {"model": model, 
             "lightIntensity": 30.0, 
             "heatIntensity": 0.08, 
             "lookAt": glm.vec3(model.position.x, model.position.y + 0.5 , model.position.z),
             "dirLight": glm.vec3(0, -0.75, -1)}
models.append(modelData)

#Desk
obj_data = Obj("models/desk/object.obj").parse_data()
model = Model(obj_data)
model.loadTexture("models/desk/texture.bmp")
model.loadNoiseTexture("noises/fire.jpg")
model.position.z = -4
model.position.y = -3
model.scale = glm.vec3(0.5, 0.5, 0.5)
modelData = {"model": model, 
             "lightIntensity": 5.0, 
             "heatIntensity": 0.08, 
             "lookAt": glm.vec3(model.position.x, model.position.y + 0.5 , model.position.z),
             "dirLight": glm.vec3(0, -0.75, -1)}
models.append(modelData)

renderer.scene.append(models[modelIndex]['model'])
renderer.lightIntensity = models[modelIndex]['lightIntensity']
renderer.heatIntensity = models[modelIndex]['heatIntensity']
renderer.target = models[modelIndex]['lookAt']
renderer.dirLight = models[modelIndex]['dirLight']

isRunning = True
movement_sensitive = 0.1
sens_x = 1
sens_y = 0.1
distance = abs(renderer.cameraPosition.z- models[modelIndex]['model'].position.z)
radius = distance
zoom_sensitive = 0.5
angle = 0.0
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
        
    renderer.cameraPosition.x = math.sin(math.radians(angle)) * radius + models[modelIndex]['model'].position.x
    renderer.cameraPosition.z = math.cos(math.radians(angle)) * radius + models[modelIndex]['model'].position.z

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_c:
                print(comand_list)
            if event.key == pygame.K_r:
                actual_Fragment_shader = fragment_shader
                actual_Vertex_shader = vertex_shader
            if event.key == pygame.K_1:
                actual_Fragment_shader = gourad_fragment_shader
            if event.key == pygame.K_2:
                actual_Fragment_shader = cell_fragment_shader
            if event.key == pygame.K_3:
                actual_Fragment_shader = multicolor_fragment_shader
            if event.key == pygame.K_4:
                actual_Fragment_shader = noise_fragment_shader
            if event.key == pygame.K_5:
                actual_Fragment_shader = fire_fragment_shader
            if event.key == pygame.K_6:
                actual_Vertex_shader = heat_vertex_shader
            if event.key == pygame.K_RIGHT:
                modelChange("R")
                angle = 0.0
                radius = distance
            if event.key == pygame.K_LEFT:
                modelChange("L")
                angle = 0.0
                radius = distance

            renderer.setShader(actual_Vertex_shader, actual_Fragment_shader)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                is_dragging = True
                old_position = pygame.mouse.get_pos()

            elif event.button == 4:
                if radius > distance * 0.5:
                    radius -= zoom_sensitive             

            elif event.button == 5:
                if radius < distance * 1.5:
                    radius += zoom_sensitive

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                is_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                new_position = pygame.mouse.get_pos()
                deltax = new_position[0] - old_position[0]
                deltay = new_position[1] - old_position[1]
                angle += deltax * -sens_x

                if angle > 360:
                    angle = 0

                if distance > renderer.cameraPosition.y + deltay * -sens_y and distance * -1.5 < renderer.cameraPosition.y + deltay * -sens_y:
                    renderer.cameraPosition.y += deltay * -sens_y

                old_position = new_position
            

    renderer.updateViewMatrix()
    renderer.render()
    pygame.display.flip()

pygame.quit()

