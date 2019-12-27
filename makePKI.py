from random import getrandbits, randrange


# Genere un couple clé public/privé et les stocks dans deux fichier
tailleP = 256 #nomdre de bit pour generer les nombres premier
RMCheck = 128 #nombre de verification avec rabinMiller

# algo de rabin-miller de test de primalité
def rabinMiller(PrimeCandidate):
    #si pair, pas premier
    if PrimeCandidate%2==0:
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
        number = getrandbits(tailleP)
        number = (number & ~1) | 1 #passe le LSB a 1 pour eviter les nombres pair
        print("*",end="", flush=True)
        if rabinMiller(number):
            isPrime=True

    print("prime found ",number) # print de debug
    return number #retourne le nombre premier

#Genere le couple de clé
def createPKI():
    P=createPrime()
    Q=createPrime()
    N=P*Q
    M=P-1*Q-1 #indicateur euler

    C=createPrime() #pas besoin d'etre prime, mais de cette facon si C ne divise pas M alors ils sont premier entre eux
    while M%C==0
        C=createPrime()
        print('pas premier entre eux') #print de debug

#public N,C
publicKeyFile = open("publicKey", "w")
f.write("N=",N)
f.write("C=",C)
f.close()

createPKI()
