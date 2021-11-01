from functools import cache
import taichi as ti
import taichi_glsl as tg

ti.init(arch=ti.gpu)

res=512
FrameBuffer=ti.Vector.field(3,float,(res,res))
window=ti.GUI("taichi_moxi",(res,res),fast_gui=True)

@ti.func
def semiRand(x,rate):
    return frac(ti.sin(x)*rate)

@ti.func
def frac(x):
    return x-ti.floor(x)

@ti.kernel
def render(t:float):
    level=6
    for P in ti.grouped(FrameBuffer):
        tile_size=2.0
        color=ti.Vector([0.0,0.0,0.0])
        pos=float(P)+t
        for i in range(level):
            center=tile_size/2.0
            radius=tile_size/2.0
            pos_in=pos%tile_size
            a=pos//tile_size
            c=1-tg.smoothstep((pos_in-center).norm(),radius*0.5,radius)
            chaos=semiRand(a[0]*5.0+a[1]*3.0+0.05*t,10)
            color+=ti.Vector([0.8,0.5,0.3])*c*chaos
            color*=0.8
            tile_size*=2

        FrameBuffer[P]=color


for i in range(10000):
    t=0.05*i
    render(t)
    window.set_image(FrameBuffer)
    
    window.show()

