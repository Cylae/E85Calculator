# Toyota Aygo 2014
## Comprendre et calculer le mélange E85 / SP98

Rapport technique préparé pour Alexandre

**35 litres nominalement. Deux crans restants. Aucun ratio sans voyant moteur démontré.**

Les calculs décrivent la composition d’un mélange sous des hypothèses explicites. Ils ne déterminent pas la tolérance de votre moteur.

Documentation, calculateur local, ébauche Android native et ébauche iOS native.

Vérifications documentaires : 4 octobre 2026
Version du projet : 0.1.0

<!-- pagebreak -->

# 01. Votre plein actuel : réponse concrète

Votre véhicule est décrit comme une Toyota Aygo essence de 2014, 69 ch, avec deux crans visibles sur six. Le rapport prend comme hypothèse un véhicule d’origine sans conversion E85 validée. Si un dispositif est installé, ses références et son homologation changent l’analyse.

> En l’absence de composition connue du carburant restant et de validation du véhicule à l’E85, le choix conservateur pour ce plein est : **0 litre d’E85 ajouté**, puis du **SP98 E5 jusqu’au premier arrêt automatique de la pompe**. Les 23,3 litres ci-dessous sont une estimation de scénario, pas une quantité à forcer dans le réservoir.

Toyota annonce un réservoir nominal de 35 L pour l’Aygo présentée en 2014. [S1]

Si l’on suppose, uniquement pour illustrer votre raisonnement, que chaque cran correspond au même volume :

```
Volume restant R = 35 × 2 / 6 = 35 / 3 L
R = 11,666666... L
Volume à compléter A = 35 × 4 / 6 = 70 / 3 L
A = 23,333333... L
```

La capacité nominale et le nombre de crans ne fournissent pas une calibration en litres. Ni la relation « 1 cran = 5,833 L », ni la correspondance entre 35 L et l’arrêt de votre pompe ne sont établies pour votre voiture. Inclinaison, seuils d’affichage et conditions de remplissage ne sont pas mesurés ici.

**Ajouter du SP98 réduit la teneur en éthanol si le carburant restant en contient davantage. Cela ne garantit ni l’absence de voyant, ni la disparition d’un défaut déjà présent.**

La quantité physique exacte ajoutée sera celle affichée par la pompe. Pour calculer exactement la nouvelle composition dans le modèle, il faut aussi connaître le volume et la composition du carburant restant.

<!-- pagebreak -->

# 02. Données vérifiées et inconnues

| Élément | État | Conséquence |
| --- | --- | --- |
| Aygo 2014, 69 ch | Déclaration utilisateur | Identification précise par VIN non fournie |
| Moteur 1.0 VVT-i, 998 cm³ | Fiche Toyota 2014 [S1] | Base documentaire cohérente avec le véhicule décrit |
| Réservoir 35 L | Capacité nominale Toyota [S1] | Ne mesure pas les litres restants |
| Compatibilité SP95-E10 | Aygo européenne 2014 couverte par la liste française [S2] | Référence vérifiée pour carburant normalisé |
| Conversion E85 | Non renseignée | Hypothèse de véhicule d’origine |
| Carburant restant | E85 et SP98 évoqués, proportions inconnues | Impossible d’attribuer une teneur précise |
| Éthanol réel de la pompe | Non mesuré | Utiliser une plage ou un certificat de lot |
| Limites de correction de l’ECU | Non mesurées | Aucun seuil personnalisé sans voyant établi |

La liste officielle française de juin 2026 vise les Toyota mises en circulation pour l’Europe depuis janvier 1998, avec des exceptions concernant certaines Avensis. L’Aygo 2014 européenne est donc couverte. Cela établit sa compatibilité avec le **carburant SP95-E10 conforme**, pas avec un mélange arbitraire ayant seulement la même teneur en éthanol. [S2]

Vous avez parlé de « Super Éthanol E95 » et de « E98 ». Dans le présent rapport, ces expressions sont interprétées comme **Superéthanol E85** et **Sans Plomb SP98 E5**, conformément au contexte de votre demande.

SP95 et SP98 indiquent un indice d’octane recherche. E5, E10 et E85 concernent la composition en alcools ; 98 ne signifie pas 98 % d’essence. Le SP98 E5 contient jusqu’à 5 % d’éthanol, sans garantir qu’il en contient exactement 5 %. [S3]

<!-- pagebreak -->

# 03. L’E85 change selon le lot et la saison

L’annexe II de l’arrêté français consolidé distingue les périodes suivantes. La grandeur réglementaire est la somme **éthanol + alcools supérieurs saturés**, en pourcentage volumique. [S4]

| Période | Dates | Minimum de cette somme | Maximum |
| --- | --- | --- | --- |
| Hiver | 1er novembre au 15 mars | 60 % | 85 % |
| Intersaisons | 16 mars au 30 avril ; 1er au 31 octobre | 60 % | 85 % |
| Été | 1er mai au 30 septembre | 70 % | 85 % |

**Le 4 octobre 2026 se situe en intersaison. Il est donc incorrect de supposer que l’E85 de votre station contient nécessairement 65 %, 75 % ou 85 % d’éthanol.** [S4]

Le ministère présente couramment l’E85 comme contenant de 60 à 85 % d’éthanol. [S3] Pour un calcul qui prétend distinguer l’éthanol pur, la nuance de l’annexe est utile : les alcools supérieurs peuvent représenter jusqu’à 6 % en volume. Une borne basse théorique de l’éthanol pur est donc 60 - 6 = 54 % en hiver/intersaison, et 70 - 6 = 64 % en été. Ce sont des bornes issues des spécifications, pas des mesures de votre lot. [S4]

Le calculateur utilise par défaut **54 à 85 % pour l’éthanol pur de la pompe E85**. Le plafond supérieur de 85 % est celui qui limite l’ajout dans le modèle. Les exemples à E60 ou E85 supposent, explicitement, ces teneurs d’éthanol pur.

L’arrêté réserve l’usage de l’E85 aux véhicules Flex-fuel et aux véhicules compatibles SP95-E10 équipés d’une conversion homologuée. [S4] Le calcul d’un pourcentage ne valide pas cette conversion et ne démontre pas qu’un mélange obtenu respecte toutes les spécifications de l’essence EN 228 : volatilité, oxygénés, distillation et matériaux ne sont pas représentés par une seule variable.

<!-- pagebreak -->

# 04. Pourquoi le voyant ne donne pas un seuil fiable

Une étude DOE / NREL / ORNL de 2009 a examiné 16 véhicules avec des mélanges jusqu’à E20. Elle ne rapporte pas de voyant attribué à la teneur en éthanol pendant cette phase limitée. Pourtant, 7 véhicules ont présenté un appauvrissement relatif à forte charge, contrairement aux 9 autres ; l’application des corrections apprises dépendait de la stratégie de gestion moteur. Voir pages PDF 37 et 41-43, sections 3.1.3 et 3.1.5. [S5]

**Déduction : l’absence de voyant ne suffit pas à établir que l’alimentation reste correcte dans toutes les conditions.** Cette étude, antérieure à votre Aygo 2014, ne valide ni E20, ni E30, ni E50 pour votre véhicule.

La correction court terme, STFT, et la correction long terme, LTFT, renseignent l’ajustement du dosage par l’ECU. Une correction positive peut être cohérente avec un besoin de carburant supplémentaire ; elle peut aussi avoir d’autres causes. Une mesure isolée au ralenti ne caractérise pas l’ensemble du fonctionnement.

Il manque, pour votre voiture, la référence de calibration, les valeurs de diagnostic, les conditions thermiques, les stratégies au démarrage et à forte charge, ainsi que les marges des injecteurs. **Aucun seuil universel de LTFT ou de teneur en éthanol n’est adopté dans ce rapport comme garantie anti-voyant.**

Le SP98 n’est pas un antidote à l’E85. Il dilue l’éthanol parce qu’il en contient beaucoup moins ; son indice d’octane plus élevé ne crée pas, à lui seul, une marge de débit d’injection.

Le but techniquement défendable consiste à vérifier la compatibilité et le dosage. Chercher uniquement la frontière d’apparition du voyant peut manquer un problème dans une autre zone de fonctionnement.

<!-- pagebreak -->

# 05. Le bilan volumique du mélange

Les fractions d’éthanol sont exprimées entre 0 et 1 : 30 % s’écrit 0,30. Les volumes sont exprimés en litres.

| Variable | Définition |
| --- | --- |
| R | Volume de carburant restant |
| er | Fraction d’éthanol du restant |
| X | Volume de carburant vendu comme E85 ajouté |
| ep | Fraction réelle d’éthanol de cet E85 |
| Y | Volume de SP98 ajouté |
| es | Fraction réelle d’éthanol du SP98 |
| C | Volume final retenu pour le calcul : R + X + Y |
| t | Fraction finale visée dans une simulation |

```
Volume d’éthanol = R × er + X × ep + Y × es
Fraction finale ef = (R × er + X × ep + Y × es) / C
Avec A = C - R et Y = A - X :
X = [C × t - R × er - A × es] / (ep - es)
Y = A - X
```

Cette formule résout une **composition**, pas une tolérance moteur. Elle suppose que les volumes sont additifs et comparables, que le mélange est homogène et que les fractions sont connues. Température et légère non-additivité réelle des mélanges ne sont pas modélisées : les chiffres sont exacts algébriquement sous hypothèses, pas une analyse de laboratoire.

Si X est négatif, même un appoint uniquement au SP98 reste au-dessus de la cible : **la cible est impossible par simple ajout à ce volume final**. Si X dépasse A, le restant empêche d’atteindre la cible, même en ajoutant uniquement l’E85 disponible. Si ep = es, les deux apports ont le même effet sur la teneur et cette division n’a pas de sens.

Pour un appoint déjà effectué, utilisez les litres réellement affichés aux deux pompes, sans supposer que C vaut nécessairement 35 L.

<!-- pagebreak -->

# 06. Exemple détaillé : deux crans sur six

**Exemple de calcul, pas recommandation d’utilisation : cible E30.** Hypothèses : C = 35 L ; R = 35/3 L ; restant exactement à 5 % ; E85 exactement à 85 % ; SP98 exactement à 5 %.

```
A = 35 - 35/3 = 70/3 L
X = [35 × 0,30 - (35/3) × 0,05 - (70/3) × 0,05]
    / (0,85 - 0,05)
X = 8,75 / 0,80 = 10,9375 L d’E85
Y = 70/3 - 10,9375 = 12,395833... L de SP98
```

Contrôle indépendant par conservation de l’éthanol :

```
Éthanol restant = (35/3) × 0,05 = 0,583333... L
Éthanol apporté par E85 = 10,9375 × 0,85 = 9,296875 L
Éthanol apporté par SP98 = 12,395833... × 0,05
                         = 0,619791666... L
Total = 10,5 L d’éthanol ; 10,5 / 35 = 0,30
```

| Arrondi dans la simulation | E85 | SP98 de complément | Teneur finale |
| --- | --- | --- | --- |
| Valeurs algébriques | 10,9375 L | 12,395833... L | 30,0000 % |
| E85 arrondi vers le bas au centilitre | 10,93 L | 12,403333... L | 29,9829 % |

L’E85 représente ici environ **46,87 % de l’appoint**, alors que le mélange final contient 30 % d’éthanol. Ces deux pourcentages désignent des choses différentes.

Les applications arrondissent X vers le bas au centilitre, puis calculent Y comme complément exact dans le modèle. Un affichage à deux décimales arrondit seulement la présentation de Y. Il faut conserver le volume final réel pour réévaluer un appoint effectivement effectué.

<!-- pagebreak -->

# 07. Comparaison des cibles hypothétiques

Toutes les lignes supposent C = 35 L, R = 35/3 L, restant et SP98 exactement à 5 %, E85 exactement à 85 %. Volumes affichés arrondis à deux décimales. **Aucune ligne ne constitue un seuil validé pour votre Aygo.**

| Cible | E85 à ajouter | SP98 à ajouter | E85 / appoint | Interprétation |
| --- | --- | --- | --- | --- |
| E10 | 2,19 L | 21,15 L | 9,37 % | Simulation seulement |
| E20 | 6,56 L | 16,77 L | 28,13 % | Simulation seulement |
| E30 | 10,94 L | 12,40 L | 46,88 % | Simulation seulement |
| E40 | 15,31 L | 8,02 L | 65,62 % | Simulation seulement |
| E50 | 19,69 L | 3,65 L | 84,38 % | Simulation seulement |
| E60 | Hors volume disponible | - | - | Maximum : E58,33 |

Le choix E10 sert de repère numérique correspondant à la limite d’éthanol du carburant normalisé compatible. Un mélange artisanal à 10 % n’est pas automatiquement équivalent à un SP95-E10 conforme. Les cibles supérieures sont des simulations explicatives, sans qualification du véhicule.

La composition de l’E85 de pompe change aussi la solution. Pour la même cible mathématique E30 et les mêmes volumes/restant/SP98 :

| Éthanol pompe supposé | E85 à ajouter | SP98 à ajouter | E85 / appoint |
| --- | --- | --- | --- |
| 60 % | 15,91 L | 7,42 L | 68,18 % |
| 70 % | 13,46 L | 9,87 L | 57,69 % |
| 75 % | 12,50 L | 10,83 L | 53,57 % |
| 85 % | 10,94 L | 12,40 L | 46,88 % |

Avec 10,9375 L d’E85 réellement à 60 %, et le complément utilisé dans l’exemple E85 à 85 %, le résultat serait **22,19 %**, au lieu de 30 %. La précision apparente des litres ne corrige donc pas une composition de pompe inconnue.

Ajouter « un léger soupçon » de SP98 à un gros volume d’E85 ne ramène pas le mélange à une faible teneur. Hors restant, 90 % d’E85 à 85 % + 10 % de SP98 à 5 % donnent 0,90 × 0,85 + 0,10 × 0,05 = **77 % d’éthanol**.

<!-- pagebreak -->

# 08. Le restant peut rendre la cible impossible

Hypothèses de ce tableau : C = 35 L, R = 35/3 L, E85 ajouté à 85 %, SP98 ajouté à 5 %. Chaque ligne suppose une composition différente du restant.

| Restant supposé | Après appoint 100 % SP98 | E85 pour viser E30 | SP98 pour viser E30 |
| --- | --- | --- | --- |
| E5 | 5,00 % | 10,94 L | 12,40 L |
| E10 | 6,67 % | 10,21 L | 13,12 L |
| E20 | 10,00 % | 8,75 L | 14,58 L |
| E30 | 13,33 % | 7,29 L | 16,04 L |
| E50 | 20,00 % | 4,38 L | 18,96 L |
| E70 | 26,67 % | 1,46 L | 21,88 L |
| E85 | 31,67 % | Impossible | Impossible |

> Avec un restant réellement à 85 %, compléter uniquement avec 23,333333... L de SP98 à 5 % donne encore **31,666666... % d’éthanol**. Une cible E30 ou E10 est alors impossible à atteindre en ajoutant du carburant jusqu’à 35 L.

```
ef = [(35/3) × 0,85 + (70/3) × 0,05] / 35
ef = 0,316666666...
```

Si les deux crans sont constitués d’un mélange inconnu d’E85 et de SP98, le restant peut être beaucoup plus chargé en éthanol que l’hypothèse E5 des exemples précédents. C’est la raison pour laquelle aucun « nombre exact de litres d’E85 à mettre maintenant » ne peut être justifié à partir des seuls crans.

Une dilution répétée peut se modéliser, sous hypothèses. Si un réservoir homogène est consommé jusqu’à la fraction q, puis complété avec un carburant de fraction es :

```
e(n+1) = q × e(n) + (1-q) × es
Après n cycles identiques : e(n) = es + q^n × [e(0)-es]
```

Exemple purement mathématique, q = 1/3, e(0) = 0,85 et es = 0,05 : les teneurs après les appoints seraient 31,67 %, 13,89 %, puis 7,96 %. Cette suite ne vous demande pas de continuer à rouler avec un fonctionnement irrégulier et ne décrit pas l’évolution d’un voyant.

<!-- pagebreak -->

# 09. Calculer avec une incertitude explicite

Pour un volume R connu dans le modèle et des compositions bornées, toutes les contributions sont positives. Les bornes du mélange s’obtiennent donc en combinant séparément les minima et les maxima.

```
ef_min = [R × er_min + X × ep_min + Y × es_min] / C
ef_max = [R × er_max + X × ep_max + Y × es_max] / C
```

Pour **maximiser mathématiquement X sous un plafond t**, on utilise les bornes hautes :

```
X_max = [C × t - R × er_max - (C-R) × es_max]
        / (ep_max - es_max)
```

Si la valeur est négative, le plafond ne peut pas être garanti pour toutes les compositions saisies. Le calculateur retourne « plafond non garanti » et aucun volume E85 ; il ne transforme pas ce résultat en une consigne de mélange.

Dans le scénario deux crans sur six, restant inconnu entre 0 et 85 %, SP98 entre 0 et 5 %, un appoint uniquement au SP98 donne une plage théorique **0 à 31,67 %**. Cette largeur rend impossible la garantie d’un plafond E10 dans ce scénario.

Le solveur limite X au volume disponible et l’arrondit vers le bas. Cette optimisation respecte **le plafond saisi sous les hypothèses du modèle** ; elle ne prouve pas que ce plafond est adapté au moteur.

Une incertitude sur le volume restant est distincte de celle sur sa composition. Si R est borné, le terme R × (er - es) est linéaire : il faut vérifier les deux extrémités de la plage de R, avec un X physiquement possible pour chacune. Les prototypes fournis demandent un seul R ; ils signalent son caractère estimé, sans inventer une plage issue des crans.

Lorsque l’éthanol est inconnu mais uniquement E85 et SP98 ont été utilisés, 0 à 85 % est une enveloppe conservatrice pour la fraction d’éthanol du restant. Ce choix n’est pas adapté à un réservoir contenant un autre produit.

<!-- pagebreak -->

# 10. Injection et énergie : ce que la physique explique

Pour illustrer le besoin de débit, les valeurs de référence d’Argonne sont utilisées : essence 0,741 kg/L et rapport air/carburant stœchiométrique 14,7 ; éthanol 0,790 kg/L et rapport 9,0. Les pouvoirs calorifiques inférieurs présentés sont 42,7 et 26,8 MJ/kg. Ces valeurs décrivent des combustibles de référence, pas votre lot de SP98 ou la calibration de l’Aygo. Voir diapositive 3, page PDF 3. [S6]

Pour une fraction volumique e et le même débit massique d’air, avec le modèle binaire essence/éthanol :

```
Air consommé par litre B(e) = (1-e) × 0,741 × 14,7
                             + e × 0,790 × 9,0
Débit volumique relatif à E5 = B(0,05) / B(e)
Énergie par litre H(e) = (1-e) × 0,741 × 42,7
                        + e × 0,790 × 26,8
```

| Mélange | B(e), kg air/L | Débit théorique vs E5 | H(e), MJ/L |
| --- | --- | --- | --- |
| E5 | 10,704 | 0,00 % | 31,12 |
| E10 | 10,514 | 1,80 % | 30,59 |
| E20 | 10,136 | 5,60 % | 29,55 |
| E30 | 9,758 | 9,69 % | 28,50 |
| E50 | 9,001 | 18,91 % | 26,41 |
| E85 | 7,677 | 39,42 % | 22,74 |

Les masses volumiques doivent intervenir dans le calcul : pondérer directement des rapports air/carburant massiques par des pourcentages volumiques serait une approximation différente.

Ce débit stœchiométrique n’est ni une prédiction de LTFT, ni une prévision de consommation routière. Le démarrage, la vaporisation, la richesse commandée, les autres oxygénés comme l’ETBE et le rendement réel restent hors du modèle.

<!-- pagebreak -->

# 10 bis. Débit théorique et énergie par litre

Ces graphiques utilisent exclusivement les hypothèses et équations de la page précédente. Les barres représentent les résultats du modèle ; elles ne représentent pas des mesures sur votre Aygo.

<!-- figure: injection.png -->

À teneur élevée en éthanol, le modèle demande un débit volumique supérieur pour conserver le même bilan stœchiométrique avec le même débit d’air. Pour E85, il donne environ **39,4 % de débit supplémentaire** par rapport à E5. La marge de vos injecteurs et la commande de l’ECU ne sont pas renseignées.

<!-- figure: energy.png -->

Le modèle donne 31,12 MJ/L à E5 et 22,74 MJ/L à E85. À rendement et énergie demandée identiques, le rapport H(E5) / H(E85) donnerait 36,8 % de volume supplémentaire. Cette hypothèse simplifiée ne constitue pas une prévision de consommation routière.

<!-- pagebreak -->

# 11. Informations nécessaires avant une validation moteur

Pour dépasser une simple simulation de composition, un diagnostic doit documenter le véhicule exact, son éventuelle conversion, l’état de son alimentation et le dosage dans les conditions concernées. Le rapport ne remplace pas cet examen.

| Information à relever | Utilité |
| --- | --- |
| VIN, moteur, référence ECU et calibration | Éviter une extrapolation à une autre Aygo |
| Dispositif E85 et homologation, s’il existe | Vérifier le domaine de fonctionnement prévu |
| Carburants, litres et kilomètres de chaque appoint | Reconstituer le restant dans un modèle homogène |
| Codes OBD enregistrés et en attente, données associées | Identifier le défaut avant de l’attribuer au carburant |
| STFT, LTFT, état boucle ouverte/fermée, température et charge | Contextualiser les corrections observées |
| Démarrage à froid, ratés, lambda et alimentation | Examiner les conditions que le ralenti ne couvre pas |

Conserver les codes et leurs données avant toute remise à zéro évite de perdre des éléments de diagnostic. Un fonctionnement irrégulier, une perte de puissance ou un voyant clignotant justifient d’interrompre l’essai et de faire examiner le véhicule. Il n’est pas nécessaire de provoquer un défaut pour connaître une composition.

Pour le suivi du mélange, noter le kilométrage et les litres des deux carburants à chaque plein. Si le réservoir est homogène, sa composition est supposée inchangée pendant la consommation ; son volume, lui, diminue. Cette hypothèse doit rester séparée d’une mesure réelle.

Pour comparer les coûts sans inventer les prix de votre station :

```
Coût de l’appoint = X × prix_E85 + Y × prix_SP98
Prix moyen des litres ajoutés = coût / (X+Y)
Coût pour 100 km = consommation réelle × prix moyen consommé
```

Le prix moyen de l’appoint ne décrit pas immédiatement le coût du carburant déjà présent. Une économie réelle dépend de la consommation mesurée et, le cas échéant, du coût de la conversion.

<!-- pagebreak -->

# 12. Les calculateurs fournis

| Livrable | Technologie | Usage |
| --- | --- | --- |
| Android | Kotlin et Jetpack Compose | Projet Android Studio, interface native |
| iOS | Swift et SwiftUI | Projet Xcode, interface native |
| Démonstration locale | HTML/CSS/JavaScript sans dépendance distante | Ouvrir web/index.html dans un navigateur |

Les applications mobiles utilisent des interfaces natives et leur propre moteur de calcul. La page HTML est un troisième calculateur autonome. Aucun des deux projets mobiles n’embarque une WebView pour remplacer son interface.

Fonctions présentes : volume final et volume restant, bornes de composition du restant et de l’E85, plafond numérique choisi, intervalle final, refus des cas impossibles, arrondi inférieur de l’E85, mémorisation locale et partage du résultat. Les hypothèses « 2 crans sur 6 » sont identifiées comme une estimation.

Le SP98 est borné entre 0 et 5 % dans les interfaces. Pour une simulation exacte à 5 %, le moteur accepte une plage réduite à ce seul point. Le réglage initial utilise un restant inconnu et un plafond de 10 %, de sorte qu’il montre l’incertitude au lieu de proposer arbitrairement un mélange riche en E85.

**Le plafond saisi n’est pas une propriété connue de l’Aygo.** Les prototypes ne proposent pas de seuil appris, de prédiction du voyant, ni de connexion OBD. La date documentaire et les liens restent visibles.

Ouvrir le projet android dans Android Studio avec JDK 17, SDK Android 36 et Gradle 8.13. Ouvrir ios/AygoBlend.xcodeproj dans Xcode pour un simulateur iOS 16 ou ultérieur. Les scripts de construction et les commandes précises sont décrits dans README.md.

Statut de cette remise : tests du moteur JavaScript exécutés ; tests Kotlin et XCTest fournis ; compilations mobiles à exécuter avec les SDK appropriés ou les workflows CI. Aucun APK ni IPA compilé n’est présenté comme disponible.

<!-- pagebreak -->

# 13. Vérification, maintenance et périmètre

Le moteur JavaScript est vérifié par 18 cas de référence, 9 cas de lecture des décimales et 10 000 simulations déterministes. Les contrôles examinent la conservation du volume, les huit coins des plages de composition, le respect du plafond et l’optimalité de X par une recherche numérique indépendante. Les cas invalides et les objectifs impossibles sont couverts.

Les projets Kotlin et Swift contiennent chacun 20 tests : les mêmes 18 cas de référence, la lecture des décimales et le refus des nombres non finis. Les workflows GitHub préparent la compilation Android, les tests iOS sur simulateur, le contrôle documentaire et une release conditionnée à la réussite des vérifications. Leur présence ne signifie pas qu’une exécution distante a déjà réussi.

Le PDF et le Markdown sont produits à partir du même contenu par tooling/build_report.py. Le contenu scientifique, les unités et les hypothèses doivent rester synchronisés avec les trois moteurs lors d’une évolution.

Les bornes réglementaires ne se mettent pas automatiquement à jour dans cette ébauche. Toute évolution nécessite une vérification de l’arrêté consolidé, une mise à jour documentée des valeurs et une nouvelle version. Une future source distante devrait conserver provenance, date de récupération et comportement hors ligne ; aucune API publique n’est supposée connaître la composition de votre lot de carburant.

**Ce qui reste indéterminé : le ratio maximal sans voyant pour votre voiture.** Ce résultat ne peut pas être déduit d’un bilan de litres. La documentation fournie distingue volontairement les compositions calculables des comportements moteur qui demandent une validation spécifique.

Le bilan peut être exact sous ses hypothèses, même lorsque ses données d’entrée sont incertaines. Les décimales supplémentaires ne transforment pas une estimation de jauge en mesure.

<!-- pagebreak -->

# 14. Sources vérifiées au 4 octobre 2026

**[S1] Toyota, présentation de l’Aygo du 4 mars 2014.** Fiche technique : 1.0 VVT-i, 998 cm³, réservoir nominal 35 L.

[Fiche technique Toyota 2014](https://media.toyota.co.uk/new-aygo-toyota-steps-fun-factor-new-city-car/)

**[S2] Ministère chargé de l’écologie, liste SP95-E10 de juin 2026.** Page PDF 5, rubrique TOYOTA : véhicules pour l’Europe depuis janvier 1998, exceptions Avensis.

[Liste officielle de compatibilité SP95-E10](https://www.ecologie.gouv.fr/sites/default/files/documents/Liste_v%C3%A9hicules_SP95-E10_Juin2026.pdf)

**[S3] Ministère chargé de l’écologie, Carburants et combustibles.** Définitions françaises SP95/SP98 E5, SP95-E10 et E85.

[Carburants et combustibles autorisés en France](https://www.ecologie.gouv.fr/politiques-publiques/carburants-combustibles-autorises-france)

**[S4] Légifrance, arrêté du 28 décembre 2006 relatif aux caractéristiques du superéthanol, version consolidée.** Article 3 : usages ; annexes I et II : alcools et saisons. Dernière mise à jour affichée : 1er février 2026 ; annexes modifiées le 18 avril 2025.

[Arrêté consolidé relatif au superéthanol](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000245613/)

**[S5] Knoll et al., DOE / NREL / ORNL, février 2009.** Effects of Intermediate Ethanol Blends on Legacy Vehicles and Small Non-Road Engines, Report 1 - Updated. Rapport NREL/TP-540-43543, ORNL/TM-2008/117. Pages PDF 37 et 41-43 (pagination interne 3-2 et 3-6 à 3-8).

[Étude expérimentale DOE / NREL / ORNL](https://www.energy.gov/sites/prod/files/2014/03/f14/pub_int_blends_rpt1_updated.pdf)

**[S6] Ickes et Wallner, Argonne National Laboratory, conférence DEER 2011.** Cold-Start Performance and Emissions Behavior of Alcohol Fuels in an SIDI Engine Using Transient Hardware-In-Loop Test Methods. Diapositive 3, page PDF 3 : propriétés de référence.

[Propriétés des carburants, Argonne / DOE](https://www.energy.gov/sites/default/files/2014/03/f8/deer11_ickes.pdf)

**[S7] Google et Apple, documentation des technologies natives.** Références de construction des prototypes ; aucune conclusion automobile n’en est tirée.

[Compatibilité Android Gradle Plugin 8.13](https://developer.android.com/build/releases/agp-8-13-0-release-notes)
[Documentation SwiftUI](https://developer.apple.com/documentation/swiftui)

Les études de 2009 et 2011 servent à expliquer des mécanismes physiques et des limites expérimentales. Elles ne sont pas présentées comme des essais sur votre Aygo 2014.
