from math import cos, sin, pi, sqrt, exp, atan2
from numpy import ndindex, array, ndarray, dot, empty, linspace, clip, abs, ceil, zeros, repeat
from numpy.linalg import norm
from numpy.random import normal
from numpy.fft import fft2,fftshift
from random import uniform

def vec2(x,y):
    v = empty((2,))
    v[0] = x
    v[1] = y
    return v

def vec3(x,y,z):
    v = empty((3,))
    v[0] = x
    v[1] = y
    v[2] = z
    return v

def vec4(x,y,z,w):
    v = empty((4,))
    v[0] = x
    v[1] = y
    v[2] = z
    v[3] = w
    return v

class Noise:
    def __init__(self, sigma:int, N:int):
        self.sigma = sigma
        self.noise_waves = empty((N,4))

        for n in range(N):
            Xi = normal(0, self.sigma)

            self.noise_waves[n,0] = (3 * self.sigma + Xi) * cos((2 * pi * n) / N)
            self.noise_waves[n,1] = (3 * self.sigma + Xi) * sin((2 * pi * n) / N)
            self.noise_waves[n,2] = uniform(0, 2 * pi)
            self.noise_waves[n,3] = exp(-(pow(Xi, 2))/pow(self.sigma,2))

    def noise(self, x):
        I = 0.0
        for wave in self.noise_waves:
            I += wave[3] * sin(dot(vec2(wave[0],wave[1]), x) + wave[2])
        I = (I/len(self.noise_waves))
        return I
    
    def compute_noise_grid(self, scale, span):
        dim = span
        out = empty((dim,dim))
        s = (scale/dim)
        for i,j in ndindex((dim,dim)):
            p = s*vec2(i,j)
            out[i,j] = self.noise(p)
        return out
    
    def compute_turbulence_grid(self, scale, span, octaves=3):
        dim = span
        out = empty((dim,dim))
        s = (0.5/dim)
        for i,j in ndindex((dim,dim)):
            p = s*vec2(i,j)
            out[i,j] = self.turbulence(p,octaves)
        return out
    
    def turbulence(self, x, octaves=10):
        '''Add octaves of noise to produce a turbulence-like result. Returns 
        a single number which is the intensity of the turbulence.'''
        I = 0
        c=1 #--- You can change this value to adjust the intensity of the turbulence
        #--- Part 3: Insert code that sums octaves of noise producing "turbulence"
        for i in range(octaves):
            I += (1/(c*2**i)) * self.noise((2**i)*x)
        #--- End of Part 3
        return I
  