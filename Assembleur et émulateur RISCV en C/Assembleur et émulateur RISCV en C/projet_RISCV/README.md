# Projet RISC-V CS351

Auteurs : Hugo ASTIC et Nicolas MAGNE

## Rendu 1

* Cochez (en remplaçant `[ ]` par `[x]`) si vous avez :
  - [x] Vérifié que `make test` se plaint sur le nombre d'instructions et pas
      sur l'existence des fichiers de sortie.
  - [x] Vu sur Chamilo que les soumissions se font avec `make tar`.


## Rendu 2

(Une dizaine de lignes devrait suffire à chaque fois)

* Comment avez-vous choisi de programmer l'analyse de texte (dont la lecture
des opérandes entières) ? Comment identifiez-vous les noms de registres, des noms "jolis", des entiers ?

[Pour l'analyse de texte, nous lisons ligne par ligne, en utilisant un getline, les différentes lignes de code. Ensuite, pour chaque ligne, nous lisons mots par mots, en utilisant un strtok, la ligne en utilisant le fait que entre chaque mot il y a un espace ( après avoir enlevé les virgules). Ensuite, en fonction de la position du mot on peut différencier les opcodes des opérandes et registres: si c'est la premier mot on sait que c'est forcément un opcode. Pour le reste, on a des tableaux contenant tous les registres possibles. On parcourt donc ces tableaux pour savoir si le mot que l'on est en train de traiter correspond à un des registres de notre tableaux. Si c'est le cas, c'est un registre est on va stocker la valeur décimale correspondant à ce registre dans un tableau de char. Sinon, nous reconnaissons que c'est une valeur immédiate en regardant la première valeur de notre chaine de caractère que l'on est en train de traiter( si c'est un chiffre en 0 et 9  ou un signe négatif alors c'est une valeur immédiate. Pour traiter les registres, nous avons pris en compte les deux cas possibles, soit c'est un nom de registre jolis, soit c'est une nom de registre de la forme "xi". Pour cela nous avons deux tableaux de registres.]

* Avez-vous vu des motifs récurrents émerger ? Avez-vous "factorisé" ces motifs
pour éviter de les répéter ? Si non, serait-ce difficile ?

[Nous n'avons pas remarqué d'éventuels motifs récurrents. Par contre nous avons stocké les opcodes et les funct3 et 7 dans une structure pour éviter de les redéterminer à chaque fois. Ainsi, nous parcourons notre structure et pour un opcode donné, on récupère l'opcode en binaire, le funct3, le funct7, et le type d'instruction. Avec ce type d'instruction, on peut ainsi construire l'instruction final selon la documentation RiscV, grâce à notre fonction "instruction_séquence" qui construit, en focntion d'un opcode, des registres et valeur immédiates, l'instruction finale. On aurait aussi pu éviter de faire deux tableaux de registres et n'en faire qu'un avec les noms "jolis" des registres ( a1,a2,...) car le deuxième tableaux n'est que la concaténation des caractères x et d'un nombre entre 0 et 31.]

* Comment avez-vous procédé pour écrire les tests ? Êtes-vous confiant·e·s que
toutes les instructions gérées et tous les types d'arguments sont couverts ?

[Les test ont été réalisé avec make test et make puis ./riscv-assembler ./tests/add-simple.s ./tests/add-simple.hex. Nous avons, pour les tests, écrits toutes les instructions possibles pour notre programme, en prenant aussi en compte les valeurs immédiates négatives et les instructions particulières demandées par le programme. Nos tests prennent aussi en compte les deux types de registres possibles compréhensible par l'assembleur. En fin de projet, nous avons aussi créé plusieurs petits fichiers test.s contenant chacun un programme assembleur avec les valeurs des registres que l'on devrait obtenir à la fin de l'éxécution du programme. Ces fichiers seront aussi utiles pour la partie émulateur. Nous sommes assez confiants de nos tests qui couvrent toutes les instructions possibles selon la documentation RISC-V fournie. Nous avons aussi décidé de faire des tests à la main pour voir ce que notre programme nous retournait si les fichiers en entrées ou en sorties étaient mal renseignés ou si il y avait un problème avec l'opcode. Nous avons procédé à ces quelques tests car nous avons programmé des lignes de codes C pour reconnaître ces types d'erreur et exit du programme si c'est le cas.]

* Quelle a été votre expérience avec l'utilisation et la compréhension de la
documentation fournie sur l'encodage des instructions RISC-V ?

[La documentation RISCV était complète, compréhensible et claire. Cependant, nous avions cru à un moment que la partie sur les int64_t était aussi pour la partie sur l'assembleur or ce n'était pas le cas. Il aurait peut-être fallu rajouter cette précision...Mais pour ce qui était de la compréhension, la construction des différents types d'instruction, avec la construction et séparation des valeurs immédiates, était assez claires.]

* Cochez (en remplaçant `[ ]` par `[x]`) si vous avez :
  - [x] Implémenté la traduction pour toutes les instructions de la documentation
  - [x] Pris en compte les cas particuliers comme les valeurs immédiates négatives et le bit manquant dans l'encodage de `jal`
  - [x (un peu)] Écrit du code de gestion d'erreur pour que le programme ait une réaction propre si le code assembleur est invalide _(pas demandé par le sujet)_


## Rendu 3

Questions à remplir _avant_ de programmer l'émulateur (10 lignes sont conseillées à chaque fois pour bien y réfléchir) :

* Listez tous les éléments matériels auxquels vous pouvez penser dont l'émulateur doit reproduire le comportement, et déduisez-en une liste de toutes les tâches individuelles de l'émulateur.

[-créer une liste contenant nos registres et leur valeurs initiales. ]
[-lire nos instructions hex ]
[-utilisation d'un tableau d'entiers pour gérer la lecture et écriture de nos instructions sachant qu'une instruction est codée sur 4 octets et que notre mémoire est de 16384 octets donc [il nous faut donc au maximum 4096 cases mémoires pour stocker nos instructions]
[-on crée un PC pour parcourir notre tableau et faire des jumps que l'on stocke dans le typedef des registres]
[- lecture des instructions selon notre valeur de PC]
[- à chaque lecture on regarde si il faut modifier notre PC pour le prochain saut ( ex: si on a beg, j, jal,...)]

* Quelle fonction de la bibliothèque standard pouvez-vous utiliser pour lire les valeurs listées dans le fichier `.hex` sans vous casser la tête ? (Indice : ces valeurs ont été écrites avec `fprintf()`.)

[On peut utiliser la fonction fscanf() avec le format "%08x" pour la lecture des valeurs hexadécimales en entiers.]

* Décrivez comment vous allez répartir les tâches de l'émulateur en différents fichiers, ou ne pas les répartir et tout faire dans le même fichier. Expliquez les avantages de votre choix.

[On part sur le fait de ne pas répartir les taches en plusieurs fichiers .c et de tout faire dans le même fichier. Cela va être plus simple pour nous pour modifier notre programme, Cela va être assez intéressant aussi pour gérer la mémoire.]



Questions à remplir _après_ avoir programmé l'émulateur :

* Aviez-vous réussi à listé toutes les tâches dans la première question ? Rétrospectivement, y a-t-il des tâches dont vous aviez sous-estimé ou sur-estimé la complexité ?

[Oui, nous avons réussi à faire la liste de tache de la question 1.Cependant, nous avons sous-estimé la faisabilité et le fonctionnement du ld/sd et le décodage des instructions avec les valeurs immédiates négatives.]

* Avez-vous compris le fonctionnement de chaque instruction à partir de la
documentation fournie ? Si non, quels sont les points obscurs ?

[Toute les instructions étaient claires et précises dans la documentation]

* Quels exemples de programmes avez-vous choisi pour tester le calcul ? Les
comparaisons et sauts ? La mémoire ?

[Nous avons créé 11 fichiers tests différents ( et 5 autres qui sont des retours de bugs de la part de Mr.Michelland) permettant de tester toutes les instructions demandées avec des valeurs immédiates positives et négatives. Nous avons aussi crée des programme avec des boucles et des programmes simulant l'appel de fonction en utilisant la pile ]

* Reste-t-il des bugs que vous avez découverts et pas corrigés ?

[Pas de bugs à signaler sur le code en lui même et l'émulation de programmes assembleurs. Cependant, nous avons remarqué avec Valgrind qu'une valeur n'était pas initialisée lors du strcmp() dans notre fonction execute_instruction().]

* D'autres remarques sur votre programme ?

[Pas de remarques supplémentaires à signaler ]

* Cochez (en remplaçant `[ ]` par `[x]`) si vous avez :**
  - [x] Implémenté l'émulation de toutes les instructions gérées par le rendu 2.
  - [x] Implémenté l'émulation de toutes les instructions.
  - [x] Tous vos tests qui passent.
  - [x] Vérifié que vous tests couvrent toutes les instructions émulées.
  - [x] Testé les cas particuliers : valeurs négatives, overflows...
  - [x] Testé les cas d'erreur : division par zéro, sauts invalides... _(pas demandé par le sujet)_
  - [euh..] Un port fonctionnel de DOOM pour votre émulateur.

* Des retours sur le projet en général ?

[Projet assez intéressant tant au niveau programmation C que programmation RISCV. Cela a permis de reprendre tout ce que nous avons fait en C (tableaux, typedef, manipulation bit, ...) mais aussi de mieux comprendre la programmation assembleur en RISCV. Ce projet nous a aussi permis de mieux comprendre les fonctionnalités de décalage de bit, masques de bits et utilisation des structures en C comparable à des dictionnaires en Python.]
