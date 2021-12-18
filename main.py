from vpython import *
from astropy.time import Time
from astroquery.jplhorizons import Horizons

trail = True
simRate = 10000
        
#Simulation Time
t = 0
dt = 10

#scale factor between graphics and actual numbers
scale = 10**10

#Constants
G = (6.67408*(10**(-11)))

#Objects
sun = sphere(
 name = 'sun', 
 mass = 1.9*10**30, 
 radius = 695508000/scale, 
 realpos = vec(0,0,0), 
 pos = vec(0,0,0), 
 vel = vec(0,0,0), 
 acc = vec(0,0,0), 
 color = vec(1,1,0), 
 make_trail = trail
 )

 
def getObject(identifier, name, radius, mass, col):
    o = Horizons(id=identifier, location="@sun", epochs=Time("2020-01-01").jd, id_type='id').vectors()
    obj = sphere(color=col, make_trail=trail)
    obj.name = name
    obj.mass = mass
    obj.realpos = vec(o['x'], o['z'], o['y'])
    obj.realpos *= 1.5*10**11
    obj.pos = obj.realpos/scale
    obj.vel = vec(o['vx'], o['vz'], o['vy'])
    obj.vel *= (1.49597*10**11)/(86400)
    obj.acc = vec(0,0,0)
    obj.radius = radius/scale
    return obj

#Objects Array [Use getObject(JPL id, name, radius, mass, color)]
objects = [
sun, 
getObject(1, 'Mercury', 243900, 7.2*10**23, vec(.66, .33, 0)),
getObject(2, 'Venus', 6051800, 4.86*10**24, vec(.55, .33, 0)),
getObject(3, 'Earth', 6378000, 5.972*10**24, vec(0, 0, 1)),
getObject(301, 'Moon', 1737500, 7.348*10**22, vec(.8,.8,.8)),
getObject(4, 'Mars', 3389000, 6.417*10**23, vec(1, 0, 0)),
getObject('Phobos', 'Phobos', 11000, 10658529896187200, vec(.4, .4, .4)),
getObject('Deimos', 'Deimos', 6200, 1476188406600740, vec(.6, .6, .6)),
getObject(5, 'Jupiter', 69911000, 1.898*10**27, vec(.8, .3, 0)),
getObject(501,'Io', 1821300, 8.9*10**22, vec(.4, .4, .4)),
getObject(6, 'Saturn', 58232000, 5.683*10**26, vec(.8, .8, .4)),
getObject(606, 'Titan', 2575000, 1.35*10**23, vec(.5, .5, .3)),
getObject(7, 'Uranus', 25362000, 8.681*10**25, vec(0, 1, .3)),
getObject(8, 'Neptune', 24622000 ,1.024*10**26, vec(0, .3, 1))
]

#Initialize the objects
def initializeObjects(Array):
    for n in range(len(objects)):
        Array[n].force = vec(0,0,0)
        
#Calculate the force of gravity
def calculateGravForce(Array):
    for n in range(len(Array)):
        for i in range(len(Array)):
            if i > n:
                M = Array[n].mass
                m = Array[i].mass

                rVec = Array[i].realpos-Array[n].realpos
                rHat = norm(rVec)
                r    = mag(rVec)
                
                if r == 0:
                    raise Exception("Two objects are in the same position and gravity has become infinite!")
                    break
                
                fVec = (G*M*m)/(r**(2)) * rHat

                Array[n].force += fVec
                Array[i].force += fVec * -1

#calculate the motion of objects
def calculateMotion(Array):
    for n in range(len(Array)):
        Array[n].acc  = Array[n].force / Array[n].mass
        Array[n].vel += Array[n].acc*dt
        Array[n].realpos += Array[n].vel*dt
        Array[n].pos = Array[n].realpos/scale
        Array[n].force = vec(0,0,0)
        #clear trails at intervals
        if (t%(5*10**7)*dt < 1*dt):
            Array[n].clear_trail()
        

#INITIALIZATION

#Camera

#Fix camera onto an object
followedObject = 3
scene.camera.follow(objects[followedObject])

#Debug

#attach_arrow(moon, 'vel', color = color.yellow, shaftwidth = .003)
#attach_arrow(moon, 'acc', color = color.red, shaftwidth = .00003)

#Initialize objects
initializeObjects(objects)

#Keyboard Callback

def updateFollowedObject():
        global followedObject

        followedObject = followedObject%len(objects)
        scene.camera.follow(objects[followedObject])
        print("Now following " + objects[followedObject].name)


def keyInput(e):

    global dt
    global followedObject

    if (e.key == 'left'):
        followedObject += 1
        updateFollowedObject()
    if (e.key == 'right'):
        followedObject -= 1
        updateFollowedObject()
    
    if (e.key == 'up'):
        dt *= 1.5
    if (e.key == 'down'):
        dt *= 1/1.5

scene.bind('keydown', keyInput)

#LOOP

while True:
    rate(simRate)
    calculateGravForce(objects)
    calculateMotion(objects)
    t += dt
