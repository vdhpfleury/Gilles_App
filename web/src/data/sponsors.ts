// Partenaires affichés sur l'accueil (src/components/Sponsors.astro), dans l'ordre d'importance
// voulu par Gilles. Logos : PNG ivoire sur fond transparent, recadrés au plus juste, dans
// src/assets/sponsors/. Pour retirer un partenaire, supprimer son entrée (et son logo) ; pour
// en ajouter un, déposer son logo et ajouter une entrée.

import type { ImageMetadata } from 'astro';
import ballWatch from '../assets/sponsors/ball-watch.png';
import beuchat from '../assets/sponsors/beuchat.png';
import sportProGroup from '../assets/sponsors/sport-pro-group.png';
import pureOcean from '../assets/sponsors/pure-ocean.png';

export interface Sponsor {
  nom: string;
  logo: ImageMetadata;
  /** Site officiel (ouvert dans un nouvel onglet). Sans URL, le logo n'est pas cliquable. */
  url?: string;
  /**
   * Correction optique de la taille (1 par défaut). Tous les logos ont déjà la même aire
   * apparente ; ce facteur compense en partie leur densité (lettrage fin ou aplats pleins) :
   * ≈ (densité moyenne / densité du logo)^0,2, puis vérifié à l'œil.
   */
  echelle?: number;
}

export const sponsors: Sponsor[] = [
  { nom: 'Ball Watch', logo: ballWatch, url: 'https://www.ballwatch.com/en/', echelle: 1.11 },
  { nom: 'Beuchat', logo: beuchat, url: 'https://www.beuchat-diving.com/fr/', echelle: 0.9 },
  { nom: 'Sport Pro Group', logo: sportProGroup, url: 'https://www.sportprogroup.fr/', echelle: 0.95 },
  { nom: 'Pure Ocean', logo: pureOcean, url: 'https://www.pure-ocean.org/', echelle: 1.05 },
];
