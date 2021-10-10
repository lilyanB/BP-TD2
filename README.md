# BP-TD2
Blockchain Programming

Pour bien appréhender nos recherches, nous allons décomposer en 2 parties. Une première partie avec un fichier très simple, qui va vous permettre d'interagir avec un programme basique. 
Le but du deuxième programme est de générer toutes les informations nécessaire pour la création d'un wallet. Nous avons insisté sur la partie pratique de ce programme. Vous ne devez en aucun cas modifier le programme pour qu'il puisse fonctionner, vous devez juste répondre aux questions via le terminal et le programme s'executera. 

Ce programme va fonctionner de cette manière : 

Vous devez dans un premier temps télécharger le fichier "TD02_Bitcoin_Today_practice.py" et le fichier "english.txt" puis exécuter le fichier "TD02_Bitcoin_Today_practice.py".

Une question va apparaitre.
Avez vous une seed ? Comprenez par seed d'une phrase mnémonique anglaise de 12 mots de chacun 11 bits. Si oui, vous pouvez répondre "y" à la question "Voulez vous importer votre propre seed ? (y/n)". Lorsque vous avez répondu, une autre question apparait "Entrez votre propre seed :", répondez par votre phrase. Si vous n'êtes pas concerné par cette option et que vous voulez générer un portefeuille aléatoire, répondez "n".

De nombreuses informations vont apparaitre à votre écran. Il s'agit des informations sur l'extension de vos clés privé et publique maitresse après une extension de la norme BIP32. Nous avons choisi de vous communiquer ces informations pour vous assurer de la validité des informations du portefeuille. 
Pour vérifier ces informations, rendez vous sur la page : https://iancoleman.io/bip39/ puis cliquez sur derivation path BIP32 et remplacez "m/0" dans le bip32 derivation path par "m/".

Après avoir récupéré nos adresses maitresse sous la norme BIP32, nous pouvons dérivé et indexé nos adresses maitresse BIP32. 
Vous devez choisir alors si vous voulez ou non dérivé vos adresses, si vous mettez "y", il faudra changer votre path sur le site : https://iancoleman.io/bip39/
par la dérivation de votre choix. 
Exemple: Si vous choississez de dérivé par 3, il faudra remplacer "m/0" dans le bip32 derivation path par "m/3".
Si vous ne voulez pas dériver vos futures adresses, écrivez "n".

Pour le choix de l'index et de la dérivation, il est important d'inscrire un int, comprenez un chiffre entier. 
Une fois cette étape terminée, vous pourrez vérifier les adresses BIP32 du code en les comparant avec le site précédemment évoqué. 

Nous vous laissons la liberté de récupérer les informations de votre portefeuille à la fin du programme par des questions. Répondez par "y" si vous voulez les récupérer ou "n" si ces informations ne vous intéressent pas. 

Merci pour votre confiance. 
