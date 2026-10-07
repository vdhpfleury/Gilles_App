import type { Globe, Marker } from 'cobe';

/*
 * Globe des expéditions (composant ExpeditionsGlobe.astro), piloté par attributs data-* :
 * - [data-globe]             racine de la section
 * - [data-globe-stage]       conteneur carré du globe (canvas + halos)
 * - [data-globe-canvas]      canvas WebGL rendu par cobe (aria-hidden : la liste porte l'info)
 * - [data-globe-halo]        halo HTML de chaque lieu, positionné au-dessus du marqueur
 * - [data-globe-item]        boutons de la liste (data-lat, data-lng)
 * - [data-globe-detail]      fiches détaillées, une par lieu
 * Boutons, halos et fiches sont associés par leur ordre dans le DOM (même ordre de rendu).
 * - [data-globe-placeholder] invitation affichée tant que rien n'est sélectionné
 *
 * La liste fonctionne seule (sans WebGL, ou avant le chargement du globe). Le globe n'est
 * chargé (import dynamique de cobe) qu'à l'approche de la section, ne tourne que lorsqu'elle
 * est à l'écran et l'onglet actif, et est détruit au pagehide.
 */

type RGB = [number, number, number];

// Charte "Abysse" en composantes 0–1 (cobe attend du RGB linéaire 0–1).
const IVORY: RGB = [0.957, 0.945, 0.918]; // #f4f1ea
const LAGON: RGB = [0.31, 0.541, 0.553]; // #4f8a8d
const LAGON_LIGHT: RGB = [0.62, 0.86, 0.86];
const GLOW: RGB = [0.1, 0.2, 0.22];

const RADIUS = 0.8; // rayon du globe dans le repère de cobe (clip space, canvas carré)
const MARKER_ELEVATION = 0.01; // marqueurs posés sur la sphère (0,05 par défaut dans cobe : ils flottent au-delà du limbe)
const REST_THETA = 0.28; // légère inclinaison : tous les lieux sont dans l'hémisphère nord
const MAX_THETA = 0.7;
const AUTO_SPEED = 0.12; // rad/s — un tour en ~50 s
const TAU = Math.PI * 2;

const clamp = (v: number, min: number, max: number) => Math.min(max, Math.max(min, v));
/** Écart angulaire le plus court de `from` vers `to`, dans ]-π, π]. */
const shortest = (from: number, to: number) => {
  const d = (((to - from) % TAU) + TAU) % TAU;
  return d > Math.PI ? d - TAU : d;
};

/** Angles (phi, theta) de cobe qui amènent un lieu au centre du globe. */
const anglesFor = (lat: number, lng: number) => ({
  phi: (3 * Math.PI) / 2 - (lng * Math.PI) / 180,
  theta: clamp((lat * Math.PI) / 180, -MAX_THETA, MAX_THETA),
});

/** Position 3D d'un lieu sur la sphère, avec la même convention que cobe. */
function toVector(lat: number, lng: number): [number, number, number] {
  const la = (lat * Math.PI) / 180;
  const lo = (lng * Math.PI) / 180 - Math.PI;
  const c = Math.cos(la);
  return [-c * Math.cos(lo), Math.sin(la), c * Math.sin(lo)];
}

/** Projection d'un point (même calcul que le vertex shader des marqueurs de cobe). */
function project(v: [number, number, number], phi: number, theta: number) {
  const r = RADIUS + MARKER_ELEVATION;
  const [ax, ay, az] = [v[0] * r, v[1] * r, v[2] * r];
  const cp = Math.cos(phi);
  const sp = Math.sin(phi);
  const ct = Math.cos(theta);
  const st = Math.sin(theta);
  return {
    x: cp * ax + sp * az,
    y: sp * st * ax + ct * ay - cp * st * az,
    z: -sp * ct * ax + st * ay + cp * ct * az,
  };
}

function hasWebGL() {
  try {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
    if (!gl) return false;
    gl.getExtension('WEBGL_lose_context')?.loseContext();
    return true;
  } catch {
    return false;
  }
}

interface Place {
  lat: number;
  lng: number;
  vector: [number, number, number];
  button: HTMLButtonElement;
  detail: HTMLElement | null;
  halo: HTMLElement | null;
}

export function initExpeditionsGlobe(root: HTMLElement) {
  const stage = root.querySelector<HTMLElement>('[data-globe-stage]');
  const canvas = root.querySelector<HTMLCanvasElement>('[data-globe-canvas]');
  const placeholder = root.querySelector<HTMLElement>('[data-globe-placeholder]');
  const halos = root.querySelectorAll<HTMLElement>('[data-globe-halo]');
  const details = root.querySelectorAll<HTMLElement>('[data-globe-detail]');

  const places: Place[] = Array.from(root.querySelectorAll<HTMLButtonElement>('[data-globe-item]')).map(
    (button, i) => {
      const lat = Number(button.dataset.lat);
      const lng = Number(button.dataset.lng);
      return { lat, lng, vector: toVector(lat, lng), button, detail: details[i] ?? null, halo: halos[i] ?? null };
    },
  );
  if (!places.length) return;

  const reduceQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  let reduceMotion = reduceQuery.matches;

  // --- État de rotation ------------------------------------------------------------------
  let phi = anglesFor(places[0].lat, places[0].lng).phi - 0.9; // l'Atlantique nord de face
  let theta = REST_THETA;
  let phiVelocity = 0; // inertie après un glisser (rad/s)
  let autoFactor = 1; // 0 → 1 : reprise progressive de la rotation automatique
  let target: { phi: number; theta: number } | null = null;
  let holding = false; // un lieu sélectionné est tenu de face jusqu'au prochain glisser
  let selected = -1;
  let dragging = false;

  // --- État du rendu (déclaré avant select() : sans WebGL, la fonction s'arrête plus bas) ---
  let globe: Globe | null = null;
  let loading = false;
  let inView = false;
  let size = 0;
  let rafId = 0;
  let lastTime = 0;

  // --- Sélection (fonctionne aussi sans globe) --------------------------------------------
  function select(index: number) {
    const place = places[index];
    if (!place) return;

    if (index !== selected) {
      selected = index;
      places.forEach((p, i) => {
        const active = i === index;
        p.button.setAttribute('aria-pressed', String(active));
        p.detail?.toggleAttribute('data-active', active);
        p.halo?.toggleAttribute('data-active', active);
      });
      if (placeholder) placeholder.hidden = true;
      updateMarkers();
    }

    target = anglesFor(place.lat, place.lng);
    phiVelocity = 0;
    if (reduceMotion) {
      // Pas d'animation : le globe saute directement sur le lieu.
      phi = target.phi;
      theta = target.theta;
      target = null;
      holding = true;
    }
    requestFrame();
  }

  // Sélection au clic, à Entrée ou Espace (le « click » natif d'un <button>), jamais au simple
  // focus : parcourir la liste au clavier ne change pas la sélection.
  places.forEach((place, i) => {
    place.button.addEventListener('click', () => select(i));
  });

  // --- Globe (chargé à la demande) ---------------------------------------------------------
  if (!stage || !canvas) return;
  if (!hasWebGL()) {
    root.dataset.globeState = 'unsupported';
    return;
  }

  const markers = (): Marker[] =>
    places.map((p, i) =>
      i === selected
        ? { location: [p.lat, p.lng], size: 0.06, color: LAGON_LIGHT }
        : { location: [p.lat, p.lng], size: 0.035 },
    );

  function updateMarkers() {
    globe?.update({ markers: markers() });
  }

  async function ensureGlobe() {
    if (globe || loading) return;
    loading = true;
    try {
      const { default: createGlobe } = await import('cobe');
      if (globe || !inView) return;
      size = stage!.clientWidth;
      globe = createGlobe(canvas!, {
        devicePixelRatio: Math.min(window.devicePixelRatio || 1, 2),
        width: size,
        height: size,
        phi,
        theta,
        dark: 1,
        diffuse: 1.15,
        mapSamples: 20000,
        mapBrightness: 7,
        mapBaseBrightness: 0.025,
        baseColor: IVORY,
        markerColor: LAGON,
        glowColor: GLOW,
        opacity: 0.7,
        markerElevation: MARKER_ELEVATION,
        markers: markers(),
      });
      // Laisse le premier rendu se faire avant le fondu d'apparition.
      requestAnimationFrame(() => root.setAttribute('data-globe-state', 'ready'));
      startLoop();
    } catch {
      // Chunk introuvable (réseau) : la liste reste utilisable seule.
      root.dataset.globeState = 'unsupported';
    } finally {
      loading = false;
    }
  }

  function teardown() {
    stopLoop();
    if (!globe) return;
    globe.destroy();
    globe = null;
    // cobe enveloppe le canvas dans un <div> : on le retire pour pouvoir recréer le globe
    // proprement (retour depuis le bfcache).
    const wrapper = canvas!.parentElement;
    if (wrapper && wrapper !== stage) wrapper.replaceWith(canvas!);
    root.removeAttribute('data-globe-state');
  }

  // --- Boucle de rendu ---------------------------------------------------------------------
  /** Vrai tant qu'une image suivante changerait quelque chose. */
  function needsAnimation() {
    return dragging || target !== null || phiVelocity !== 0 || (!reduceMotion && !holding);
  }

  function canRun() {
    return globe !== null && inView && !document.hidden;
  }

  function startLoop() {
    if (rafId || !canRun()) return;
    lastTime = performance.now();
    rafId = requestAnimationFrame(tick);
  }

  function stopLoop() {
    if (rafId) cancelAnimationFrame(rafId);
    rafId = 0;
  }

  /** Demande au moins une image (après une sélection, un glisser, un redimensionnement). */
  function requestFrame() {
    startLoop();
  }

  function tick(now: number) {
    rafId = 0;
    if (!canRun()) return;
    const dt = Math.min((now - lastTime) / 1000, 0.1);
    lastTime = now;

    if (!dragging) {
      if (target) {
        // Rotation amortie vers le lieu sélectionné.
        const k = 1 - Math.exp(-dt * 3.2);
        const dPhi = shortest(phi, target.phi);
        const dTheta = target.theta - theta;
        phi += dPhi * k;
        theta += dTheta * k;
        if (Math.abs(dPhi) < 0.0005 && Math.abs(dTheta) < 0.0005) {
          phi = target.phi;
          theta = target.theta;
          target = null;
          holding = true;
        }
      } else {
        phi += phiVelocity * dt;
        phiVelocity *= Math.exp(-dt * 2.4);
        if (Math.abs(phiVelocity) < 0.002) phiVelocity = 0;
        if (!reduceMotion && !holding) {
          autoFactor = Math.min(1, autoFactor + dt * 0.6);
          phi += AUTO_SPEED * autoFactor * dt;
        }
      }
    }

    phi %= TAU;
    globe!.update({ phi, theta });
    placeHalos();

    if (needsAnimation()) rafId = requestAnimationFrame(tick);
  }

  /** Positionne les halos HTML au-dessus des marqueurs visibles (face avant du globe). */
  function placeHalos() {
    const half = size / 2;
    for (const place of places) {
      if (!place.halo) continue;
      const { x, y, z } = project(place.vector, phi, theta);
      const facing = z / (RADIUS + MARKER_ELEVATION);
      const opacity = clamp((facing - 0.12) / 0.3, 0, 1);
      place.halo.style.transform = `translate3d(${(half * (1 + x)).toFixed(1)}px, ${(half * (1 - y)).toFixed(1)}px, 0)`;
      place.halo.style.opacity = opacity.toFixed(3);
      place.halo.toggleAttribute('data-flip', x > 0.35);
    }
  }

  // --- Glisser (souris et tactile) avec inertie --------------------------------------------
  let lastX = 0;
  let lastY = 0;
  let lastMove = 0;
  let pointerId: number | null = null;

  canvas.addEventListener('pointerdown', (event) => {
    if (!globe || (event.pointerType === 'mouse' && event.button !== 0)) return;
    dragging = true;
    pointerId = event.pointerId;
    target = null;
    holding = false;
    phiVelocity = 0;
    autoFactor = 0;
    lastX = event.clientX;
    lastY = event.clientY;
    lastMove = event.timeStamp;
    canvas.setPointerCapture(event.pointerId);
    root.setAttribute('data-globe-dragging', '');
    requestFrame();
  });

  canvas.addEventListener('pointermove', (event) => {
    if (!dragging || event.pointerId !== pointerId) return;
    const dx = event.clientX - lastX;
    const dy = event.clientY - lastY;
    const dt = Math.max((event.timeStamp - lastMove) / 1000, 1 / 240);
    lastX = event.clientX;
    lastY = event.clientY;
    lastMove = event.timeStamp;

    // Une largeur de globe glissée ≈ un demi-tour.
    const dPhi = (dx / Math.max(size, 1)) * Math.PI;
    phi += dPhi;
    theta = clamp(theta + (dy / Math.max(size, 1)) * Math.PI * 0.6, -MAX_THETA, MAX_THETA);
    // Vitesse lissée, reprise comme inertie au relâchement.
    phiVelocity = phiVelocity * 0.6 + (dPhi / dt) * 0.4;
    requestFrame();
  });

  const endDrag = (event: PointerEvent) => {
    if (!dragging || event.pointerId !== pointerId) return;
    dragging = false;
    pointerId = null;
    root.removeAttribute('data-globe-dragging');
    // Relâché après une pause : pas d'élan.
    if (event.timeStamp - lastMove > 80) phiVelocity = 0;
    phiVelocity = reduceMotion ? 0 : clamp(phiVelocity, -6, 6);
    requestFrame();
  };
  canvas.addEventListener('pointerup', endDrag);
  canvas.addEventListener('pointercancel', endDrag);

  // --- Visibilité, redimensionnement, cycle de vie -----------------------------------------
  const onVisibility = (isVisible: boolean) => {
    inView = isVisible;
    if (inView) {
      if (globe) startLoop();
      else void ensureGlobe();
    } else {
      stopLoop();
    }
  };

  if ('IntersectionObserver' in window) {
    new IntersectionObserver((entries) => onVisibility(entries[entries.length - 1].isIntersecting), {
      rootMargin: '150px 0px',
    }).observe(stage);
  } else {
    onVisibility(true);
  }

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopLoop();
    else startLoop();
  });

  if ('ResizeObserver' in window) {
    new ResizeObserver(() => {
      const next = stage.clientWidth;
      if (!globe || !next || next === size) return;
      size = next;
      globe.update({ width: size, height: size });
      requestFrame();
    }).observe(stage);
  }

  reduceQuery.addEventListener('change', (event) => {
    reduceMotion = event.matches;
    requestFrame();
  });

  window.addEventListener('pagehide', teardown);
  window.addEventListener('pageshow', (event) => {
    if (event.persisted && inView) void ensureGlobe();
  });
}
