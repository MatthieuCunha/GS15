from makePKI import createPKI

# fonction qui fera office de retour au menu
def introduction():
    print('->1<- Générer des couples de clés publiques / privées. ')
    print('->2<- Générer un certificat.')
    print('->3<- Vérifier la validité d’un certificat. ')
    print('->4<- Partager une clé secrète. ')
    print('->5<- Chiffrer un message.')
    print('->6<- Signer un message.')
    print('->7<- Vérifier une signature. ')
    print('->8<- I WANT IT ALL !! I WANT IT NOW !!')
    choice = input ('Option :')
    print(choice)
    # pas de switch propre en python donc c'est parti pour l'empilement de if !
    if choice=='1':
        createPKI()
        print('KeyPair généré et placer dans 2 fichier')
    elif choice=='2':
        print('Création Certificat')
    elif choice=='3':
        print('Check certificat')
    elif choice=='4':
        print('Partage Clé secrete')
    elif choice=='5':
        print('Chiffrement message')
    elif choice=='6':
        print('Signature message')
    elif choice=='7':
        print('Création Verification Signature')
    elif choice=='8':
        print('tout ? maybe ?')
    else:
        # retour menu si choix incorrect
        print('Incorrect, nombre entre 1 et 8 requis ')
        introduction()






# lancement de l'introduction
introduction()
