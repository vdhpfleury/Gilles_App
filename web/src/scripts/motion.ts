import { gsap } from 'gsap';

/*
 * Motion design, driven by data attributes (anti-flash rules live in global.css):
 * - [data-hero] / [data-hero-item] / [data-parallax]: hero entrance + scrubbed parallax
 * - [data-reveal]: fade + slide-up the first time a block enters the viewport
 * - [data-tilt]: pointer-following 3D tilt (mouse only)
 * - [data-magnetic]: cursor-attracted buttons/links (mouse only)
 * With prefers-reduced-motion, everything is shown at once and nothing moves.
 */

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = !window.matchMedia('(pointer: coarse)').matches;

/** Queues work in its own task, so the load-time work is split into short tasks. */
const nextTask = (fn: () => void) => window.setTimeout(fn, 0);

/** Hero entrance: staggered fade/slide-in of the [data-hero-item] elements. */
function initHeroEntrance() {
  const items = gsap.utils.toArray<HTMLElement>('[data-hero-item]');
  if (!items.length) return;

  if (reduceMotion) {
    gsap.set(items, { autoAlpha: 1, y: 0 });
    return;
  }

  gsap.fromTo(
    items,
    { autoAlpha: 0, y: 24 },
    { autoAlpha: 1, y: 0, duration: 0.8, ease: 'power3.out', stagger: 0.12, delay: 0.1 },
  );
}

/** Slow parallax drift of the hero image, scrubbed by ScrollTrigger (only loaded where needed). */
async function initParallax() {
  const parallax = document.querySelector<HTMLElement>('[data-parallax]');
  const heroSection = document.querySelector<HTMLElement>('[data-hero]');
  if (!parallax || !heroSection || reduceMotion) return;

  const { ScrollTrigger } = await import('gsap/ScrollTrigger');
  gsap.registerPlugin(ScrollTrigger);
  gsap.to(parallax, {
    yPercent: 12,
    ease: 'none',
    scrollTrigger: { trigger: heroSection, start: 'top top', end: 'bottom top', scrub: true },
  });
}

/**
 * Fade + slide up each [data-reveal] block the first time it enters the viewport (its top
 * crossing 88% of the viewport height); blocks already on screen at load cascade in.
 * A single IntersectionObserver watches every block: nothing measures the layout at load
 * (one ScrollTrigger per block re-measured the page for each of them, in one long task).
 * Opacity only (not autoAlpha/visibility): blocks not revealed yet stay in the accessibility
 * tree and in the Tab order, and focusing one reveals it at once.
 */
function initReveal() {
  const items = gsap.utils.toArray<HTMLElement>('[data-reveal]');
  if (!items.length) return;

  if (reduceMotion || !('IntersectionObserver' in window)) {
    gsap.set(items, { opacity: 1, y: 0 });
    return;
  }

  gsap.set(items, { opacity: 0, y: 32 });
  const pending = new Set<Element>(items);
  let firstBatch = true;

  const observer = new IntersectionObserver(
    (entries) => {
      let order = 0;
      for (const entry of entries) {
        // The first notification covers every block: reveal all those already on screen.
        const { top, bottom } = entry.boundingClientRect;
        const show = firstBatch ? top < window.innerHeight && bottom > 0 : entry.isIntersecting;
        if (!show || !pending.delete(entry.target)) continue;

        observer.unobserve(entry.target);
        gsap.to(entry.target, {
          opacity: 1,
          y: 0,
          duration: 0.7,
          ease: 'power2.out',
          // Blocks entering together (first screen, a row of cards) cascade.
          delay: (firstBatch ? 0.05 : 0) + Math.min(order++, 6) * 0.08,
        });
      }
      firstBatch = false;
    },
    { rootMargin: '0px 0px -12% 0px' },
  );
  items.forEach((el) => observer.observe(el));

  document.addEventListener('focusin', (event) => {
    const el = event.target instanceof Element ? event.target.closest('[data-reveal]') : null;
    if (!el || !pending.delete(el)) return;
    observer.unobserve(el);
    gsap.set(el, { opacity: 1, y: 0 });
  });
}

/** Pointer-following 3D tilt on a [data-tilt] card (set up on its first hover). */
function setupTilt(card: HTMLElement) {
  // quickTo() needs GSAP's internal transform names: rotationX/rotationY (not the
  // rotateX/rotateY aliases) and scaleX/scaleY (`scale` is split, so not eligible).
  const rotateX = gsap.quickTo(card, 'rotationX', { duration: 0.5, ease: 'power3.out' });
  const rotateY = gsap.quickTo(card, 'rotationY', { duration: 0.5, ease: 'power3.out' });
  const scaleX = gsap.quickTo(card, 'scaleX', { duration: 0.4, ease: 'power3.out' });
  const scaleY = gsap.quickTo(card, 'scaleY', { duration: 0.4, ease: 'power3.out' });
  const scale = (value: number) => {
    scaleX(value);
    scaleY(value);
  };

  // GSAP-only property (adds perspective() to the transform); not a CSS property.
  gsap.set(card, { transformPerspective: 700 });

  card.addEventListener('pointermove', (event) => {
    const rect = card.getBoundingClientRect();
    rotateY(((event.clientX - rect.left) / rect.width - 0.5) * 10);
    rotateX(((event.clientY - rect.top) / rect.height - 0.5) * -10);
  });
  card.addEventListener('pointerenter', () => scale(1.02));
  card.addEventListener('pointerleave', () => {
    rotateX(0);
    rotateY(0);
    scale(1);
  });

  scale(1.02); // the pointer is already over the card
}

/** Cursor-following "magnetic" pull on a [data-magnetic] button/link (set up on first hover). */
function setupMagnetic(el: HTMLElement) {
  const x = gsap.quickTo(el, 'x', { duration: 0.4, ease: 'power3.out' });
  const y = gsap.quickTo(el, 'y', { duration: 0.4, ease: 'power3.out' });

  el.addEventListener('pointermove', (event) => {
    const rect = el.getBoundingClientRect();
    x((event.clientX - (rect.left + rect.width / 2)) * 0.3);
    y((event.clientY - (rect.top + rect.height / 2)) * 0.35);
  });
  el.addEventListener('pointerleave', () => {
    x(0);
    y(0);
  });
}

/** Tilt and magnetic effects (mouse only): nothing runs until the pointer first enters. */
function initPointerEffects() {
  if (reduceMotion || !finePointer) return;

  gsap.utils.toArray<HTMLElement>('[data-tilt]').forEach((card) => {
    card.addEventListener('pointerenter', () => setupTilt(card), { once: true });
  });
  gsap.utils.toArray<HTMLElement>('[data-magnetic]').forEach((el) => {
    el.addEventListener('pointerenter', () => setupMagnetic(el), { once: true });
  });
}

function init() {
  // First task: the hero entrance must start right away.
  initHeroEntrance();

  // Then short separate tasks for the rest (keeps the main thread responsive at load).
  nextTask(() => {
    initReveal();
    // GSAP now owns the hidden/visible state (inline styles): the anti-flash CSS in
    // global.css (scoped to html.js:not(.motion-ready)) stops applying.
    document.documentElement.classList.add('motion-ready');

    nextTask(() => {
      initPointerEffects();
      initParallax().catch(() => {
        // Parallax is decorative: if its chunk fails to load, the page simply stays still.
      });
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
