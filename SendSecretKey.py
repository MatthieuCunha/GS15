#les fonctions dans ce fichier simuleront les différents actions lors de l'échanger de clé avec l'algo diffie-hellman
from secrets import randbits, randbelow
from makePKI import createPrime
from fastExpo import pow_mod

p = 0 # represente ce que la personne 1 memorise entre les etapes
a = 0 # represente ce que la personne 1 memorise entre les etapes

def retourPersonne1(B):
    k=pow_mod(B,a,p)
    print('personne 1 trouve k '+str(k))
    publicKeyFile = open("Secretkey", "w")
    publicKeyFile.write(str(k))

def addSecondLock(p,g,A): #genere secret personne 2 et envoi retourne g^b
    b=randbelow(p-1) #secret personne 2
    B=pow_mod(g,b,p)
    k=pow_mod(A,b,p)
    print('personne 2 trouve k '+str(k))
    retourPersonne1(B) #retour du B calculé par le second participant au premier

#creation des elemnts de l'échange et ajout du premier lock
def createSecret():
    Key = randbits(KeySize)
    global p
    p=createPrime() #prime du groupe
    g=randbelow(p-1) #generateur
    global a
    a=randbelow(p-1) #secret personne 1
    A=pow_mod(g,a,p)
    print('A '+str(A))

    addSecondLock(p,g,A) # phase d'envoi du nombre premier,generateur et A du premier participant au second participant
