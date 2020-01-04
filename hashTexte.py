# coding=utf-8

import hashlib






# hash le texte
#a remplacer si j'ai la motiviation par une version manuel
def hashTexte(texte):
    s=hashlib.sha3_224(texte).hexdigest()
    return s
