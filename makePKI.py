from random import getrandbits, randrange
from secrets import randbits

tailleP = 512 #nomdre de bit pour generer les nombres premier
RMCheck = 128 #nombre de verification avec rabinMiller


# verifie que le nombre premier est plus grand que la moyenne des 2 premiers les plus proches de lui
def strongPrime(PrimeCandidate):
    # Initialize previous_prime to n - 1
    # and next_prime to n + 1
    previous_prime = PrimeCandidate - 1
    next_prime = PrimeCandidate + 1
    # Find next prime number
    while (rabinMiller(next_prime) == False):
        next_prime += 1
    # Find previous prime number
    while (rabinMiller(previous_prime) == False):
        previous_prime -= 1
    # Arithmetic mean
    mean = (previous_prime + next_prime) / 2
    # If n is a strong prime
    if (PrimeCandidate > mean):
        return True
    else:
        return False

# algo de rabin-miller de test de primalité
def rabinMiller(PrimeCandidate):
    #si pair, pas premier, les nombres trop petit causes des problemes
    if PrimeCandidate%2==0 or PrimeCandidate<10:
        return False

    s = 0
    r = PrimeCandidate - 1

    while r & 1 == 0: # tant que pair, divide pour resoudre n-1 = 2^s * r
        s += 1
        r //= 2

    for _ in range(RMCheck): # boucle pour atteindre le nombre d'itération de verification voulu
        a = randrange(2, PrimeCandidate - 1)
        x = pow(a, r, PrimeCandidate)
        if x != 1 and x != PrimeCandidate - 1:
            j = 1
            while j < s and x != PrimeCandidate - 1:
                x = pow(x, 2, PrimeCandidate)
                if x == 1:
                    return False
                j += 1
            if x != PrimeCandidate - 1:
                return False

    return True # si pas detecté non-prime, il est sans doute prime

#genere un grand nombre premier, les 0/1 sont choisi a l'aide de la fonction rand de python car je n'ai pas de Quantis TRNG sous la main
def createPrime():
    isPrime =False
    while isPrime==False:
        number = randbits(tailleP)
        number = (number & ~1) | 1 #passe le LSB a 1 pour eviter les nombres pair
        print("*",end="", flush=True)
        if rabinMiller(number) and strongPrime(number):
            isPrime=True

    print("prime found ",number) # print de debug
    return number #retourne le nombre premier


def bezout(p,q):
    if p==0:
        return (q,0,1)
    else:
        g,y,x=bezout(q%p,p)
        return (g,x-(q//p)*y,y)

def invmod(C,M): #inverse modulaire
    g,x,y=bezout(C,M)
    if g!=1:
        raise Exception('pas inversible')
    else:
        return x%M

# Genere un couple clé public/privé et les stocks dans deux fichier
def createPKI():
    P=createPrime()
    Q=createPrime()
    N=P*Q
    print('P '+str(P))
    print('Q '+str(Q))
    M=(P-1)*(Q-1) #indicateur euler
    print('M '+str(M))

    C=createPrime() #pas besoin d'etre prime, mais de cette facon si C ne divise pas M alors ils sont premier entre eux, et la fonction est déja la
    while M%C == 0:
        C=createPrime()
        print('pas premier entre eux') #print de debug

#public N,C
    publicKeyFile = open("publicKey", "w")
    publicKeyFile.write("N="+str(N)+"\n")
    publicKeyFile.write("C="+str(C))
    publicKeyFile.close()

# section creation clé privé U,N
    U=invmod(C,M)
    print('U '+str(U))
    privateKeyFile = open("privateKey", "w")
    privateKeyFile.write("U="+str(U)+"\n")
    privateKeyFile.write("N="+str(N))
    privateKeyFile.close()
