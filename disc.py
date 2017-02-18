from pylab import *
from matplotlib import pyplot as plt
from matplotlib import animation


class disc(object):
    velocity_transfer = 0.9
    def __init__(self, pos, R=1, vel=[0.,0.], M=1.):
        self.pos = np.array(pos)
        self.R = R
        self.vel = np.array(vel)
        self._vel_cart = self.vel[0]*np.array([np.cos(self.vel[1]), np.sin([self.vel[1]])])
        self.M = M
    def set_vel_rad(self,r,phi):
        self.vel[0]=r
        self.vel[1]=phi
        self._vel_cart = self.vel[0]*np.array([np.cos(self.vel[1]), np.sin([self.vel[1]])])
    def set_vel_cart(self,x,y):
        self._vel_cart[0] = x
        self._vel_cart[1]=y
        self.vel[0] = np.sqrt(x**2+y**2)
        self.vel[1] = -np.arctan2(x,y)+np.pi/2.

    def time_advance(self,dt):
        #self.pos = self.pos + dt*self.vel[0]*np.array([np.cos(self.vel[1]), np.sin(self.vel[1])])
        self.pos[0] += dt*self.vel[0]*np.cos(self.vel[1])
        self.pos[1] += dt*self.vel[0]*np.sin(self.vel[1])
    def detect_collision(self, discs,dt):
        distances = [np.linalg.norm(self.pos-d.pos) for d in discs]
        def minimum(x):
            return distances[x]
        closest = min(range(len(discs)), key=minimum)
        collision=False
        self_vel = self.vel[0]*np.array([np.cos(self.vel[1]), np.sin([self.vel[1]])])
        closest_vel = discs[closest].vel[0]*np.array([np.cos(discs[closest].vel[1]), np.sin([discs[closest].vel[1]])])
        if distances[closest]<=discs[closest].R+self.R+(-self_vel+closest_vel).dot((self.pos-discs[closest].pos)/np.linalg.norm(self.pos-discs[closest].pos))*dt:
            collision=True
        return collision, closest
    def draw(self, ax,color='red'):
        x = np.linspace(self.pos[0]-self.R, self.pos[0]+self.R, 100)
        xd = np.linspace(-self.R, self.R, 100)
        patch = plt.Circle((self.pos[0], self.pos[1]), radius=self.R, color=color)
        #ax.add_patch(patch)
        return patch
    def get_energy(self):
        return 1./2.*self.M*self._vel_cart.dot(self._vel_cart)
def collide(disc1,disc2):
    p0 = disc1._vel_cart * disc1.M + disc2._vel_cart*disc2.M
    d = disc2.pos - disc1.pos
    p2_r = np.linalg.norm(p0)*np.cos(np.arccos(p0.dot(d)/np.linalg.norm(p0)/np.linalg.norm(d)))
    d_normed_polar = np.array([1., np.pi/2. - np.arctan2(d[0],d[1])])
    p2 = p2_r * np.array([np.cos(d_normed_polar[1]), np.sin(d_normed_polar[1])])
    p1 = p0 - p2
    v2 = p2/disc2.M
    v1 = p1/disc1.M
    return v1,v2
    
