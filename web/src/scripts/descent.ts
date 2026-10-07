/*
 * « La descente » (page d'accueil uniquement) : faire défiler la page, c'est descendre.
 * - [data-descent] : calque d'eau fixe derrière le contenu (z-index -1). Il commence sous le
 *   hero (bord haut en fondu), puis couvre tout l'écran ; l'eau passe du bleu de surface à
 *   l'encre des abysses au fil du défilement.
 * - [data-descent-bubbles] : bulles CSS qui se raréfient avec la profondeur.
 * - [data-depth-gauge] : jauge 0 → 100 m (voir DepthGauge.astro).
 *
 * Un seul écouteur de défilement passif, regroupé par requestAnimationFrame. À chaque image on
 * ne lit que scrollY et on n'écrit que des propriétés composées (transform, opacity) sur
 * quelques éléments sans enfants : ni mise en page ni repeinture du calque. Les mesures
 * (hero, sections, hauteur du document) ne sont faites qu'au redimensionnement, dans un
 * ResizeObserver (mise en page déjà à jour à ce moment-là).
 * Sans JavaScript, rien de tout cela n'est affiché (cf. global.css) : la page reste sur l'encre.
 */

/** Hauteur (px) du fondu entre le bas du hero et l'eau ; reprise par global.css via --fade
 *  (et en dur, 15rem, dans les keyframes descent-rise). */
const FADE = 240;

/**
 * Opacité de l'eau bleue (#0c2f4a, cf. global.css) posée sur le fond encre (#0b0f14) : 1 en
 * surface, 0 au fond. La courbe garde l'eau bleue plus longtemps qu'un fondu linéaire
 * (≈ #0e2940 à 35 %, #0f1f31 à 65 %, #0c151f à 88 %). Le pire cas pour le contraste est donc
 * la surface : ivory 12,2:1, muted-1 7,6:1 (7,0:1 sur les cartes translucides).
 */
const waterOpacity = (p: number) => 1 - p ** 1.6;

/** Les bulles ont toutes disparu à 85 % de la descente. */
const BUBBLES_END = 0.85;

const clamp01 = (v: number) => Math.min(1, Math.max(0, v));

function init() {
  const layer = document.querySelector<HTMLElement>('[data-descent]');
  const hero = document.querySelector<HTMLElement>('[data-hero]');
  if (!layer || !hero) return;

  const water = layer.querySelector<HTMLElement>('[data-descent-water]');
  const glow = layer.querySelector<HTMLElement>('[data-descent-glow]');
  const bubbles = layer.querySelector<HTMLElement>('[data-descent-bubbles]');
  // Ordre d'extinction des bulles : celles de rang élevé disparaissent les premières.
  const bubbleEls = Array.from(bubbles?.children ?? []);
  const gauge = document.querySelector<HTMLElement>('[data-depth-gauge]');
  const track = gauge?.querySelector<HTMLElement>('[data-depth-indicator]');
  const value = gauge?.querySelector<HTMLElement>('[data-depth-value]');
  const bottomCap = gauge?.querySelector<HTMLElement>('[data-depth-cap]');
  const labels = Array.from(gauge?.querySelectorAll<HTMLElement>('[data-depth-label]') ?? [], (el) => ({
    el,
    section: document.querySelector<HTMLElement>(`[data-depth-section="${el.dataset.depthLabel}"]`),
    depth: 0,
    near: false,
    passed: false,
  }));

  layer.style.setProperty('--fade', `${FADE}px`);

  // Mesures (px, repère du document), mises à jour au redimensionnement seulement.
  let heroBottom = 0;
  let start = 0;
  let range = 1;
  let vh = window.innerHeight;

  // Dernières valeurs écrites, pour ne toucher au DOM que si quelque chose change.
  let lastShift = NaN;
  let lastP = NaN;
  let lastMeters = -1;
  let lastBubbles = -1;
  let lastActive: boolean | null = null;
  let lastCapNear: boolean | null = null;
  let lastState = '';

  function measure() {
    const y = window.scrollY;
    vh = window.innerHeight;
    heroBottom = hero!.getBoundingClientRect().bottom + y;
    // La descente commence quand le bas du hero remonte à 70 % de l'écran (l'eau occupe
    // alors le dernier tiers) et atteint 100 m tout en bas de la page.
    start = Math.max(0, heroBottom - vh * 0.7);
    range = Math.max(1, document.documentElement.scrollHeight - vh - start);

    for (const label of labels) {
      if (!label.section) continue;
      // Une section est « atteinte » quand son haut passe à 60 % de la hauteur de l'écran
      // (repère borné pour ne pas chevaucher les bornes Surface / 100 m de la jauge).
      const top = label.section.getBoundingClientRect().top + y;
      label.depth = Math.min(0.95, Math.max(0.03, (top - vh * 0.6 - start) / range));
      label.el.style.setProperty('--d', label.depth.toFixed(4));
    }
  }

  function update() {
    const y = window.scrollY;
    const p = clamp01((y - start) / range);

    // Le calque suit le bas du hero jusqu'à ce que le fondu soit sorti par le haut.
    const shift = Math.round(Math.max(-FADE, heroBottom - y));
    if (shift !== lastShift) {
      layer!.style.transform = `translate3d(0, ${shift}px, 0)`;
      lastShift = shift;
    }

    if (p !== lastP) {
      lastP = p;
      if (water) water.style.opacity = waterOpacity(p).toFixed(4);
      if (glow) glow.style.opacity = clamp01(1 - p * 2.5).toFixed(3);
      if (track) track.style.transform = `translate3d(0, ${(p * 100).toFixed(3)}%, 0)`;
    }

    const meters = Math.round(p * 100);
    if (value && meters !== lastMeters) {
      value.textContent = meters === 0 ? '0 m' : `−${meters} m`;
      lastMeters = meters;
    }

    for (const label of labels) {
      const near = Math.abs(p - label.depth) < 0.05;
      const passed = p >= label.depth;
      if (near !== label.near) label.el.classList.toggle('is-near', (label.near = near));
      if (passed !== label.passed) label.el.classList.toggle('is-passed', (label.passed = passed));
    }

    // « 100 m » s'efface quand la profondeur courante (« −100 m ») arrive à sa hauteur.
    const capNear = p > 0.94;
    if (bottomCap && capNear !== lastCapNear) {
      bottomCap.classList.toggle('is-near', capNear);
      lastCapNear = capNear;
    }

    // Densité : nombre de bulles encore visibles (les autres s'effacent en fondu, CSS).
    const visible = Math.ceil(bubbleEls.length * clamp01(1 - p / BUBBLES_END));
    if (visible !== lastBubbles) {
      bubbleEls.forEach((el, i) => el.toggleAttribute('data-gone', i >= visible));
      lastBubbles = visible;
    }

    // Bulles au repos (et masquées) tant que le hero occupe l'écran, à l'arrêt quand il n'en
    // reste plus, en mouvement entre les deux.
    const state = y < start ? 'rest' : visible === 0 ? 'still' : 'on';
    if (bubbles && state !== lastState) {
      bubbles.dataset.state = state;
      lastState = state;
    }

    // La jauge apparaît quand le hero est en bonne partie sorti de l'écran (le hero reste
    // tel quel) : le bas du hero est alors remonté au-dessus de 65 % de l'écran.
    const active = y > heroBottom - vh * 0.65;
    if (gauge && active !== lastActive) {
      gauge.classList.toggle('is-active', active);
      lastActive = active;
    }
  }

  let queued = false;
  const schedule = () => {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {
      queued = false;
      update();
    });
  };

  const refresh = () => {
    measure();
    lastShift = lastP = NaN; // forcer la réécriture avec les nouvelles mesures
    update();
    // Calque et jauge entrent dans le rendu une fois placés (fondu d'entrée en CSS).
    document.documentElement.classList.add('descent-ready');
  };

  // Appelé une première fois dès l'observation, puis à chaque changement de taille de la page.
  new ResizeObserver(refresh).observe(document.body);
  window.addEventListener('resize', () => requestAnimationFrame(refresh), { passive: true });
  window.addEventListener('scroll', schedule, { passive: true });
}

// Effet d'ambiance : il démarre une fois la page chargée et le fil principal libre, pour ne
// rien retirer au premier affichage ni à l'entrée du hero.
const start = () => {
  // Repli pour les navigateurs sans requestIdleCallback (Safari).
  if (typeof requestIdleCallback === 'function') requestIdleCallback(init, { timeout: 1500 });
  else setTimeout(init, 200);
};

if (document.readyState === 'complete') start();
else window.addEventListener('load', start, { once: true });
