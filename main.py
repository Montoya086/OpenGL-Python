import pygame
from OpenGL.GL import *

from Renderer import Renderer
from Model import Model
from Shaders import *
import glm
from obj import Obj

width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)

obj = Obj("models/skull/object.obj")

model_list = []
model_data = []
for face in obj.faces:

    for vertex_info in face:
        vertex_id, texcoord_id, normal_id = vertex_info

        vertex = obj.vertices[vertex_id - 1]
        normal = obj.normals[normal_id - 1]

        model_data.extend(vertex + normal)

    model = Model(model_data)
    model_list.append(model)

model = Model(model_data)
model.position.z = -15
model.position.y = -1
model.scale = glm.vec3(0.007, 0.007, 0.007)

renderer.scene.append(model)

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        renderer.clearColor[0] += deltaTime
    if keys[pygame.K_LEFT]:
        renderer.clearColor[0] -= deltaTime
    if keys[pygame.K_UP]:
        renderer.clearColor[1] += deltaTime
    if keys[pygame.K_DOWN]:
        renderer.clearColor[1] -= deltaTime
    if keys[pygame.K_z]:
        renderer.clearColor[2] += deltaTime
    if keys[pygame.K_x]:
        renderer.clearColor[2] -= deltaTime

    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    renderer.render()
    pygame.display.flip()

pygame.quit()