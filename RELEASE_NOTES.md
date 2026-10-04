# Aygo Blend 0.1.0 - Préversion

Première ébauche fonctionnelle de calcul de composition E85 / SP98 pour documenter le cas d’une Toyota Aygo 2014.

- Rapport français en Markdown et PDF : sources primaires, formule, calculs détaillés, incertitudes et limites de l’objectif « sans voyant moteur ».
- Android natif en Kotlin / Jetpack Compose et iOS natif en Swift / SwiftUI, avec projets de construction et tests du moteur.
- Calculateur HTML autonome, utilisable hors ligne.
- 18 cas de référence ; 10 000 simulations déterministes et vérifications des interfaces web en CI.
- Construction Android et tests iOS requis avant publication automatique des artefacts.

Cette version calcule une composition sous hypothèses. Aucun ratio maximal sans voyant moteur n’est validé pour l’Aygo. L’absence de voyant n’atteste pas, à elle seule, la compatibilité du carburant.

L’APK joint par la CI est une construction de développement. L’archive iOS concerne le simulateur et ne contient pas d’IPA signé pour iPhone. Ces artefacts ne sont disponibles que si les jobs correspondants réussissent.
