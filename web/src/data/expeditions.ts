// Liste provisoire, limitée aux lieux déjà cités sur le site (coordonnées approximatives du
// centre de chaque région) : à compléter avec Gilles (lieux réels, dates, missions ESA).

export type ExpeditionType = 'expedition' | 'stage' | 'mission' | 'recherche';

export interface Expedition {
  lieu: string;
  region: string;
  lat: number;
  lng: number;
  periode: string;
  titre: string;
  description: string;
  type: ExpeditionType;
  aConfirmer: boolean;
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
    periode: '[À compléter]',
    titre: 'Fjords glacés du Groenland',
    description:
      "Plongées et missions dans les fjords glacés du Groenland, entre rigueur scientifique et exploration humaine. Le Groenland est aussi l'une des destinations des stages d'apnée sous glace.",
    type: 'expedition',
    aConfirmer: true,
  },
  {
    lieu: "Nice, Côte d'Azur",
    region: 'Méditerranée',
    lat: 43.7,
    lng: 7.27,
    periode: '[À compléter]',
    titre: 'Récifs méditerranéens',
    description:
      "Plongée scientifique et protocoles d'étude marine sur la Côte d'Azur : échantillonnage, observation in situ, cartographie sous-marine et suivi écologique des récifs méditerranéens.",
    type: 'recherche',
    aConfirmer: true,
  },
  {
    lieu: 'Caraïbes',
    region: 'Mer des Caraïbes',
    lat: 15,
    lng: -73,
    periode: '[À compléter]',
    titre: 'Abysses caribéens',
    description:
      "Des récifs méditerranéens aux abysses caribéens : plongées animées par la même passion — découvrir, préserver, faire connaître et aimer l'océan.",
    type: 'expedition',
    aConfirmer: true,
  },
  {
    lieu: 'Alpes françaises',
    region: 'Alpes',
    lat: 45.5,
    lng: 6.5,
    periode: '[À compléter]',
    titre: 'Apnée sous glace — Alpes françaises',
    description:
      'Stage sur mesure : le silence absolu, la lumière du froid, la maîtrise du souffle. Respiration, concentration et gestion du froid en environnement extrême.',
    type: 'stage',
    aConfirmer: true,
  },
  {
    lieu: 'Suisse',
    region: 'Alpes',
    lat: 46.8,
    lng: 8.2,
    periode: '[À compléter]',
    titre: 'Apnée sous glace — Suisse',
    description:
      "Stage sur mesure : découvrir et pratiquer l'apnée sous glace en toute sécurité, avec la logistique et les techniques spécifiques à ce milieu.",
    type: 'stage',
    aConfirmer: true,
  },
  {
    lieu: 'Norvège',
    region: 'Scandinavie',
    lat: 64.5,
    lng: 12,
    periode: '[À compléter]',
    titre: 'Apnée sous glace — Norvège',
    description:
      "Stage sur mesure : sous la glace, chaque mouvement devient une méditation, chaque respiration une connexion profonde entre le corps, l'eau et la lumière.",
    type: 'stage',
    aConfirmer: true,
  },
  {
    lieu: 'Finlande',
    region: 'Scandinavie',
    lat: 63.5,
    lng: 26,
    periode: '[À compléter]',
    titre: 'Apnée sous glace — Finlande',
    description:
      'Stage sur mesure : développer la maîtrise mentale et physique en environnement extrême.',
    type: 'stage',
    aConfirmer: true,
  },
];
