/*
 * Lieux du globe des expéditions (section en fin de page « Qui suis-je », composant
 * ExpeditionsGlobe.astro). Chaque entrée donne un bouton de la liste, un marqueur sur le globe
 * et une fiche ; l'ordre du tableau est celui de la liste (numérotée 01, 02…).
 *
 * Ajouter une expédition = ajouter un objet au tableau `expeditions` ci-dessous :
 * - lieu        nom court, affiché dans la liste et en étiquette sur le globe (ex. « Groenland ») ;
 * - region      zone plus large, affichée dans la fiche après le lieu (ex. « Arctique ») ;
 * - lat, lng    coordonnées en degrés décimaux, nord et est positifs, sud et ouest négatifs
 *               (ex. Nice : lat 43.7, lng 7.27 ; Caraïbes : lat 15, lng -73) — un clic droit sur
 *               un point dans Google Maps affiche ces deux nombres ;
 * - periode     facultatif, texte libre (« Hiver 2024 », « 2019-2021 »…) : la ligne « Période »
 *               de la fiche n'apparaît que si ce champ est renseigné ;
 * - titre       titre de la fiche ;
 * - description une ou deux phrases ;
 * - type        'expedition', 'stage', 'mission' ou 'recherche' : libellé affiché dans la liste
 *               et la fiche (voir `typeLabels`, à compléter avec `ExpeditionType` pour un
 *               nouveau type).
 *
 * Les lieux actuels sont ceux déjà cités sur le site, avec les coordonnées approximatives du
 * centre de chaque région.
 */

export type ExpeditionType = 'expedition' | 'stage' | 'mission' | 'recherche';

export interface Expedition {
  lieu: string;
  region: string;
  /** Latitude en degrés décimaux (nord positif, sud négatif). */
  lat: number;
  /** Longitude en degrés décimaux (est positif, ouest négatif). */
  lng: number;
  /** Facultatif : la ligne « Période » n'est affichée que si elle est renseignée. */
  periode?: string;
  titre: string;
  description: string;
  type: ExpeditionType;
}

export const typeLabels: Record<ExpeditionType, string> = {
  expedition: 'Expédition',
  stage: 'Stage',
  mission: 'Mission',
  recherche: 'Recherche',
};

export const expeditions: Expedition[] = [
  {
    lieu: 'Groenland',
    region: 'Arctique',
    lat: 70,
    lng: -40,
    titre: 'Fjords glacés du Groenland',
    description:
      "Plongées et missions dans les fjords glacés du Groenland, entre rigueur scientifique et exploration humaine. Le Groenland est aussi l'une des destinations des stages d'apnée sous glace.",
    type: 'expedition',
  },
  {
    lieu: "Nice, Côte d'Azur",
    region: 'Méditerranée',
    lat: 43.7,
    lng: 7.27,
    titre: 'Récifs méditerranéens',
    description:
      "Plongée scientifique et protocoles d'étude marine sur la Côte d'Azur : échantillonnage, observation in situ, cartographie sous-marine et suivi écologique des récifs méditerranéens.",
    type: 'recherche',
  },
  {
    lieu: 'Caraïbes',
    region: 'Mer des Caraïbes',
    lat: 15,
    lng: -73,
    titre: 'Abysses caribéens',
    description:
      "Des récifs méditerranéens aux abysses caribéens : plongées animées par la même passion — découvrir, préserver, faire connaître et aimer l'océan.",
    type: 'expedition',
  },
  {
    lieu: 'Alpes françaises',
    region: 'Alpes',
    lat: 45.5,
    lng: 6.5,
    titre: 'Apnée sous glace — Alpes françaises',
    description:
      'Stage sur mesure : le silence absolu, la lumière du froid, la maîtrise du souffle. Respiration, concentration et gestion du froid en environnement extrême.',
    type: 'stage',
  },
  {
    lieu: 'Suisse',
    region: 'Alpes',
    lat: 46.8,
    lng: 8.2,
    titre: 'Apnée sous glace — Suisse',
    description:
      "Stage sur mesure : découvrir et pratiquer l'apnée sous glace en toute sécurité, avec la logistique et les techniques spécifiques à ce milieu.",
    type: 'stage',
  },
  {
    lieu: 'Norvège',
    region: 'Scandinavie',
    lat: 64.5,
    lng: 12,
    titre: 'Apnée sous glace — Norvège',
    description:
      "Stage sur mesure : sous la glace, chaque mouvement devient une méditation, chaque respiration une connexion profonde entre le corps, l'eau et la lumière.",
    type: 'stage',
  },
  {
    lieu: 'Finlande',
    region: 'Scandinavie',
    lat: 63.5,
    lng: 26,
    titre: 'Apnée sous glace — Finlande',
    description:
      'Stage sur mesure : développer la maîtrise mentale et physique en environnement extrême.',
    type: 'stage',
  },
];
