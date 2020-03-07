import random
import pyprimes
import string
import warnings
from Crypto.Hash import SHA3_256
import hashlib

# This homework did by caghankoksal - 20588 and canertasan - 21224

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

def modinv(a, m):
    if a < 0:
        a = a+m
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m
 
def random_prime(bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        p = random.randrange(2**(bitsize-1), 2**bitsize-1)
        chck = pyprimes.isprime(p)
    warnings.simplefilter('default')    
    return p

def large_DL_Prime(q, bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        isnotPrime = False
        k = random.randrange(2**(bitsize-1), 2**bitsize-1)
        p = k*q+1
        primes  = [2,3,5,7,11]
        for i in primes:
            if ( p % i == 0 ) :
                isnotPrime = True
                break
        if isnotPrime ==False:
            chck = pyprimes.isprime(p) and p.bit_length() == 2048
    warnings.simplefilter('default')    
    return p

def Param_Generator(qsize, psize):
    q = random_prime(qsize)
    p = large_DL_Prime(q, psize-qsize)
    tmp = (p-1)//q
    g = 1
    while g == 1:
        alpha = random.randrange(1, p)
        g = pow(alpha, tmp, p)
    return q, p, g


def GenerateOrRead(filename):
    i = 0
    try: 
        with open(filename , "r") as read_In:
            for line in read_In:
                if i == 0:
                    q = int(line)
                elif i == 1:
                    p = int(line)
                elif i == 2:
                    g = int(line)
                i += 1
            return q, p, g   
    except:
        print("Waiting for computation... It takes averagely 50sec.")
        q,p,g = Param_Generator(224, 2048)
        return q,p,g
    
# Generating private-public key pair
def KeyGen(q, p, g):
    alpha = random.randint(1, q) # private key
    beta = pow(g, alpha, p)         # public key
    return alpha, beta

# Signature generation
def SignGen(message, q, p, g, alpha):
    h = int(hashlib.sha3_256(message).hexdigest(), 16)
    h = h % q
    k = random.randrange(1, q-1)
    r = pow(g, k, p) % q
    s = (alpha * r - k * h) % q
    signature = (s, r)
    return signature

# Signature verification
def SignVer(message, s, r, q, p, g,beta):
    h = int(hashlib.sha3_256(message).hexdigest(), 16)
    h = h % q

    v = modinv(h,q)
    z1 = (s*v) % q
    z2 = (r*v) % q
    res = modinv(g,p)
    u = (pow(res,z1,p)*pow(beta,z2, p)) 
    u = u % p
    u = u % q
    if u == r:
        return 0
    else:
        return -1


def random_string(randomNum):
    total = ""
    for i in range(10):
        x = random.randint(32, 512)
        total += chr(x)
    return total







