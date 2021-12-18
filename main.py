#IMPORTS

from vpython import *
from astropy.time import Time
from astroquery.jplhorizons import Horizons


#INFORMATION

#Global User Variables
trail = True
simRate = 10000
        
#Simulation Time
t = 0
dt = 1000

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

#Objects Array [syntax :: getObject(JPL id, name, radius, mass, color)]
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
getObject(6, 'Saturn', 58232000, 5.683*10**26, vec(.8, .8, .4)),
getObject(7, 'Uranus', 25362000, 8.681*10**25, vec(0, 1, .3)),
getObject(8, 'Neptune', 24622000 ,1.024*10**26, vec(0, .3, 1))
]


#Functions

#Initialize the objects so that they are ready for simulation
#this helps to eliminate redundant code in the instantiation of objects
def initializeObjects(Array):
    for n in range(len(objects)):
        Array[n].force = vec(0,0,0)
        
        #will later add things automaticaly such as position, mass, velocity, radius and such from a data query


#Calculate the force of gravity
def calculateGravForce(Array):
    for n in range(len(Array)):
        for i in range(len(Array)):
            if i > n:
                M = Array[n].mass
                m = Array[i].mass

                rVec = Array[i].realpos-Array[n].realpos
                rHat = norm(rVec) #normalize to a unit vector
                r    = mag(rVec) #make vector a scalar
                
                if r == 0:
                    raise Exception("Two objects are in the same position and gravity has become infinite! (divide by zero error)")
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
scene.camera.follow(objects[3])

#Debug

#attach_arrow(moon, 'vel', color = color.yellow, shaftwidth = .003)
#attach_arrow(moon, 'acc', color = color.red, shaftwidth = .00003)

#Initialize objects
initializeObjects(objects)

#LOOP

g1 = graph()
f1 = gcurve(fast=True,color=color.blue)

while True:
    rate(simRate)
    calculateGravForce(objects)
    calculateMotion(objects)
    t += dt
