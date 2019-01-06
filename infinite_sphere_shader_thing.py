import pygame, numpy, glm

windowsize = [128, 128]
iTime = 0

max_iters = 500
max_dist = 100.0
bg_col = glm.vec3(0.5, 0.5, 0.5)

#rotation matrix around the Y axis.
def rotateY(theta):
    c = numpy.cos(theta)
    s = numpy.sin(theta)
    return glm.mat3(glm.vec3(c, 0, s), glm.vec3(0, 1, 0), glm.vec3(-s, 0, c))

#the signed distance field function
#used in the ray march loop
def sdf(p):
    #a sphere of radius 1.0
    return glm.length(p)-1.0

def mainImage(fragCoord):
    #1 : retrieve the fragment's coordinates
    uv = [fragCoord[0]/windowsize[0], fragCoord[1]/windowsize[0]]
    #2 : camera position and ray direction
    pos = glm.vec3(0.0, 0.0, -20.0)
    direction = glm.normalize(glm.vec3(uv[0], uv[1], 3.0))
    pos = rotateY(iTime/4.0)*pos
    direction = rotateY(iTime/8.0)*direction
    #3 : ray march loop
    #ip will store where the ray hits the surface
    ip = None
    #variable step size
    t = 0.0
    i = 0
    for i in range(max_iters):
        #update position along path
        ip = pos+direction*t
        #gets the shortest distance to the scene
        m = 4.0
        ip = glm.abs(ip-m*0.5) #ip = glm.abs(glm.mod(ip-m*0.5, m)-m*0.5)
        temp = sdf(ip)
        #break the loop if the distance was too small
        #this means that we are close enough to the surface
        if temp < 0.01:
            a = i/max_iters
            diffuse = glm.dot(ip, glm.vec3(0.6, 0.8, 0.0))*0.5+0.5
            ip = glm.vec3(1.0, 1.0, 1.0)*diffuse*(1.0-a)+bg_col*a
            break
        #break if too far
        if temp > max_dist:
            ip = bg_col
            break
        #increment the step along the ray path
        t += temp
    if i == max_iters: ip = bg_col
    #4 : apply color to this fragment
    surface.set_at(fragCoord, ip*255)

pygame.init()
surface = pygame.display.set_mode(windowsize)
pygame.display.set_caption("Infinite Sphere Shader Thing")
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    for x in range(windowsize[0]):
        for y in range(windowsize[1]):
            mainImage([x, y])
            #print("pixel " + str(x*windowsize[1]+y) + " done")
    pygame.display.flip()
    iTime += 0.1 #simulate iTime because I was too lazy to make it use the time library or pygame clock
pygame.quit()
