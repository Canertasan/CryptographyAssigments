import pyprimes,random
from Crypto.Hash import SHA3_256
import hashlib

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    if a < 0:
        a = a+m
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

def KeyGen(E):
    n = E.order
    P = E.generator
    sA = random.randint(2,n-1)
    #generates a random key pair, signs a message and veries the signature.
    QA = sA*P
    return sA, QA


def SignGen(message, E, sA): 
    h = int(hashlib.sha3_256(message).hexdigest(), 16)
    h = h % E.order
    k = random.randrange(0,E.order-1)
    x = (k * E.generator) 
    xr = x.x
    yr =x.y
    r = xr % E.order
    s = (modinv(k,E.order) *(h + sA))  % E.order
    signature = (r,s)
    return signature

def SignVer(message, s, r, E, QA):
    h = int(hashlib.sha3_256(message).hexdigest(), 16)
    h = h % E.order # mod n
    u1 =modinv(s,E.order) * h % E.order 
    u2 = modinv(s,E.order)*r % E.order
    V = u1*E.generator + u2*QA 
    P = E.generator
    p = E.field
    a = E.a
    b = E.b
    #print("Is V on the curver?", (V.y*V.y)%p == (V.x**3+a*V.x+b)%p)
    ux = "NULL"
    if (V.y*V.y)%p == (V.x**3+a*V.x+b)%p :
        return 0
    else:
        return -1