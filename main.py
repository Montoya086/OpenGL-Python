import pygame
import glm
from pygame.locals import *

from Renderer import Renderer
from Model import Model
from Shaders import *
<<<<<<< Updated upstream
import glm
from obj import Obj
=======
from obj import Obj

>>>>>>> Stashed changes

width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)

<<<<<<< Updated upstream
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

=======
#Model loading
obj = Obj("models/cone/object.obj")
objData = []
for face in obj.faces:
    for vertexInfo in face:
        vertexId, texcoordId, normalId = vertexInfo
        vertex = obj.vertices[vertexId - 1]
        normals = obj.normals[normalId - 1]
        uv = obj.texcoords[texcoordId - 1]
        objData.extend(vertex + uv + normals)


model = Model(objData)
model.loadTexture("models/cone/texture.bmp")
model.position.z = -5
model.position.y = -1
model.scale = glm.vec3(5, 5, 5)
>>>>>>> Stashed changes
renderer.scene.append(model)

isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        renderer.clearColor[0] += deltaTime
    if keys[K_LEFT]:
        renderer.clearColor[0] -= deltaTime
    if keys[K_UP]:
        renderer.clearColor[1] += deltaTime
    if keys[K_DOWN]:
        renderer.clearColor[1] -= deltaTime
    if keys[K_SPACE]:
        renderer.clearColor[2] += deltaTime
    if keys[K_LSHIFT]:
        renderer.clearColor[2] -= deltaTime

    if keys[K_d]:
        model.rotation.y += deltaTime * 50
    if keys[K_a]:
        model.rotation.y -= deltaTime * 50
    if keys[K_w]:
        model.rotation.x += deltaTime * 50
    if keys[K_s]:
        model.rotation.x -= deltaTime * 50


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    renderer.render()
    pygame.display.flip()

pygame.quit()

