def darken(c,f):
    """
    c = (r,g,b), f in [0,1], f is the factor by which each element of c is multiplied
    """
    r,g,b = c
    return (r*f,g*f,b*f)

def mix(c1, c2, f1):
    """
    returns c = f1*c1+(1-f1)*c2
    """
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    def mix(v1,v2):
        return v1*f1 + v2*(1-f1)
    return (mix(r1,r2),mix(g1,g2),mix(b1,b2))



BACKGROUND = (0,0,0)

WHITE = (255,255,255)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)
GREEN = (100,250,100)
PURPLE = (100,0,200)
RED = (220,20,60)