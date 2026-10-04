# E85Calculator · Aygo Blend

[![CI](https://github.com/Cylae/E85Calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/Cylae/E85Calculator/actions/workflows/ci.yml)

Calculateur de composition E85 / SP98, rapport technique pour une Toyota Aygo 2014 et ébauches **natives Android et iOS**.

**Aucun ratio maximal sans voyant moteur n’est établi pour une Aygo non convertie.** Ce projet calcule des mélanges sous hypothèses. Il ne détermine pas la tolérance d’un moteur et ne remplace pas une validation de conversion ou un diagnostic.

Le réservoir nominal de l’Aygo 2014 est de 35 L. Le scénario « deux crans sur six » est une approximation explicative de 11,67 L restants. Il ne constitue pas une mesure de jauge.

| Contenu | Emplacement |
| --- | --- |
| Rapport français, calculs, limites et sources | [Markdown](reports/Rapport_Toyota_Aygo_E85_SP98.md) et [PDF](reports/Rapport_Toyota_Aygo_E85_SP98.pdf) |
| Calculateur autonome et hors ligne | [web/index.html](web/index.html) |
| Android : Kotlin + Jetpack Compose | [android/](android/) |
| iOS : Swift + SwiftUI | [ios/AygoBlend.xcodeproj](ios/AygoBlend.xcodeproj) |
| Moteur de référence et tests numériques | [verification/](verification/) |
| Génération documentaire et contrôles | [tooling/](tooling/) |
| Compilation, tests et release | [.github/workflows/ci.yml](.github/workflows/ci.yml) |

## Modèle

```text
ef = (R × er + X × ep + Y × es) / C
C = R + X + Y
X = [C × t - R × er - (C-R) × es] / (ep - es)
```

Les volumes sont en litres et les fractions entre 0 et 1. `X` désigne les litres de carburant commercialisé comme E85, et non des litres d’éthanol pur. Le solveur utilise les bornes hautes pour maximiser `X` sous un plafond choisi. Il refuse de produire un volume E85 si même un appoint uniquement au SP98 ne peut garantir ce plafond dans le modèle. `X` est arrondi vers le bas au centilitre.

Par défaut : volume final simulé 35 L, restant estimé 11,67 L, teneur du restant inconnue de 0 à 85 %, SP98 de 0 à 5 %, E85 de 54 à 85 %, plafond 10 %. Le chiffre 54 % est une borne théorique prudente pour l’éthanol pur : la réglementation française borne la somme éthanol + alcools supérieurs, lesquels peuvent atteindre 6 %. Le lot réel demande une mesure ou une documentation de composition.

Un plafond de 10 % dans ce calcul n’atteste pas que le mélange respecte toutes les spécifications du SP95-E10 normalisé. Les applications n’établissent pas de seuil anti-voyant, ne commandent pas l’ECU et n’effacent aucun défaut.

## Utilisation immédiate de la démonstration

Ouvrir `web/index.html` dans un navigateur. Le fichier contient son moteur, son interface et ses styles ; aucune installation et aucune requête distante ne sont nécessaires au calcul. La mémorisation des hypothèses est locale et explicite. Les liens des sources s’ouvrent uniquement à la demande.

## Android

Prérequis : Android Studio compatible AGP 8.13, JDK 17, SDK Android 36 et Gradle 8.13. Ouvrir le dossier `android/` en projet Gradle. Le projet utilise AGP 8.13.2, Kotlin 2.2.20 et Compose BOM 2025.09.00 ; Android 8.0 / API 26 minimum.

Un wrapper binaire Gradle n’est pas embarqué. La CI installe la version de Gradle spécifiée. Avec Gradle 8.13 disponible localement :

```bash
gradle -p android testDebugUnitTest assembleDebug
```

L’APK de développement résultant est `android/app/build/outputs/apk/debug/app-debug.apk`. L’application ne demande aucune permission réseau. Les champs sont mémorisés localement lorsque l’utilisateur choisit de les enregistrer.

## iOS

Ouvrir `ios/AygoBlend.xcodeproj` dans Xcode et sélectionner un simulateur iPhone ou iPad. Le projet inclut un schéma partagé `AygoBlend` et une cible XCTest. Cible minimum iOS 16 ; aucune dépendance externe.

```bash
python3 tooling/test_ios.py
```

Le script choisit un simulateur iPhone disponible, puis lance `xcodebuild test` avec la signature désactivée pour le simulateur. Pour un iPhone physique, une équipe de signature Apple et une construction pour appareil sont nécessaires. Une archive de simulateur n’est pas un IPA installable.

## Vérification et génération

```bash
node verification/test_blend.cjs
python3 -m pip install -r requirements.txt
python3 tooling/create_projects.py
python3 tooling/build_report.py
python3 tooling/build_html.py
python3 tooling/verify_artifacts.py
```

Les 18 cas numériques sont utilisés dans le moteur JavaScript et comme fixtures de test Kotlin/XCTest. Le test JavaScript effectue aussi 10 000 simulations déterministes avec conservation des volumes, contrôle des bornes et recherche indépendante du maximum. Chaque suite mobile comporte 20 tests.

Les tests de navigateur utilisent Playwright. Avec Node.js et npm :

```bash
npm install
npx playwright install chromium
node verification/test_web.cjs
```

La CI exécute ces vérifications, construit l’APK de développement et teste l’application iOS sur simulateur. Un échec de compilation ou de test bloque la publication automatique de release.

**État de la remise 0.1.0 :** le moteur JavaScript et l’identité du moteur embarqué dans le HTML sont vérifiés dans l’environnement de création. Le PDF est contrôlé visuellement. Les tests mobiles et de navigateur sont fournis ; cet environnement ne dispose pas des SDK Android et Apple ni d’un navigateur exécutable, donc leur réussite ne peut pas être affirmée sans une exécution native ou de CI.

## Publication GitHub

Le dépôt du projet est [Cylae/E85Calculator](https://github.com/Cylae/E85Calculator), avec la description :

> Calculateur E85/SP98 pour Toyota Aygo : rapport sourcé, simulations avec incertitudes et prototypes natifs Kotlin/Compose et Swift/SwiftUI.

Pour créer une copie dans un autre nouveau dépôt, le script `tooling/publish_github.py` utilise l’identité GitHub réellement authentifiée. Il crée un **nouveau dépôt privé par défaut**, configure la description et les sujets, pousse `main`, puis le tag `v0.1.0`. Il évite de modifier un dépôt préexistant portant ce nom. `--public` permet une publication publique explicite.

```bash
python3 tooling/publish_github.py
```

Prérequis de cette commande : Git et GitHub CLI (`gh`) installés, compte déjà authentifié, fichiers revus et commit local sur `main`. La création du dépôt nécessite une capacité GitHub de création de repositories ; le seul accès aux fichiers d’un dépôt existant ne suffit pas.

## Release

Un tag `v*` déclenche les mêmes contrôles que les changements de code. Après réussite de tous les jobs, le job release publie une **préversion** avec le rapport PDF, le Markdown, la page HTML, les sources, l’APK de développement et une application pour simulateur iOS. Les notes proviennent de `RELEASE_NOTES.md`.

Le workflow peut également être lancé depuis l’onglet Actions avec le champ `release_version` égal à `v0.1.0`. Dans ce mode, il crée le tag et la préversion sur le commit vérifié après réussite de tous les jobs. Laisser ce champ vide exécute uniquement les vérifications.

Pour la première publication depuis une intégration qui peut pousser des commits mais ne peut pas créer de tag, un commit sur `main` dont le message complet est exactement `Release v0.1.0` déclenche aussi la préversion `v0.1.0`. Les trois jobs de vérification doivent réussir avant sa création.

La présence de ces workflows ne signifie pas qu’un dépôt ou une release ont déjà été publiés. Seuls les résultats GitHub constatés attestent la publication et les constructions.

## Sources et maintenance

Les sources primaires, leurs dates et les passages pertinents figurent dans le rapport. Les bornes sont vérifiées au 4 octobre 2026 et ne s’actualisent pas automatiquement. Chaque modification documentaire doit être accompagnée d’une mise à jour des hypothèses et des cas de test concernés.

Licence MIT. Documentation et calculs produits pour ce projet ; aucune affiliation à Toyota.
