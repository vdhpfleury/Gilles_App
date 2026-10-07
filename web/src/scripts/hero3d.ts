/*
 * "Living photo" hero (desktop only, loaded lazily by motion.ts): the hero photo is redrawn
 * in WebGL with a depth-map parallax that follows the pointer, caustic light ripples and
 * rising bubbles. The <img> stays underneath as the LCP element and the fallback: on any
 * failure the canvas is removed and the photo is left as it was.
 */

export interface Hero3DOptions {
  /** The hero section (pointer position is measured from its centre; render pauses when off screen). */
  hero: HTMLElement;
  /** The parallax wrapper of the photo: the canvas is appended to it, so it drifts with it. */
  wrapper: HTMLElement;
  /** The hero photo, already downloaded: reused as the colour texture. */
  img: HTMLImageElement;
  canvas: HTMLCanvasElement;
  gl: WebGLRenderingContext;
  /** Called once torn down, whatever the cause (failure, lost context, pagehide, caller). */
  onDestroy?: () => void;
}

const DEPTH_URL = '/3d/hero-wave-depth.webp';
const MAX_DPR = 1.5;
/**
 * Extra zoom over object-fit: cover (+4.5%), so the displaced lookups stay inside the texture:
 * per-side margin (1 - 1 / 1.045) / 2 ≈ 2.15% > max vertical displacement (1.9%) + shimmer.
 */
const ZOOM_EXTRA = 0.045;
/** Max displacement = 0.5 * DEPTH_STRENGTH = 1.25% of the texture width (more doubles edges). */
const DEPTH_STRENGTH = 0.025;
const CAUSTICS_INTENSITY = 0.12;
const POINTER_SMOOTHING = 0.06;
const BUBBLE_COUNT = 90;
const REPEL_RADIUS = 150;
/** The effects ease in after the fade, starting from a frame identical to the <img>. */
const INTRO_DELAY = 0.5;
const INTRO_DURATION = 1.8;

const FULLSCREEN_VS = `
attribute vec2 aPosition;
varying vec2 vUv;
void main() {
  vUv = vec2(aPosition.x, -aPosition.y) * 0.5 + 0.5;
  gl_Position = vec4(aPosition, 0.0, 1.0);
}`;

const PHOTO_FS = `
precision highp float;
uniform sampler2D uPhoto;
uniform sampler2D uDepth;
uniform vec2 uScale;
uniform vec2 uOffset;
uniform float uTime;
uniform float uIntro;
varying vec2 vUv;

// Iterated-turbulence caustic pattern (after joltz0r's "water turbulence").
float caustic(vec2 p, float t) {
  vec2 i = p;
  float c = 1.0;
  for (int n = 0; n < 5; n++) {
    float tt = t * (1.0 - 3.5 / float(n + 1));
    i = p + vec2(cos(tt - i.x) + sin(tt + i.y), sin(tt - i.y) + cos(tt + i.x));
    c += 1.0 / length(vec2(p.x / (sin(i.x + tt) / 0.005), p.y / (cos(i.y + tt) / 0.005)));
  }
  c = 1.17 - pow(c / 5.0, 1.4);
  return clamp(pow(abs(c), 8.0), 0.0, 1.0);
}

// Blurred depth: a soft edge spreads the stretch where the near plane meets the background,
// instead of smearing the foam around the diver into streaks.
float depthAt(vec2 uv) {
  const vec2 r = vec2(0.016, 0.024);
  float sum = texture2D(uDepth, uv).r * 2.0;
  sum += texture2D(uDepth, uv + vec2(r.x, 0.0)).r + texture2D(uDepth, uv - vec2(r.x, 0.0)).r;
  sum += texture2D(uDepth, uv + vec2(0.0, r.y)).r + texture2D(uDepth, uv - vec2(0.0, r.y)).r;
  sum += texture2D(uDepth, uv + r * 0.7).r + texture2D(uDepth, uv - r * 0.7).r;
  sum += texture2D(uDepth, uv + vec2(r.x, -r.y) * 0.7).r + texture2D(uDepth, uv + vec2(-r.x, r.y) * 0.7).r;
  return sum / 10.0;
}

void main() {
  vec2 uv = (vUv - 0.5) * uScale + 0.5;
  // Two fixed-point steps approximate the inverse displacement: fewer doubled edges.
  float depth = depthAt(uv);
  depth = depthAt(clamp(uv + (depth - 0.5) * uOffset, 0.0, 1.0));
  vec2 duv = uv + (depth - 0.5) * uOffset;

  // Open water only (not the diver nor the foam at the surface), fading with depth in the frame.
  float water = (1.0 - smoothstep(0.45, 0.9, depth)) * mix(1.0, 0.45, smoothstep(0.3, 1.0, vUv.y));
  float t = uTime * 0.22;
  // Faint refraction shimmer, mostly in the open water.
  duv += vec2(sin(duv.y * 38.0 + t * 5.0), cos(duv.x * 31.0 + t * 4.0)) * 0.0012 * water * uIntro;
  duv = clamp(duv, 0.001, 0.999);

  vec3 color = texture2D(uPhoto, duv).rgb;
  // Under one 2*PI period across the photo (no visible tiling); the -250 offset sets the line width.
  float light = caustic(duv * vec2(6.0, 4.0) - 250.0, t);
  light *= 0.65 + 0.35 * sin(duv.x * 4.0 - t * 1.3 + duv.y * 3.0);
  light *= water * uIntro;
  // Partly multiplicative, so the ripples light the scene rather than sit on top of it.
  vec3 tint = mix(vec3(0.31, 0.54, 0.55), vec3(0.96, 0.95, 0.92), light);
  color = color * (1.0 + light * 0.4) + tint * light * ${CAUSTICS_INTENSITY.toFixed(3)};
  gl_FragColor = vec4(color, 1.0);
}`;

const BUBBLE_VS = `
attribute vec4 aBubble;
uniform vec2 uResolution;
uniform float uPixelRatio;
varying float vAlpha;
void main() {
  vec2 clip = aBubble.xy / uResolution * 2.0 - 1.0;
  gl_Position = vec4(clip.x, -clip.y, 0.0, 1.0);
  gl_PointSize = aBubble.z * uPixelRatio;
  vAlpha = aBubble.w;
}`;

const BUBBLE_FS = `
precision mediump float;
varying float vAlpha;
void main() {
  vec2 p = gl_PointCoord * 2.0 - 1.0;
  float r = length(p);
  float disc = 1.0 - smoothstep(0.84, 1.0, r);
  if (disc <= 0.0) discard;
  float rim = smoothstep(0.5, 0.92, r);
  float spec = 1.0 - smoothstep(0.0, 0.3, length(p - vec2(-0.34, -0.38)));
  float alpha = clamp(0.07 + rim * 0.5 + spec * 0.9, 0.0, 1.0) * disc * vAlpha;
  vec3 color = mix(vec3(0.62, 0.82, 0.84), vec3(1.0, 0.98, 0.93), clamp(spec + rim * 0.3, 0.0, 1.0));
  gl_FragColor = vec4(color * alpha, alpha);
}`;

type Vec2 = { x: number; y: number };

interface Bubble {
  x: number;
  y: number;
  size: number;
  /** 0 = far/small, 1 = near/big. */
  near: number;
  speed: number;
  phase: number;
  wobble: number;
  frequency: number;
  push: Vec2;
}

const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value));
const smoothstep = (t: number) => {
  const x = clamp(t, 0, 1);
  return x * x * (3 - 2 * x);
};
const nextFrame = () => new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
const nextTask = () => new Promise<void>((resolve) => setTimeout(resolve, 0));

function compileShader(gl: WebGLRenderingContext, type: number, source: string): WebGLShader {
  const shader = gl.createShader(type);
  if (!shader) throw new Error('hero3d: createShader failed');
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  return shader;
}

/** Compiles and links without blocking the main thread where KHR_parallel_shader_compile exists. */
async function createProgram(gl: WebGLRenderingContext, vs: string, fs: string): Promise<WebGLProgram> {
  const program = gl.createProgram();
  if (!program) throw new Error('hero3d: createProgram failed');
  const shaders = [compileShader(gl, gl.VERTEX_SHADER, vs), compileShader(gl, gl.FRAGMENT_SHADER, fs)];
  shaders.forEach((shader) => gl.attachShader(program, shader));
  gl.linkProgram(program);

  const parallel = gl.getExtension('KHR_parallel_shader_compile');
  if (parallel) {
    while (!gl.isContextLost() && !gl.getProgramParameter(program, parallel.COMPLETION_STATUS_KHR)) {
      await nextFrame();
    }
  }
  shaders.forEach((shader) => gl.deleteShader(shader));
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    throw new Error(`hero3d: link failed: ${gl.getProgramInfoLog(program) ?? ''}`);
  }
  return program;
}

function createTexture(gl: WebGLRenderingContext, source: TexImageSource, format: number): WebGLTexture {
  const texture = gl.createTexture();
  if (!texture) throw new Error('hero3d: createTexture failed');
  gl.bindTexture(gl.TEXTURE_2D, texture);
  // Non-power-of-two textures in WebGL1: clamp + no mipmaps.
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texImage2D(gl.TEXTURE_2D, 0, format, format, gl.UNSIGNED_BYTE, source);
  return texture;
}

interface PhotoSource {
  source: TexImageSource;
  aspect: number;
  release: () => void;
}

/** The hero photo as a texture source (no new download), as an ImageBitmap where supported. */
async function loadPhoto(img: HTMLImageElement): Promise<PhotoSource> {
  await img.decode();
  const aspect = img.naturalWidth / img.naturalHeight;
  if (!('createImageBitmap' in window)) return { source: img, aspect, release: () => {} };
  const bitmap = await createImageBitmap(img);
  return { source: bitmap, aspect, release: () => bitmap.close() };
}

async function loadDepth(): Promise<HTMLImageElement> {
  const depth = new Image();
  depth.decoding = 'async';
  depth.src = DEPTH_URL;
  await depth.decode();
  return depth;
}

/** Texture scale reproducing object-fit: cover (centred), then zoomed in by `zoom`. */
function coverScale(canvasAspect: number, textureAspect: number, zoom: number): [number, number] {
  return canvasAspect > textureAspect
    ? [1 / zoom, textureAspect / canvasAspect / zoom]
    : [canvasAspect / textureAspect / zoom, 1 / zoom];
}

function createBubble(width: number, height: number, anywhere: boolean): Bubble {
  // Mostly small (far) bubbles, a few big near ones.
  const near = Math.random() ** 2.2;
  const size = 2.5 + near * 17;
  return {
    x: Math.random() * width,
    y: anywhere ? Math.random() * height : height + size + Math.random() * 60,
    size,
    near,
    speed: 16 + near * 64 + Math.random() * 10,
    phase: Math.random() * Math.PI * 2,
    wobble: 2 + near * 8,
    frequency: 0.6 + Math.random(),
    push: { x: 0, y: 0 },
  };
}

interface BubbleFrame {
  dt: number;
  time: number;
  width: number;
  height: number;
  intro: number;
  /** Smoothed pointer offset, -1..1 from the hero centre. */
  offset: Vec2;
  /** Pointer in canvas CSS pixels, or null when it is not over the page. */
  pointer: Vec2 | null;
  maxSize: number;
}

/** Moves the bubbles and writes [x, y, size, alpha] per bubble into `out`. */
function updateBubbles(bubbles: Bubble[], out: Float32Array, frame: BubbleFrame) {
  const { dt, time, width, height, intro, offset, pointer, maxSize } = frame;
  const relax = 1 - Math.exp(-dt * 5);

  bubbles.forEach((bubble, index) => {
    bubble.y -= bubble.speed * dt;
    if (bubble.y < -bubble.size) Object.assign(bubble, createBubble(width, height, false));

    // Near bubbles shift opposite to the pointer, like the near parts of the photo.
    const parallax = 3 + bubble.near * 22;
    const x = bubble.x + Math.sin(time * bubble.frequency + bubble.phase) * bubble.wobble - offset.x * parallax;
    const y = bubble.y - offset.y * parallax;

    let targetX = 0;
    let targetY = 0;
    if (pointer) {
      const dx = x - pointer.x;
      const dy = y - pointer.y;
      const distance = Math.hypot(dx, dy);
      if (distance > 0 && distance < REPEL_RADIUS) {
        const force = (1 - distance / REPEL_RADIUS) ** 2 * (24 + bubble.near * 30);
        targetX = (dx / distance) * force;
        targetY = (dy / distance) * force;
      }
    }
    bubble.push.x += (targetX - bubble.push.x) * relax;
    bubble.push.y += (targetY - bubble.push.y) * relax;

    const o = index * 4;
    out[o] = x + bubble.push.x;
    out[o + 1] = y + bubble.push.y;
    out[o + 2] = Math.min(bubble.size, maxSize);
    // Fade in from the bottom so respawns never pop.
    out[o + 3] = (0.2 + bubble.near * 0.5) * intro * smoothstep((height - bubble.y) / 80);
  });
}

/**
 * Mounts the WebGL hero on top of the photo. Resolves with a teardown function; on any failure
 * (missing depth map, shader error, lost context) the canvas is removed and the photo stays.
 */
export async function mountHero3D({ hero, wrapper, img, canvas, gl, onDestroy }: Hero3DOptions): Promise<() => void> {
  const listeners = new AbortController();
  const { signal } = listeners;
  const programs: WebGLProgram[] = [];
  const textures: WebGLTexture[] = [];
  const buffers: WebGLBuffer[] = [];
  // Queried before any upload: once the GPU is busy, getParameter stalls until it is done.
  const maxPointSize = (gl.getParameter(gl.ALIASED_POINT_SIZE_RANGE) as Float32Array)[1];
  let releasePhoto = () => {};
  let resizeObserver: ResizeObserver | null = null;
  let intersectionObserver: IntersectionObserver | null = null;
  let destroyed = false;
  let rafId = 0;

  const destroy = () => {
    if (destroyed) return;
    destroyed = true;
    listeners.abort();
    cancelAnimationFrame(rafId);
    resizeObserver?.disconnect();
    intersectionObserver?.disconnect();
    if (!gl.isContextLost()) {
      programs.forEach((program) => gl.deleteProgram(program));
      textures.forEach((texture) => gl.deleteTexture(texture));
      buffers.forEach((buffer) => gl.deleteBuffer(buffer));
      gl.getExtension('WEBGL_lose_context')?.loseContext();
    }
    releasePhoto();
    canvas.remove();
    onDestroy?.();
  };

  canvas.setAttribute('aria-hidden', 'true');
  canvas.style.cssText =
    'position:absolute;inset:0;display:block;width:100%;height:100%;pointer-events:none;opacity:0;transition:opacity .8s ease';
  canvas.addEventListener('webglcontextlost', destroy, { signal });
  window.addEventListener('pagehide', destroy, { signal });
  wrapper.append(canvas);

  try {
    const [photo, depth] = await Promise.all([loadPhoto(img), loadDepth()]);
    releasePhoto = photo.release;
    if (destroyed) {
      photo.release();
      return destroy;
    }

    await nextTask();
    const photoProgram = await createProgram(gl, FULLSCREEN_VS, PHOTO_FS);
    const bubbleProgram = await createProgram(gl, BUBBLE_VS, BUBBLE_FS);
    programs.push(photoProgram, bubbleProgram);
    if (destroyed) return destroy;

    await nextTask();
    textures.push(createTexture(gl, photo.source, gl.RGB));
    await nextTask();
    textures.push(createTexture(gl, depth, gl.LUMINANCE));
    if (destroyed) return destroy;

    // The GPU copy is enough from now on.
    releasePhoto();
    startRendering({ photoProgram, bubbleProgram, textureAspect: photo.aspect });
  } catch {
    // Decorative layer: any failure just leaves the photo.
    destroy();
  }
  return destroy;

  function startRendering({
    photoProgram,
    bubbleProgram,
    textureAspect,
  }: {
    photoProgram: WebGLProgram;
    bubbleProgram: WebGLProgram;
    textureAspect: number;
  }) {
    const [photoTexture, depthTexture] = textures;
    const photoUniforms = {
      scale: gl.getUniformLocation(photoProgram, 'uScale'),
      offset: gl.getUniformLocation(photoProgram, 'uOffset'),
      time: gl.getUniformLocation(photoProgram, 'uTime'),
      intro: gl.getUniformLocation(photoProgram, 'uIntro'),
    };
    const bubbleUniforms = {
      resolution: gl.getUniformLocation(bubbleProgram, 'uResolution'),
      pixelRatio: gl.getUniformLocation(bubbleProgram, 'uPixelRatio'),
    };
    const positionLocation = gl.getAttribLocation(photoProgram, 'aPosition');
    const bubbleLocation = gl.getAttribLocation(bubbleProgram, 'aBubble');

    gl.useProgram(photoProgram);
    gl.uniform1i(gl.getUniformLocation(photoProgram, 'uPhoto'), 0);
    gl.uniform1i(gl.getUniformLocation(photoProgram, 'uDepth'), 1);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, photoTexture);
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, depthTexture);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

    // One oversized triangle covers the whole viewport.
    const triangleBuffer = gl.createBuffer();
    const bubbleBuffer = gl.createBuffer();
    if (!triangleBuffer || !bubbleBuffer) throw new Error('hero3d: createBuffer failed');
    buffers.push(triangleBuffer, bubbleBuffer);
    gl.bindBuffer(gl.ARRAY_BUFFER, triangleBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const bubbleData = new Float32Array(BUBBLE_COUNT * 4);
    gl.bindBuffer(gl.ARRAY_BUFFER, bubbleBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, bubbleData.byteLength, gl.DYNAMIC_DRAW);

    let dpr = 1;
    let width = 1;
    let height = 1;
    let bubbles: Bubble[] = [];

    const pointerClient: Vec2 = { x: 0, y: 0 };
    let pointerOver = false;
    let lastMove = -Infinity;
    const offset: Vec2 = { x: 0, y: 0 };

    let time = 0;
    let lastNow = 0;
    let firstFrameAt = -1;
    let inView = false;
    let visible = false;

    function resize(cssWidth: number, cssHeight: number) {
      if (cssWidth < 1 || cssHeight < 1) return;
      dpr = Math.min(window.devicePixelRatio || 1, MAX_DPR);
      canvas.width = Math.round(cssWidth * dpr);
      canvas.height = Math.round(cssHeight * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
      if (bubbles.length) bubbles.forEach((bubble) => (bubble.x *= cssWidth / width));
      else bubbles = Array.from({ length: BUBBLE_COUNT }, () => createBubble(cssWidth, cssHeight, true));
      width = cssWidth;
      height = cssHeight;
    }

    function updateOffset(dt: number) {
      const rect = hero.getBoundingClientRect();
      const target: Vec2 = { x: 0, y: 0 };
      if (pointerOver) {
        target.x = clamp((pointerClient.x - rect.left - rect.width / 2) / (rect.width / 2), -1, 1);
        target.y = clamp((pointerClient.y - rect.top - rect.height / 2) / (rect.height / 2), -1, 1);
      }
      // Slow idle drift once the pointer has been still for a moment, so the scene keeps breathing.
      const stillness = smoothstep((time - lastMove - 1.5) / 2.5);
      target.x = clamp(target.x + Math.sin(time * 0.21) * 0.45 * stillness, -1, 1);
      target.y = clamp(target.y + Math.sin(time * 0.13 + 1) * 0.3 * stillness, -1, 1);

      const k = 1 - (1 - POINTER_SMOOTHING) ** (dt * 60);
      offset.x += (target.x - offset.x) * k;
      offset.y += (target.y - offset.y) * k;
    }

    function pointerInCanvas(): Vec2 | null {
      if (!pointerOver) return null;
      // getBoundingClientRect includes the wrapper's scale/translate; map back to CSS pixels.
      const rect = canvas.getBoundingClientRect();
      return {
        x: ((pointerClient.x - rect.left) / rect.width) * width,
        y: ((pointerClient.y - rect.top) / rect.height) * height,
      };
    }

    function draw(intro: number) {
      const zoom = 1 + ZOOM_EXTRA * intro;
      const strength = DEPTH_STRENGTH * intro;

      gl.disable(gl.BLEND);
      gl.useProgram(photoProgram);
      gl.uniform2fv(photoUniforms.scale, coverScale(width / height, textureAspect, zoom));
      // y scaled by the texture aspect so the displacement is isotropic in pixels.
      gl.uniform2f(photoUniforms.offset, offset.x * strength, offset.y * strength * textureAspect);
      gl.uniform1f(photoUniforms.time, time);
      gl.uniform1f(photoUniforms.intro, intro);
      gl.bindBuffer(gl.ARRAY_BUFFER, triangleBuffer);
      gl.enableVertexAttribArray(positionLocation);
      gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      gl.disableVertexAttribArray(positionLocation);

      if (intro <= 0) return;
      gl.enable(gl.BLEND);
      gl.useProgram(bubbleProgram);
      gl.uniform2f(bubbleUniforms.resolution, width, height);
      gl.uniform1f(bubbleUniforms.pixelRatio, dpr);
      gl.bindBuffer(gl.ARRAY_BUFFER, bubbleBuffer);
      gl.bufferSubData(gl.ARRAY_BUFFER, 0, bubbleData);
      gl.enableVertexAttribArray(bubbleLocation);
      gl.vertexAttribPointer(bubbleLocation, 4, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.POINTS, 0, BUBBLE_COUNT);
      gl.disableVertexAttribArray(bubbleLocation);
    }

    function render(dt: number) {
      const intro = firstFrameAt < 0 ? 0 : smoothstep((time - firstFrameAt - INTRO_DELAY) / INTRO_DURATION);
      updateOffset(dt);
      updateBubbles(bubbles, bubbleData, {
        dt,
        time,
        width,
        height,
        intro,
        offset,
        pointer: pointerInCanvas(),
        maxSize: maxPointSize / dpr,
      });
      draw(intro);
    }

    function frame(now: number) {
      rafId = 0;
      const dt = clamp((now - lastNow) / 1000, 0, 1 / 20);
      lastNow = now;
      time += dt;
      render(dt);
      if (firstFrameAt < 0) {
        firstFrameAt = time;
        // The first frame matches the <img> exactly (no zoom, no effects): a seamless cross-fade.
        requestAnimationFrame(() => (canvas.style.opacity = '1'));
      }
      schedule();
    }

    function schedule() {
      if (destroyed || !inView || !visible || rafId) return;
      rafId = requestAnimationFrame(frame);
    }

    function updateRunning() {
      visible = document.visibilityState === 'visible';
      if (inView && visible) {
        lastNow = performance.now();
        schedule();
      } else if (rafId) {
        cancelAnimationFrame(rafId);
        rafId = 0;
      }
    }

    window.addEventListener(
      'pointermove',
      (event) => {
        pointerClient.x = event.clientX;
        pointerClient.y = event.clientY;
        pointerOver = true;
        lastMove = time;
      },
      { passive: true, signal },
    );
    document.addEventListener(
      'pointerout',
      (event) => {
        if (!event.relatedTarget) pointerOver = false;
      },
      { signal },
    );
    document.addEventListener('visibilitychange', updateRunning, { signal });

    resizeObserver = new ResizeObserver(([entry]) => {
      resize(entry.contentRect.width, entry.contentRect.height);
      // Resizing clears the drawing buffer: redraw now so no blank frame gets painted.
      if (firstFrameAt >= 0) render(0);
    });
    resizeObserver.observe(canvas);

    intersectionObserver = new IntersectionObserver(([entry]) => {
      inView = entry.isIntersecting;
      updateRunning();
    });
    intersectionObserver.observe(hero);
  }
}
