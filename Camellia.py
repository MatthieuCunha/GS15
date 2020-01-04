# coding=utf-8

keySize=128 # nombre de bit attendu pour la clé
k=0 # key used by camellia

KA=0
KB=0

MASK8   = 0xff
MASK32  = 0xffffffff
MASK64  = 0xffffffffffffffff
MASK128 = 0xffffffffffffffffffffffffffffffff

Sigma1 = bin(0xA09E667F3BCC908B)
Sigma2 = bin(0xB67AE8584CAA73B2)
Sigma3 = bin(0xC6EF372FE94F82BE)
Sigma4 = bin(0x54FF53A5F1D36F1C)
Sigma5 = bin(0x10E527FADE682D1D)
Sigma6 = bin(0xB05688C2B3E6C1FD)

# adapte la taille la cle échanger avec diffie hellman, par decoupe ou padding selong les parametres
def resizeKey(fullK):
	global k

	print('taille actuel '+str(fullK.bit_length())+' bits')
	if(fullK.bit_length()>keySize):
		## extraction des keySize premier bit
		binary = bin(fullK)
		binary = binary[2:]
		end = len(binary) - 1
		start = end - keySize + 1
		kBitSubStr = binary[start : end+1]
		k=int(kBitSubStr,2) # repasse de base 2 en integer
		print('taille final  '+str(k.bit_length())+' bits')
	#elif(K.bit_length()<keySize):
		#padding

def rotateLeft(num, bits):
	bit = num & (1 << (bits-1))
	num <<= 1
	if(bit):
		num |= 1
	num &= (2**bits-1)

	return num

def xor(s1, s2):
	if(isinstance(s2,int)):
		s2=bin(s2)
	if(isinstance(s1,int)):
		s1=bin(s1)
	return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

# string to binary
def stobin(s):
    return ''.join('{:08b}'.format(ord(c)) for c in s)


# binary to int
def bintoint(s):
    return int(s, 2)


# int to binary
def itobin(i):
    return bin(i)


# binary to string
def bintostr(b):
    n = int(b, 2)
    return ''.join(chr(int(b[i: i + 8], 2)) for i in xrange(0, len(b), 8))

# substitu la tValue par le resultat correspondant a la sbox, a faire plus tard si j'y pense
def SBOX(boxNumber,tValue):
	return tValue

# fonction F de la doc, sans doute util a quelque chose
def F(F_IN, KE):
	 x= xor(F_IN, KE)
	 t1 =  x >> 56
	 t2 = (x >> 48) & MASK8
	 t3 = (x >> 40) & MASK8
	 t4 = (x >> 32) & MASK8
	 t5 = (x >> 24) & MASK8
	 t6 = (x >> 16) & MASK8
	 t7 = (x >>  8) & MASK8
	 t8 =  x        & MASK8
	 # la doc utilise un tableau, mais apparement on doit changer pour un calcul dans Gf2^8, donc fonction a faire
	 t1 = SBOX(1,t1)
	 t2 = SBOX(2,t2)
	 t3 = SBOX(3,t3)
	 t4 = SBOX(4,t4)
	 t5 = SBOX(2,t5)
	 t6 = SBOX(3,t6)
	 t7 = SBOX(4,t7)
	 t8 = SBOX(1,t8)

	 y1 = t1 ^ t3 ^ t4 ^ t6 ^ t7 ^ t8
	 y2 = t1 ^ t2 ^ t4 ^ t5 ^ t7 ^ t8
	 y3 = t1 ^ t2 ^ t3 ^ t5 ^ t6 ^ t8
	 y4 = t2 ^ t3 ^ t4 ^ t5 ^ t6 ^ t7
	 y5 = t1 ^ t2 ^ t6 ^ t7 ^ t8
	 y6 = t2 ^ t3 ^ t5 ^ t7 ^ t8
	 y7 = t3 ^ t4 ^ t5 ^ t6 ^ t8
	 y8 = t1 ^ t4 ^ t5 ^ t6 ^ t7
	 F_OUT = (y1 << 56) | (y2 << 48) | (y3 << 40) | (y4 << 32) | (y5 << 24) | (y6 << 16) | (y7 <<  8) | y8
	 return F_OUT


#FL-function takes two parameters.  One is 64-bit input data FL_IN.   The other is 64-bit subkey KE.  FL-function returns 64-bit data FL_OUT.
def FL(FL_IN,KE):
	 x1 = FL_IN >> 32
	 x2 = FL_IN & MASK32
	 k1 = KE >> 32
	 k2 = KE & MASK32
	 x2 = x2 ^ rotateLeft(x1 & k1,1)
	 x1 = x1 ^ (x2 | k2)
	 FL_OUT = (x1 << 32) | x2
	 return FL_OUT

def FLINV(FLINV_IN, KE):

	y1 = FLINV_IN >> 32
	y2 = FLINV_IN & MASK32
	k1 = KE >> 32
	k2 = KE & MASK32
	y1 = y1 ^ (y2 | k2)
	y2 = y2 ^ rotateLeft(y1 & k1,1)
	#rotated=y1 & k1
	#rotated = rotated[1:] + [rotated[0]]
	#y2 = y2 ^ rotated
	FLINV_OUT = (y1 << 32) | y2
	return FLINV_OUT


def camelliaEncrypt():
  KL=k
  KR= 0x00000000000000000000000000000000 # valeur 0
  global KA
  global KB

# génération des clés a partir de la clé de base
  D1 = (KL ^ KR) >> 64
  D2 = (KL ^ KR) & MASK64
  D2 = D2 ^ F(D1, Sigma1)
  D1 = D1 ^ F(D2, Sigma2)
  D1 = D1 ^ (KL >> 64)
  D2 = D2 ^ (KL & MASK64)
  D2 = D2 ^ F(D1, Sigma3)
  D1 = D1 ^ F(D2, Sigma4)
  KA = (D1 << 64) | D2
  D1 = (KA ^ KR) >> 64
  D2 = (KA ^ KR) & MASK64
  D2 = D2 ^ F(D1, Sigma5)
  D1 = D1 ^ F(D2, Sigma6)
  KB = (D1 << 64) | D2

  kw1 =bin( KL  >> 64)
  kw2 =bin( KL  & MASK64)
  k1  =bin( KA  >> 64)
  k2  =bin( KA  & MASK64)
  k3  =bin( rotateLeft(KL ,  15) >> 64)
  k4  =bin( rotateLeft(KL ,  15) & MASK64)
  k5  =bin( rotateLeft(KA ,  15) >> 64)
  k6  =bin( rotateLeft(KA ,  15) & MASK64)
  ke1 =bin( rotateLeft(KA ,  30) >> 64)
  ke2 =bin( rotateLeft(KA ,  30) & MASK64)
  k7  =bin( rotateLeft(KL ,  45) >> 64)
  k8  =bin( rotateLeft(KL ,  45) & MASK64)
  k9  =bin( rotateLeft(KA ,  45) >> 64)
  k10 =bin( rotateLeft(KL ,  60) & MASK64)
  k11 =bin( rotateLeft(KA ,  60) >> 64)
  k12 =bin( rotateLeft(KA ,  60) & MASK64)
  ke3 =bin( rotateLeft(KL ,  77) >> 64)
  ke4 =bin( rotateLeft(KL ,  77) & MASK64)
  k13 =bin( rotateLeft(KL ,  94) >> 64)
  k14 =bin( rotateLeft(KL ,  94) & MASK64)
  k15 =bin( rotateLeft(KA ,  94) >> 64)
  k16 =bin( rotateLeft(KA ,  94) & MASK64)
  k17 =bin( rotateLeft(KL , 111) >> 64)
  k18 =bin( rotateLeft(KL , 111) & MASK64)
  kw3 =bin( rotateLeft(KA , 111) >> 64)
  kw4 =bin( rotateLeft(KA , 111) & MASK64)

  open('EncryptedTexte', 'w').close() # delete le contenu du message
  #lire le message et extraire des bloc de 128bit en boucle
  texteFile = open("baseTexte.txt", "r")
  texte=texteFile.read(16)
  while texte:
  #découpe en 2 bloc de 64bit gauche et droite
	   D1, D2 = texte[:int(len(texte)/2)], texte[int(len(texte)/2):]

	   # tourné de feistel
	   D1 = xor(D1, kw1)          # Prewhitening
	   D2 = xor(D2, kw2)
	   D2 = D2 ^ F(D1, k1)     # Round 1
	   D1 = D1 ^ F(D2, k2)     # Round 2
	   D2 = D2 ^ F(D1, k3)     # Round 3
	   D1 = D1 ^ F(D2, k4)     # Round 4
	   D2 = D2 ^ F(D1, k5)     # Round 5
	   D1 = D1 ^ F(D2, k6)     # Round 6
	   D1 = FL   (D1, ke1)     # FL
	   D2 = FLINV(D2, ke2)     # FLINV
	   D2 = D2 ^ F(D1, k7)     # Round 7
	   D1 = D1 ^ F(D2, k8)     # Round 8
	   D2 = D2 ^ F(D1, k9)     # Round 9
	   D1 = D1 ^ F(D2, k10)    # Round 10
	   D2 = D2 ^ F(D1, k11)    # Round 11
	   D1 = D1 ^ F(D2, k12)    # Round 12
	   D1 = FL   (D1, ke3)     # FL
	   D2 = FLINV(D2, ke4)     # FLINV
	   D2 = D2 ^ F(D1, k13)    # Round 13
	   D1 = D1 ^ F(D2, k14)    # Round 14
	   D2 = D2 ^ F(D1, k15)    # Round 15
	   D1 = D1 ^ F(D2, k16)    # Round 16
	   D2 = D2 ^ F(D1, k17)    # Round 17
	   D1 = D1 ^ F(D2, k18)    # Round 18
	   D2 = D2 ^ kw3           # Postwhitening
	   D1 = D1 ^ kw4

	   C = (D2 << 64) | D1
	   f = open("EncryptedTexte", "a")
	   f.write(str(C))

		  #lecture du prochain morceau
	   texte=texteFile.read(16)
	   if(len(texte)<16 and texte!=''): # padding si le dernier fait moins de 16 octets
		   missing=16-len(texte)
		   texte+= ' '*missing

def switch(var1,var2):
	return var2,var1

def camelliaDecrypt():
	  KL=k
	  KR= MASK128 & MASK128 # valeur 0
	  global KA
	  global KB

	# regeneration des cle car les variables globale c'est chiant a faire
	  D1 = (KL ^ KR) >> 64
	  D2 = (KL ^ KR) & MASK64
	  D2 = D2 ^ F(D1, Sigma1)
	  D1 = D1 ^ F(D2, Sigma2)
	  D1 = D1 ^ (KL >> 64)
	  D2 = D2 ^ (KL & MASK64)
	  D2 = D2 ^ F(D1, Sigma3)
	  D1 = D1 ^ F(D2, Sigma4)
	  KA = (D1 << 64) | D2
	  D1 = (KA ^ KR) >> 64
	  D2 = (KA ^ KR) & MASK64
	  D2 = D2 ^ F(D1, Sigma5)
	  D1 = D1 ^ F(D2, Sigma6)
	  KB = (D1 << 64) | D2

	  kw1 = KL  >> 64
	  kw2 = KL  & MASK64
	  k1  = KA  >> 64
	  k2  = KA  & MASK64
	  k3  = rotateLeft(KL ,  15) >> 64
	  k4  = rotateLeft(KL ,  15) & MASK64
	  k5  = rotateLeft(KA ,  15) >> 64
	  k6  = rotateLeft(KA ,  15) & MASK64
	  ke1 = rotateLeft(KA ,  30) >> 64
	  ke2 = rotateLeft(KA ,  30) & MASK64
	  k7  = rotateLeft(KL ,  45) >> 64
	  k8  = rotateLeft(KL ,  45) & MASK64
	  k9  = rotateLeft(KA ,  45) >> 64
	  k10 = rotateLeft(KL ,  60) & MASK64
	  k11 = rotateLeft(KA ,  60) >> 64
	  k12 = rotateLeft(KA ,  60) & MASK64
	  ke3 = rotateLeft(KL ,  77) >> 64
	  ke4 = rotateLeft(KL ,  77) & MASK64
	  k13 = rotateLeft(KL ,  94) >> 64
	  k14 = rotateLeft(KL ,  94) & MASK64
	  k15 = rotateLeft(KA ,  94) >> 64
	  k16 = rotateLeft(KA ,  94) & MASK64
	  k17 = rotateLeft(KL , 111) >> 64
	  k18 = rotateLeft(KL , 111) & MASK64
	  kw3 = rotateLeft(KA , 111) >> 64
	  kw4 = rotateLeft(KA , 111) & MASK64

	  kw1 , kw3 =switch(kw1 , kw3)
	  kw2 , kw4 =switch(kw2 , kw4)
	  k1  , k18 =switch(k1  , k18)
	  k2  , k17  =switch(k2  , k17)
	  k3  , k16  =switch(k3  , k16)
	  k4  , k15  =switch(k4  , k15)
	  k5  , k14  =switch(k5  , k14)
	  k6  , k13  =switch(k6  , k13)
	  k7  , k12  =switch(k7  , k12)
	  k8  , k11  =switch(k8  , k11)
	  k9  , k10  =switch(k9  , k10)
	  ke1 , ke4  =switch(ke1 , ke4)
	  ke2 , ke3  =switch(ke2 , ke3)

	  open('DecryptedTexte', 'w').close() # delete le contenu du message
	  texteFile = open("EncryptedTexte", "r")
	  texte=texteFile.read(16)
	  while texte:
	#découpe en 2 bloc de 64bit gauche et droite
	   D1, D2 = texte[:int(len(texte)/2)], texte[int(len(texte)/2):]

	   D1 = ''.join(format(ord(i), 'b') for i in D1)
	   D1 = int(D1,2)
	   D2 = ''.join(format(ord(i), 'b') for i in D2)
	   D2 = int(D2,2)

	   # tourné de feistel
	   D1 = D1 ^ kw1          # Prewhitening
	   D2 = D2 ^ kw2
	   D2 = D2 ^ F(D1, k1)     # Round 1
	   D1 = D1 ^ F(D2, k2)     # Round 2
	   D2 = D2 ^ F(D1, k3)     # Round 3
	   D1 = D1 ^ F(D2, k4)     # Round 4
	   D2 = D2 ^ F(D1, k5)     # Round 5
	   D1 = D1 ^ F(D2, k6)     # Round 6
	   D1 = FL   (D1, ke1)     # FL
	   D2 = FLINV(D2, ke2)     # FLINV
	   D2 = D2 ^ F(D1, k7)     # Round 7
	   D1 = D1 ^ F(D2, k8)     # Round 8
	   D2 = D2 ^ F(D1, k9)     # Round 9
	   D1 = D1 ^ F(D2, k10)    # Round 10
	   D2 = D2 ^ F(D1, k11)    # Round 11
	   D1 = D1 ^ F(D2, k12)    # Round 12
	   D1 = FL   (D1, ke3)     # FL
	   D2 = FLINV(D2, ke4)     # FLINV
	   D2 = D2 ^ F(D1, k13)    # Round 13
	   D1 = D1 ^ F(D2, k14)    # Round 14
	   D2 = D2 ^ F(D1, k15)    # Round 15
	   D1 = D1 ^ F(D2, k16)    # Round 16
	   D2 = D2 ^ F(D1, k17)    # Round 17
	   D1 = D1 ^ F(D2, k18)    # Round 18
	   D2 = D2 ^ kw3           # Postwhitening
	   D1 = D1 ^ kw4

	   C = (D2 << 64) | D1
	   f = open("DecryptedTexte", "a")
	   f.write(str(C))
	   texte=texteFile.read(16)


def camellia():
	f = open("SecretKey", "r")
	fullK = int(f.read())
	resizeKey(fullK)
	print('la clé redimensionné est '+str(k)) ## print de debug

	#camelliaEncrypt()
	#print('Choix du mode 1)ECD 2)CBC 3)PCBC')
	#choice = int(input ('Option :'))



camellia()
#camelliaDecrypt()
