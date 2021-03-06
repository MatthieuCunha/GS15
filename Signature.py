# coding=utf-8

#code récupéré sur github car je comprends rien a l'algo de toute facon.

from random import randrange
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime
from hashlib import sha1
from hashTexte import hashTexte

N = 160
L = 1024

#generation des parametres et des nombres premier du code github, pas de la fonction makePKI, car celle ci semble bien plus rapide
def generate_p_q(L, N):
    g = N  # g >= 160
    n = (L - 1) // g
    b = (L - 1) % g
    while True:
        # generate q
        while True:
            s = xmpz(randrange(1, 2 ** (g)))
            a = hashTexte(to_binary(s))
            zz = xmpz((s + 1) % (2 ** g))
            z = hashTexte(to_binary(zz))
            U = int(a, 16) ^ int(z, 16)
            mask = 2 ** (N - 1) + 1
            q = U | mask
            if is_prime(q, 20):
                break
        # generate p
        i = 0  # counter
        j = 2  # offset
        while i < 4096:
            V = []
            for k in range(n + 1):
                arg = xmpz((s + j + k) % (2 ** g))
                zzv = hashTexte(to_binary(arg))
                V.append(int(zzv, 16))
            W = 0
            for qq in range(0, n):
                W += V[qq] * 2 ** (160 * qq)
            W += (V[n] % 2 ** b) * 2 ** (160 * n)
            X = W + 2 ** (L - 1)
            c = X % (2 * q)
            p = X - c + 1  # p = X - (c - 1)
            if p >= 2 ** (L - 1):
                if is_prime(p, 10):
                    return p, q
            i += 1
            j += n + 1


def generate_g(p, q):
    while True:
        h = randrange(2, p - 1)
        exp = xmpz((p - 1) // q)
        g = powmod(h, exp, p)
        if g > 1:
            break
    return g


def generate_keys(g, p, q):
    x = randrange(2, q)  # x < q
    certificat = open("certificateurPrivateKey", "w")
    certificat.write(str(x))
    y = powmod(g, x, p)
    certificat = open("certificateurPublicKey", "w")
    certificat.write(str(y)+'\n')
    return x, y


def generate_params(L, N):
    p, q = generate_p_q(L, N)
    g = generate_g(p, q)
    return p, q, g


def sign(M, p, q, g, x):
    if not validate_params(p, q, g):
        raise Exception("Invalid params")
    while True:
        k = randrange(2, q)  # k < q
        r = powmod(g, k, p) % q
        m = int(hashTexte(M), 16)
        try:
            s = (invert(k, q) * (m + x * r)) % q
            return r, s
        except ZeroDivisionError:
            pass


def verify(M, r, s, p, q, g, y):
    p=xmpz(p)
    q=xmpz(q)
    g=xmpz(g)
    r=xmpz(r)
    y=xmpz(y)
    if not validate_params(p, q, g):
        raise Exception("Invalid params")
    if not validate_sign(r, s, q):
        return False
    try:
        w = invert(xmpz(s), xmpz(q))
    except ZeroDivisionError:
        return False
    m = int(hashTexte(M), 16)
    u1 = (m * w) % q
    u2 = (r * w) % q
    # v = ((g ** u1 * y ** u2) % p) % q
    v = (powmod(g, u1, p) * powmod(y, u2, p)) % p % q
    if v == r:
        return True
    return False


def validate_params(p, q, g):
    if is_prime(p) and is_prime(q):
        return True
    if powmod(g, q, p) == 1 and g > 1 and (p - 1) % q:
        return True
    return False


def validate_sign(r, s, q):
    if int(r) < 0 and int(r) > int(q):
        return False
    if int(s) < 0 and int(s) > int(q):
        return False
    return True


p, q, g = generate_params(L, N) # sont des parametres de l'algo et donc librement partagé
x, y = generate_keys(g, p, q)


def signerMessage(texte):
    r, s = sign(texte.encode(), p, q, g, x)
    print('r= '+str(r))
    print('s= '+str(s))
    signature = open("signature", "w")
    signature.write(str(r) + "\n")
    signature.write(str(s))
    return r, s

def verifierSignature(texte):
    signature = open("signature", "r")
    r=int(signature.readline())
    s=int(signature.readline())
    conforme=verify(texte.encode(),r,s,p,q,g,y)
    if(conforme):
        print('signature valide')
    else:
        print('signature invalide')


def signerCle(publicKey):
    r, s = sign(publicKey.encode(), p, q, g, x)
    certificat = open("Certificat", "w")
    certificat.write(str(y)+'\n')
    certificat.write(str(p) + '\n')
    certificat.write(str(q) + '\n')
    certificat.write(str(g) + '\n')
    certificat.write(str(r) + "\n")
    certificat.write(str(s)+'\n')
