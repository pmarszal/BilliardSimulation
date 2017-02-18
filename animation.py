from pylab import *
from matplotlib import pyplot as plt
from matplotlib import animation
from disc import *
plt.style.use('ggplot')

R=1.
L=3.*R
# Interesting angle:
alpha0 = np.arccos(L/4./R)
#alpha0 = 0.01

N=10


f = plt.figure(figsize=(14,3.5))

# Placing the discs
discs=[disc(np.array([x*L,0])) for x in range(N)]
discs[0].set_vel_rad(100.,alpha0)

# Do something nice with the masses
# Apparantly Different Masses lead to some Inaccuracies and the Energy is not conserved anymore
#for i in range(len(discs)):
#    discs[i].M = 10./(i+1)**2

print([d.M for d in discs])
ax = plt.axes(xlim=(-1, L*N+L), ylim=(-(L*N+L)/8, (L*N+L)/8))
patches = [ax.add_patch(d.draw(ax, color='red')) for d in discs]    
tend = 1.
dt = 0.001

def data():
    t = 0.0
    while t < tend:
        t+=dt
        yield t

# Die Init Funktion macht irgendwas unwichtiges im Prinzip ist auch egal was drinne steht
def init():
    line =ax.hlines(0,0,20)
    xs = [d.pos[0] for d in discs]
    ys = [d.pos[1] for d in discs]
    scatter = ax.scatter(xs,ys)
    return tuple(scatter)+(line),
def animate(t):
    # Reihenfolge wichtig fuer collision detection
    for i,d in enumerate(discs[:-1]):
        # Checke ob Disc i mit etwas kollidiert
        coll, clos = d.detect_collision(discs[i+1:],dt)
        if coll: # Wenn ja dann aktualisiere die Gescwhindingkeiten
            p1,p2 = collide(discs[i], discs[i+1+clos])
            discs[i+1+clos].set_vel_cart(p2[0],p2[1])
            discs[i].set_vel_cart(p1[0],p1[1])
    # Der Zustand jeder Disc muss einzeln integriert werden
    print('Time: {}, Energy: {}'.format(t, np.sum([d.get_energy() for d in discs])))
    for i in range(len(discs)):
        discs[i].time_advance(dt)
    
    # Hier werden die Kugeln gezeichnet
    for i in range(len(patches)):
        patches[i].center = (discs[i].pos[0],discs[i].pos[1])
    return tuple(patches)#+tuple(scatter,),
        
ani=animation.FuncAnimation(f,animate,
                               frames=data,
                       		interval=16,
                                repeat=False)
plt.show()

